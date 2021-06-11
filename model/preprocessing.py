# Eventually we will add code to Convert WAV files to Mel Spectrograms
# https://colab.research.google.com/drive/1oJC1Te5-OyUuWKJ5wOJd5edy7ct1Dtih?usp=sharing


import pathlib
import os
import re

import boto3

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
# For plotting headlessly (i.e. not also showing in notebook)
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import librosa
import librosa.display
import numpy as np


BUCKET_NAME = 'hey-spotify'

GOOGLE_INPUT_AUDIO_PATH = 'input_audio/speech_commands_v0.02/down'
GOOGLE_SPEECH_COMMANDS_SAMPLE_RATE_HZ = 16000

MOZILLA_INPUT_AUDIO_PATH = 'input_audio/mozilla/down'
MOZILLA_COMMON_VOICE_SAMPLE_RATE_HZ = 48000

# Write each Mel Spectrogram to this local path first; then upload to S3.
TEMP_LOCAL_MEL_SPECTROGRAM_PATH = '/tmp/mel_spectrogram.png'


def load_using_librosa(file_contents, sample_rate_hz):
    # There has to be a way to read directly from S3 into librosa without writing the bytes to disk.
    with open('/tmp/audio_file', 'wb') as file:
        file.write(file_contents)

    return librosa.load('/tmp/audio_file', sr=sample_rate_hz)


def convert_audio_file_to_mel_spectrogram(file_contents, sample_rate_hz):
    y, sr = load_using_librosa(file_contents, sample_rate_hz)

    mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=1024)
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)

    fig = plt.Figure()
    fig.patch.set_visible(False)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    # No whitespace at edge of image
    for spline in ['bottom', 'left', 'top', 'right']:
        ax.spines[spline].set_visible(False)

    librosa.display.specshow(mel_spect, ax=ax)
    fig.savefig(TEMP_LOCAL_MEL_SPECTROGRAM_PATH, bbox_inches='tight', pad_inches=0)


def ensure_dir_exists(dir):
    pathlib.Path(dir).mkdir(parents=True, exist_ok=True)


def mel_spectrogram_file_path(audio_file_path):
    _, extension = os.path.splitext(audio_file_path)

    in_target_dir = audio_file_path.replace('input_audio', 'mel_spectrograms')

    return re.sub(rf'{extension}$', '.png', in_target_dir)


def sample_rate(path):
    if path.startswith(GOOGLE_INPUT_AUDIO_PATH):
        return GOOGLE_SPEECH_COMMANDS_SAMPLE_RATE_HZ

    if path.startswith(MOZILLA_INPUT_AUDIO_PATH):
        return MOZILLA_COMMON_VOICE_SAMPLE_RATE_HZ

    raise RuntimeError(f'sample rate unknown for {path}')


def all_s3_objects(s3, path):
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=path)

    sr = sample_rate(path)

    i = 1
    for page in pages:
        for obj in page['Contents']:
            print(f"Downloading {obj['Key']} ({i})")
            s3_response = s3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
            s3_content = s3_response["Body"].read()
            i += 1
            yield({'Key': obj['Key'], 'Content': s3_content, 'SampleRate': sr})


def convert_files_to_mel_spectrogram(s3, source_path):
    print(f"Converting audio from {source_path}")

    for object in all_s3_objects(s3, source_path):
        print(f"Converting {object['Key']}")
        convert_audio_file_to_mel_spectrogram(object['Content'], object['SampleRate'])

        remote_mel_spectrogram_path = mel_spectrogram_file_path(object['Key'])
        print(f'Uploading to {remote_mel_spectrogram_path}')

        with open(TEMP_LOCAL_MEL_SPECTROGRAM_PATH, "rb") as f:
            s3.upload_fileobj(f, BUCKET_NAME, remote_mel_spectrogram_path)
        print()


def ignore_warnings_from_librosa():
    # https://github.com/librosa/librosa/issues/1015
    import warnings
    warnings.filterwarnings('ignore')


def determine_max_length(s3, source_path):
    for object in all_s3_objects(s3, source_path):
        print(object['Key'])
        y, sr = load_using_librosa(object['Content'], object['SampleRate'])
        d = librosa.get_duration(y)
        print(d)


# TODO padding?
# TODO MP3 length (according to librosa) is not correct, that might not matter for converting to mel-spectrograms
# but it may matter for padding. Will need to verify.

# Either librosa doesn’t correctly read in MP3s or else doesn’t correctly report the duration (edited)
# Presumably padding (to maximum length in dataset?) should be done. How else to feed same format data to the model?
# Maybe possible to achieve same results by having the model ‘on the fly’ look at only n-second-long windows
# That’s ultimately what is needed anyway: to detect the wake word in some window of audio,
# not to detect the wake word in a longer audio file — in one Mozilla example the length can be 13 seconds,
# do we really want all Mel Spectrograms to be that size?

def main():
    ignore_warnings_from_librosa()

    s3 = boto3.client('s3')

    for source_path in [GOOGLE_INPUT_AUDIO_PATH, MOZILLA_INPUT_AUDIO_PATH]:
        convert_files_to_mel_spectrogram(s3, source_path)

    print('done!')


if __name__ == "__main__":
    main()
