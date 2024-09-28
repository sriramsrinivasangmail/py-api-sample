#!/usr/bin/env bash

image="py-api-sample:v1"

script_dir=$(dirname $0)

cd ${script_dir}

docker build -t ${image} .
