The purpose of this repo is to deploy a machine learning model to the cloud. We accomplish this using GCP Cloud Build/Cloud Run. We deploy TensorFlow models developed using Python code in the `notebooks/` directory.

# Quickstart

- `make build` - build a Docker image
- `make server` - run the dev server using the Docker image (available on http://localhost:5000)
- `make test` - run tests using the Docker image

Every command above includes `make build` to ensure the latest code is used.

# Model training code

All model training code can be found in the `notebooks/` directory. These serve as an archive, for future enhancements.

# Deployment

Summary of deployment attempts via:

- [x] GCP Cloud Run: succeeded to deploy service.
  - https://golubitsky-ml-model-qvmmc7xxqa-ue.a.run.app/
- [x] GCP Cloud Build integration for Github — full CI/CD is enabled.
  - Simply merge to `main`.
- [ ] AWS ECS: missing iam:CreateRole permissions; this will not be resolved, as CI/CD deployments already work via GCP.

Further details of the 3 deployment attempts can be found in [deployment_history.README.md](deployment_history.README.md).

## Deployment Overview

For the deployment, we built a Flask API, containerized it using Docker, and deployed it on the Google Cloud Platform (GCP). We used GCP Cloud Run to deploy the containerized API service. We set up continuous integration and continuous delivery (CI/CD) using GCP Cloud Build, such that a push to the GitHub repo (https://github.com/golubitsky/wake-word-app) results in a new build being deployed to the cloud. Inside of the Flask API, we wrote a thin service layer to serve the Tensorflow/Keras models. We also provide a minimal UI to expose our optimal model.

### Integration contract during development

The purpose of defining an integration contract between multiple engineers is to enable each person to work independently and to minimize integration challenges. This is even more crucial on a larger team, where data scientists who develop models may not have the engineering expertise to deploy those models, and vice-versa. The integration contract that worked for us was that one engineer would develop a model and be responsible for the following deliverables:

1. The model artifact
2. A snippet of Python code to load the model and predict on a sample in an agreed-upon format/shape
3. Documentation of the model (e.g. hyperparameters, considerations for future enhancements)
4. Dependencies required to predict using the model

That way, another engineer working on the infrastructure to serve the model can work independently, with a relatively simple integration stage.

### Scaling

#### Larger models

At the moment, we commit the model to the source code. This works because our model size is small. However, this would not scale to larger model sizes and/or when we have many models to choose from. In that case, presumably we would explore the use of a Machine Learning Model Registry, such that we would store the model artifact in a NoSQL database somewhere, register the artifact, and, as it is booting up, have the Flask API retrieve the specific version of the model whose prediction is to be served.

#### Multiple types of models

In our MVP phase, we worked with TensorFlow models only. If multiple types of model are to be served (for example scikit-learn and PyTorch models, in addition to the TensorFlow models), we might first write independent Prediction modules in our Flask API for each type of model, and if that becomes hard to manage, consider writing multiple API services, one for each type of model.

At this point, it is likely that a dedicated Model Registry will help significantly to both streamline the deployments as well as to keep track of each model version and its documentation.

If we have many different types of models, we will seek the right abstraction, so that we can deploy different models with minimal additional code and effort. These patterns would become evident as we develop and maintain multiple models in production.
