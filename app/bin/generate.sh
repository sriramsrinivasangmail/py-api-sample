#!/bin/bash

script_dir=$(dirname $0)
src_dir=${script_dir}/../src

#rm -fr ${src_dir}/generated

fastapi-codegen --input ${src_dir}/api/aroma-api.yaml --generate-routers  --template-dir ${src_dir}/api/templates/ --output ${src_dir}/generated
