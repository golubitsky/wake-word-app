#!/usr/bin/env bash

branch=$(git rev-parse --abbrev-ref HEAD)
image=gcr.io/fb-mle-march-21/golubitsky/ml-model-develop
image_name="$image:$branch"

echo $image_name
