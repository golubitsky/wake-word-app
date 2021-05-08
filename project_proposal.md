# Student Project Proposal

## Project Title

Hey, Spotify

## Industry Sponsorship (if Any)

Spotify

## Problem definition

Determine whether a single, known-ahead-of-time wake word is present in audio:

- prototype will accept audio of a single word
  - For this portion, we will use the Google speech_commands dataset only.
- eventually, detect the word as part of more complex audio (phrases)
  - Research ongoing for this portion.
- as time allows, increase robustness/tolerance to noise
  - Metrics to include optimization between acceptable rates of false positives and false negatives (precision/recall).

## Key Research Questions/ Technological constraints that the Project will Answer

- How to pre-process the data to improve model performance?
- What would be a good wake word?
- What makes a wake word "unique enough?"
- Is it possible to model what would make a "bad" wake word. For example, "tree" might be a bad word because it's similar to "three," which is often spoken, and thus, will lead to false positives.

## Final deliverables at the end of the project

[Please list the desired technical deliverables from the project team in as much detail as possible]

Key activities/ technologies the project team may be expected to undertake/ work with
[E.g. What kind of technology stack will you work with, the datasets you may need to work on, what kind of analysis you may be expected to undertake, etc.]

- Prediction API - answer the question "is wake word present in this audio?"
- User-facing webapp that will allow user to:

  - MVP: (only via API - no webapp at this point) specify detect wake word in audio that's already available on the server to classify.
  - v1: detect wake word in audio recorded via UI and sent to server.
  - v2: detect wake word in audio streamed via UI -> server.

- Preprocessing: FFT to convert problem into image recognition using spectrograms.
- Training
  - Convolutional Neural Network (CNN) using Tensorflow/Keras
  - RNN, if time allows

## Ethical considerations

- Under-representation of various groups in the training data:

  - male/female/child
  - ethnicity (accents)

- Existing datasets are anonymized.
- For the webapp, user will initiate and consent to recording and sending of their voice for prediction.

## Expected learning outcomes

[What do you expect to learn from the project? Please mention the technical skills you will imbibe over the project.]

## Team

#### Member names

- Georgia
- Jida
- Misha

## Tentative Timeplan

Submit a tentative time plan (table/chart or text) regarding breakdown of the work that will be conducted between May 2021- July 2
