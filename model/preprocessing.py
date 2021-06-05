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

# TODO set sample rate for Mozilla?
GOOGLE_SPEECH_COMMANDS_SAMPLE_RATE_HZ = 16000


def open_audio_file(path):
    s3_client = boto3.resource('s3')
    s3_client.download_file('hey-spotify', path, '/tmp/audio_file')


def convert_audio_file_to_mel_spectrogram(audio_file_path, local_tmp_mel_spectrogram_output_path):
    # Begin hack
    res = s3.get_object(Bucket='hey-spotify', Key=audio_file_path)
    content = res["Body"].read()
    # There has to be a way to read directly from S3 into librosa without writing the bytes to disk.
    with open('/tmp/audio_file', 'wb') as file:
        file.write(content)
    # End hack

    y, sr = librosa.load('/tmp/audio_file', sr=GOOGLE_SPEECH_COMMANDS_SAMPLE_RATE_HZ)
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
    fig.savefig(local_tmp_mel_spectrogram_output_path, bbox_inches='tight', pad_inches=0)


def ensure_dir_exists(dir):
    pathlib.Path(dir).mkdir(parents=True, exist_ok=True)


def mel_spectrogram_file_path(audio_file_path):
    _, extension = os.path.splitext(audio_file_path)

    in_target_dir = audio_file_path.replace('input_audio', 'mel_spectrograms')

    return re.sub(rf'{extension}$', '.png', in_target_dir)


BUCKET_NAME = 'hey-spotify'
s3 = boto3.client('s3')
inputs = s3.list_objects(Bucket=BUCKET_NAME, Prefix='input_audio/speech_commands_v0.02/down')['Contents']

# MEL_SPECTROGRAM_DIR = mel_spectrograms/speech_commands_v0.02/down

for input in inputs:
    local_tmp_mel_spectrogram_output_path = '/tmp/mel_spectrogram.png'
    convert_audio_file_to_mel_spectrogram(input['Key'], local_tmp_mel_spectrogram_output_path)
    remote_mel_spectrogram_path = mel_spectrogram_file_path(input['Key'])

    with open(local_tmp_mel_spectrogram_output_path, "rb") as f:
        s3.upload_fileobj(f, BUCKET_NAME, remote_mel_spectrogram_path)
    # TODO remove the break to run for all
    # TODO add progress indicator: i.e. "converting x of 2344 files"
    # or use tqdm package
    break

print('done!')
