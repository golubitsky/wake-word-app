## Overview

- [Project definition](https://docs.google.com/document/d/1OT4Ia46U7MTkquMIEYaLrGxiw7zxvn0Db_ogwX9X0kw/edit)
- [How to work on your Capstone](https://docs.google.com/document/d/1h-XXeTrYdn_SWidsiF9iBrdtkksXJJjm-TYWXep74fE/edit)
- [System design and ethical considerations](https://canvas.instructure.com/courses/2578379/modules/items/42755620)

## Development

To develop:

0. Download Docker: https://www.docker.com/products/docker-desktop
1. Change source code.
2. Build
3. Run

### Build

```sh
docker build -t wake-word-app .
```

### Run

```sh
# Volume mount the credentials for AWS; probably not needed in EC2.
docker run -it -v ~/.aws:/root/.aws wake-word-app python3 model/preprocessing.py
# Without credentials
docker run -it wake-word-app python3 model/preprocessing.py
```

## Development Quick Links

Username is your email.

- [AWS SageMaker: hey-spotify](https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/notebook-instances)
- [AWS S3 bucket: hey-spotify](https://s3.console.aws.amazon.com/s3/home?region=us-east-1#)

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

- Implement baseline model based on Howl research paper: “res8”.
- identify first wake-word that we will try to find in sentences — wake-word must appear in many sentences in https://commonvoice.mozilla.org/en/datasets — we don’t know how to find frequency of sentences by word, no index appears to exist for mozilla dataset, need to investigate
  - this will be the baseline data we need to train the “res8" model.
- load our 2 datasets into S3 bucket
- determine what data to use from our 2 datasets
- train baseline model using data sample
- How to standardize audio length in pre-processing. Need to?
- Pre-process audio into images.
- How to code (in isolation, preferably) the best model from howl paper (res8)?
- What is a small sample of data we can use to train it?

  - Can we use just Google Speech Commands dataset? It doesn’t contain sentences. And our model will need “wake words” and “sentences” (which to classify as containing or not containing wake words). But maybe as the simplest model we can use words from Google Speech Commands as both.
  - It’s possible to import a sample of this dataset pretty easily, as shown in "Simple audio recognition: Recognizing keywords tensorflow tutorial"

- Explore the Mozilla Common Voice Dataset

  - Can we import a sample? The full english dataset is ~58 GB in size.

- Set up frontend app (this repo); probably using create-react-app.
- Prototype to capture audio and send to API.
- Repo for model-training, API, deployment.

  - We may consider having multiple folders in this one repo instead. That may be simpler for us to work with for now.
  - SageMaker will need access to a repo with our model code for training.
  - Existing SageMaker instance already imports this repo but we can always change it.
  - It might make most sense to have two separate repos. One for the front-end (this repo). One for the rest (another repo).

## Done

- Identify baseline model based on Howl research paper: “res8”.
- Setup `hey-spotify` S3 bucket
- Setup `hey-spotify` SageMaker instance, remember to add during creating instance:
  - tags: team name, each team member name
  - lifecycle policy - auto-idle-stop
- Prototype how to read files from S3 bucket [make sure you can see this notebook on the SageMaker instance](https://hey-spotify.notebook.us-east-1.sagemaker.aws/notebooks/wake-word-app/S3%20demo.ipynb)
- [Convert WAV files to Mel Spectrograms](https://colab.research.google.com/drive/1oJC1Te5-OyUuWKJ5wOJd5edy7ct1Dtih?usp=sharing)
  - No white space in output of Mel Spectrograms.
  - Output not shown in notebook; only saved to filesystem.
- [Simple audio recognition: Recognizing keywords tensorflow tutorial](https://www.tensorflow.org/tutorials/audio/simple_audio) on [speech commands dataset](https://www.tensorflow.org/datasets/catalog/speech_commands)
  - [GitHub](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/speech_commands)
  - [Hey Spotify! went through the tutorial (colab)](https://colab.research.google.com/drive/1N7KJ-TS-d91heKK1s3q8nnT7LaRTdZat#scrollTo=dHqqcuf4PL9T)
- Repo for front-end app (so it can easily be developed separately).

## Along the way/miscellaneous

- [Blog about going to production asap](https://www.bodyworkml.com/posts/scikit-learn-meet-production)
