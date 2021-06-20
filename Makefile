build:
	docker build -t gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1 .

develop: build
	docker-compose up

deploy: build
	docker push gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1
	echo 'manually deploy at https://console.cloud.google.com/run/deploy/us-east1/golubitsky-ml-model-deployment-without-cloud-build?project=fb-mle-march-21'