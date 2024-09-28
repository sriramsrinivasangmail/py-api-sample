#! /usr/bin/env bash

script_dir=$(dirname $0)
src_dir=${script_dir}/../src

cd ${src_dir}/generated
python main.py
