## Overview

- [Project definition](https://docs.google.com/document/d/1OT4Ia46U7MTkquMIEYaLrGxiw7zxvn0Db_ogwX9X0kw/edit)
- [How to work on your Capstone](https://docs.google.com/document/d/1h-XXeTrYdn_SWidsiF9iBrdtkksXJJjm-TYWXep74fE/edit)
- [System design and ethical considerations](https://canvas.instructure.com/courses/2578379/modules/items/42755620)

## Questions

- What will the features be?
- Can we train just a yes/no classifier as a baseline? Or even something simpler?
- Might want to build the simplest possible model (i.e. "if audio is not silent, wake word is detected") in order to get the web app and API up and running. Later we can iterate on the model.
- Need to explore the datasets; some resources below. There's a tensorflow tutorial for the Speech Commands Dataset.
- [honk](https://github.com/castorini/honk) GitHub may provide baseline of web app code; also the GitHub for [howl-deploy](https://github.com/castorini/howl-deploy).

### Progression of complexity in pattern recognition

- Simplest possible pattern recognition:
  - Substring in a word.
  - Arrangement of pixels.
  - These two don't have variance for each example. Every instance identical.
- OCR - digit recognition - variance.
- Applying [Mel-Spectrogram](https://towardsdatascience.com/getting-to-know-the-mel-spectrogram-31bca3e2d9d0) to audio could transform problem into OCR

  - Show many examples of wake word; also some negative examples.
  - Finding the word in arbitrary-length audio is harder than simply detecting a digit in 32x32 images, having trained on 32x32 images.

### Scaling

- Possible to train on phonemes? Datasets with phonemes? Could help to generalize to any wake word?
  - General model (i.e. ability to specify wake-word at run time, already having trained) is much harder/different than specific model (wake-word known before training).
- How much data is needed? Does increasing amount of data help?

## Papers

For existing papers on the subject of wake word detection, see [papers.md](papers.md) (with notes).

## Datasets

See [datasets.md](datasets.md).

## Technical

- [librosa](https://librosa.org/doc/latest/tutorial.html)
- [Dockerized PyTorch + GPU](https://ngc.nvidia.com/catalog/containers/nvidia:pytorch)
- [WavAugment](https://github.com/facebookresearch/WavAugment) - [colab walkthrough](https://colab.research.google.com/github/facebookresearch/WavAugment/blob/master/examples/python/WavAugment_walkthrough.ipynb)

### Audio Streaming/Recording

It would be pretty awesome to build an app that could:

- stream audio from a user's microphone to the API
- API will interpret the stream, and every `n` seconds (where `n` might be like 1 or 3 or something..) will pass `n` seconds of audio as a "chunk" into the model
- API will return "yes" or "no" to the client at the end of processing every "chunk" of audio

But a simpler goal would be to just provide the user the ability to record a `n`-second-long clip and have that send to the server for the "yes"/"no" answer.

Research in this direction:

- https://webrtc.org/
- https://github.com/nexmo-community/audiosocket_framework/blob/main/server.py
- https://www.html5rocks.com/en/tutorials/webrtc/basics/
- https://github.com/aiortc/aiortc
- https://dev.to/whitphx/python-webrtc-basics-with-aiortc-48id
- https://github.com/golubitsky/explorations/tree/master/aiortc-server-example -- could be used for streaming (?), can't get it to 'work'.
- https://github.com/golubitsky/explorations/tree/master/brautopy - this works to record `wav` files from the browser.

## TODO

- [Simple audio recognition: Recognizing keywords tensorflow tutorial](https://www.tensorflow.org/tutorials/audio/simple_audio) on [speech commands dataset](https://www.tensorflow.org/datasets/catalog/speech_commands)
  - [GitHub](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/speech_commands)
  - [Hey Spotify! went through the tutorial (colab)](https://colab.research.google.com/drive/1N7KJ-TS-d91heKK1s3q8nnT7LaRTdZat#scrollTo=dHqqcuf4PL9T)
- Set up frontend app (this repo); probably using create-react-app.
- Prototype to capture audio and send to API.
- Repo for model-training, API, deployment.

## Done

- Repo for front-end app (so it can easily be developed separately).

## Along the way/miscellaneous

- [Blog about going to production asap](https://www.bodyworkml.com/posts/scikit-learn-meet-production)
