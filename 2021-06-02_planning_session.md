## What we should work on soon

### Upload google data

- Upload google data to S3: ‘down’ only
  - Manually is fine. It’s already just one folder of files. Or light-weight script.

### Preprocessing: audio -> Mel spectrogram

- Script to convert WAV -> Mel Spectrogram (already prototyped, but need script that can run against S3)
  - Normalize length of audio/dimension of images? Similar to Tensorflow tutorial.
    - Find the longest file we have.
    - While creating images
      - pad with empty audio so that each represents the same length.
      - Where to pad? Is beginning best?
- Script to convert MP3 -> Mel Spectrogram (not yet prototyped; presumably small modification needed w.r.t. WAV, if any)

#### How to develop the script?

- SageMaker issue: how to pull in the latest version of our repo — we want to commit our scripts to the repo, SageMaker doesn’t automatically pull the latest code for us.

  - These docs “Using Git repositories in a notebook instance” say that we can just !git pull origin master
    - https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-notebooks-now-support-git-integration-for-increased-persistence-collaboration-and-reproducibility/
  - Determine if requirements are missing; we can pip install -r requirements.txt https://docs.aws.amazon.com/sagemaker/latest/dg/nbi-add-external.html
  - Maybe as first step, prototype the script in SageMaker, then port to our repo as a script. When we run the script, it will have been git pulled from our repo.

#### Deploy/run the script

- Run script to convert all audio -> Mel Spectrogram -> S3.

#### Train!

At this point we’d be ready to train a model. Woo!

- train-test-split
- model v1
  - Train what?
  - RNN?
  - AutoML?

How to evaluate the model?
