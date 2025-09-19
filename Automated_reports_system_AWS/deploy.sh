#!/bin/bash

echo "Building SAM application..."
sam build

echo "Deploying to AWS..."
sam deploy --guided

echo "Deployment complete!"
echo "The system will automatically generate daily reports at 9 AM UTC"