#!/bin/bash

# Build and deploy the SAM application
echo "Building SAM application..."
sam build

echo "Deploying to AWS..."
sam deploy --guided

echo "Deployment complete!"
echo "Check the outputs for your API Gateway URL"