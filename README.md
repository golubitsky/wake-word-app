## Overview

- [Project definition](https://docs.google.com/document/d/1OT4Ia46U7MTkquMIEYaLrGxiw7zxvn0Db_ogwX9X0kw/edit)
- [How to work on your Capstone](https://docs.google.com/document/d/1h-XXeTrYdn_SWidsiF9iBrdtkksXJJjm-TYWXep74fE/edit)

## Questions

- What will the features be?
- Can we train just a yes/no classifier as a baseline?

## Approaches

- Simplest possible pattern recognition:
  - Substring in a word.
  - Arrangement of pixels.
  - These two don't have variance for each example. Every instance identical.
- OCR - digit recognition - variance.
- Applying [Mel-Spectrogram](https://towardsdatascience.com/getting-to-know-the-mel-spectrogram-31bca3e2d9d0) to audio could transform problem into OCR

  - Show many examples of wake word; also some negative examples.
  - Finding the word in arbitrary-length audio is harder than simply detecting a digit in 32x32 images, having trained on 32x32 images.

- Possible to train on phonemes? Datasets with phonemes? Could help to generalize to any wake word?

## Papers

For existing papers on the subject of wake word detection, see [papers.md](papers.md) (with notes).

## Datasets

- [Google Speech Commands Dataset](https://ai.googleblog.com/2017/08/launching-speech-commands-dataset.html)
  - [Paper about this dataset](https://arxiv.org/pdf/1804.03209.pdf)
- [Mozilla Common Voice Dataset](https://commonvoice.mozilla.org/en/datasets)

## Technical

- [librosa](https://librosa.org/doc/latest/tutorial.html)
- [Dockerized PyTorch + GPU](https://ngc.nvidia.com/catalog/containers/nvidia:pytorch)

## TODO

- [Simple audio recognition: Recognizing keywords tensorflow tutorial](https://www.tensorflow.org/tutorials/audio/simple_audio) on [speech commands dataset](https://www.tensorflow.org/datasets/catalog/speech_commands)
  - [GitHub](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/speech_commands)
- Set up frontend app (this repo); probably using create-react-app.
- Prototype to capture audio and send to API.
- Repo for model-training, API, deployment.

## Done

- Repo for front-end app (so it can easily be developed separately).

## Along the way/miscellaneous

- [Blog about going to production asap](https://www.bodyworkml.com/posts/scikit-learn-meet-production)
