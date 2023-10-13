#!/bin/bash

# Set the name of the Lambda function and the directory where the function code is located
LAMBDA_FUNCTION_NAME="task_manager_lambda"
LAMBDA_FUNCTION_DIR="src/${LAMBDA_FUNCTION_NAME}}"

# Create a temporary directory to store the packaged dependencies
TMP_DIR=$(mktemp -d)

# Install the dependencies to the temporary directory
pip install -r ${LAMBDA_FUNCTION_DIR}/requirements.txt -t ${TMP_DIR}

# Zip the Lambda function code and the dependencies
cd ${LAMBDA_FUNCTION_DIR}
zip -r9 ${LAMBDA_FUNCTION_NAME}.zip .
cd ${TMP_DIR}
zip -r9 ${LAMBDA_FUNCTION_NAME}.zip .

# Move the zipped Lambda function and dependencies to the parent directory
mv ${LAMBDA_FUNCTION_NAME}.zip ../

# Clean up the temporary directory
rm -rf ${TMP_DIR}