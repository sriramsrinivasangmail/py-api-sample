#!/bin/bash
fastapi-codegen --input ./src/api/aroma-api.yaml  --template-dir ./src/api/templates/ --output ./src/generated
