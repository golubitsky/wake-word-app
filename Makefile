build:
	docker build -t gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1 .

develop: build
	docker-compose up

deploy: build
	docker push gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1
	echo 'image pushed; now manually deploy'