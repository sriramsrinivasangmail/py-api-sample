#!/bin/bash

cd $(dirname $0)

image="py-api-sample:v1"

docker run --rm -it --entrypoint=/bin/bash --user 1001 -v ${PWD}/app:/app ${image}
