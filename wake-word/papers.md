- [Howl](https://www.aclweb.org/anthology/2020.nlposs-1.9.pdf)
  - [GitHub](https://github.com/castorini/howl)
  - We further make the distinction between wake word detection and speech commands classification toolkits such as Honk (Tang and Lin, 2017). These frameworks focus on classifying fixed-length audio as one of a few dozen keywords, with no evaluation on a sizable negative set, as required in wake word detection. While these trained models may be used in detection applications, they are not rigorously tested for such.
- [Honk](https://arxiv.org/pdf/1710.06554.pdf) (_linked from Howl_): A PyTorch Reimplementation of Convolutional Neural Networks for Keyword Spotting
  - [GitHub](https://github.com/castorini/honk)
    - A utility for recording and building custom speech commands, producing audio samples of the appropriate length and format.
    - Test harnesses for training and testing any of a number of models implemented in TensorFlow and those proposed by [Sainath and Parada][1].
    - A RESTful service that deploys a trained model. The server accepts base 64-encoded audio and responds with the predicted label of the utterance. This service can be used for on-device keyword spotting via local loopback.
    - A desktop application for demonstrating the keyword spotting models described in this paper. The client uses the REST API above for model inference.
  - To augment the dataset and to increase robustness, background noise consisting of white noise, pink noise, and human-made noise are mixed in with some of the input audio, and the sample is randomly time-shifted. For feature extraction, a band-pass filter of 20Hz/4kHz is first applied to reduce the effect of unimportant sounds. Forty-dimensional Mel-Frequency Cepstrum Coefficient (MFCC) frames are then constructed and stacked using a 30 ms window size and 10 ms frame shift.
  - If desired, the convolution can stride by `s×v` and max-pool in `p×q, parameters which also influence the compactness of the model.
  - The integer value of the SHA1 hash of the filename is used to place each example into either the training, validation, or test sets.
- [Convolutional Neural Networks for Small-footprint Keyword Spotting][1] (_linked from Honk_)
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
- https://paperswithcode.com/task/keyword-spotting

- https://www.connectedpapers.com/main/ea2690304b0f08cf298247bcc0d341e2a2981299/Howl-A-Deployed-OpenSource-Wake-Word-Detection-System/graph
  - [Few-Shot Keyword Spotting With Prototypical Networks](https://arxiv.org/pdf/2007.14463.pdf)
  - [Metric Learning for Keyword Spotting](https://arxiv.org/pdf/2005.08776.pdf)
  - [MatchboxNet: 1D Time-Channel Separable Convolutional Neural Network Architecture for Speech Commands Recognition](https://arxiv.org/pdf/2004.08531.pdf)
  - [Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition](https://arxiv.org/pdf/1804.03209.pdf)

[1]: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43969.pdf
