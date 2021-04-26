## Overview

- [Project definition](https://docs.google.com/document/d/1OT4Ia46U7MTkquMIEYaLrGxiw7zxvn0Db_ogwX9X0kw/edit)
- [How to work on your Capstone](https://docs.google.com/document/d/1h-XXeTrYdn_SWidsiF9iBrdtkksXJJjm-TYWXep74fE/edit)

## Papers

- [Howl](https://www.aclweb.org/anthology/2020.nlposs-1.9.pdf)
  - [GitHub](https://github.com/castorini/howl)
- [Honk](https://arxiv.org/pdf/1710.06554.pdf) (_linked from Howl_): A PyTorch Reimplementation of Convolutional Neural Networks for Keyword Spotting
- [Convolutional Neural Networks for Small-footprint Keyword Spotting](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43969.pdf) (_linked from Honk_)
  - The problem is [keyword spotting (KWS)](https://en.wikipedia.org/wiki/Keyword_spotting)
  - Convolutional Neural Networks (CNNs) have become popular for acoustic modeling
  - Performance: CNN > DNN > Hidden Markov Model
  - Performance is measured by looking at the false reject (FR) rate at the operating
    threshold of 1 false alarm (FA) per hour
  - First, in the feature extraction module, 40 dimensional log-mel filterbank features are computed every 25ms with a 10ms frame shift. Next, at every frame, we stack 23 frames to the left and 8 frames to the right, and input this into the DNN.
  - The network weights are trained to optimize a cross-entropy criterion using distributed asynchronous gradient descent.
  - Multiple stride params are used: "the filter can stride by a non-zero amount s in time and v in frequency."
  - A typical convolutional architecture that has been heavily tested and shown to work well on many LVCSR (Large Vocabulary Conversational Speech Recognition) tasks is to use two convolutional layers.
  - 10K–15K utterances containing each of these phrases.
  - 396K 'negative' utterances
  - Next, we created noisy training and evaluation sets by artificially adding car and cafeteria noise at SNRs randomly sampled between [-5dB, +10dB] to the clean data sets. Models are trained in noisy conditions, and evaluated in both clean and noisy conditions.
  - KWS performance is measured by plotting a receiver operating curve (ROC), which calculates the false reject (FR) rate per false alarm (FA) rate. The lower the FR per FA rate is the better. The KWS system threshold is selected to correspond to 1 FA per hour of speech on this set.
  - MG: I can't quite follow the discussion about pooling/striding in time vs frequency, need to learn more about mel spectrogram.

## Datasets

- [Google Speech Commands Dataset](https://ai.googleblog.com/2017/08/launching-speech-commands-dataset.html)
- [Mozilla Common Voice Dataset](https://commonvoice.mozilla.org/en/datasets)

## Libraries

- [librosa](https://librosa.org/doc/latest/tutorial.html)

## TODO

- Set up frontend app (this repo); probably using create-react-app.
- Prototype to capture audio and send to API.
- Repo for model-training, API, deployment.

## Done

- Repo for front-end app (so it can easily be developed separately).

## Along the way/miscellaneous

- [Blog about going to production asap](https://www.bodyworkml.com/posts/scikit-learn-meet-production)
