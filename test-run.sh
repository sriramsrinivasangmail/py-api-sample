#!/bin/bash

cd $(dirname $0)

image="py-api-sample:v1"
cname=py-api

docker rm -f ${cname}
docker run --name ${cname} -d --user 1001 -p 20080:20080 -v ${PWD}/src:/mnt/src ${image}
