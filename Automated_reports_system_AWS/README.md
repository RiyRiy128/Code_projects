# Automated Report Generation System

Creates reports on-demand and on schedule

## What It Does

**Manual Reports**: Users request reports via API Gateway → System generates CSV files via lambda → Users download via secure S3 links

**Automated Reports**: System generates daily reports automatically at 9AM UTC

## Architecture

- **API Gateway**: Handles user requests
- **Lambda Functions**: Generate and process reports
- **EventBridge**: Triggers daily reports automatically
- **S3**: Stores report files
- **DynamoDB**: Tracks report status

## How It Works

### Manual Reports
1. User calls API with report type (daily/weekly/custom)
2. System creates report record and starts generation
3. Lambda function creates CSV with sample data
4. File uploaded to S3, status updated to "COMPLETED"
5. User gets download link via API Gateway response

### Automated Reports
1. EventBridge triggers Lambda at 9 AM UTC daily
2. Lambda generates report automatically
3. Report saved with ID like "auto-20240117-090000"
4. Same process as manual, but no user request needed

## API Usage

### Request a Report
***
curl -X POST https://your-api-url/dev/reports \
  -H "Content-Type: application/json" \
  -d '{
    "reportType": "daily",
    "userId": "user_123"
  }'
***

### Check Report Status
***
curl https://your-api-url/dev/reports/REPORT_ID
***

### List All Reports
***
curl https://your-api-url/dev/reports
***

## Report Types

- **Daily**
- **Weekly**
- **Monthly**
- **Custom**: User-defined parameters

## Deployment

# Deploy to AWS environment
sam build && sam deploy

# Get your API URL from outputs
aws cloudformation describe-stacks --stack-name automated-report \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text

## Testing

### Test Manual Reports

# Request report
API_URL="https://your-api-id.execute-api.eu-west-1.amazonaws.com/dev"
curl -X POST $API_URL/reports \
  -H "Content-Type: application/json" \
  -d '{"reportType": "daily", "userId": "test_user"}'

# Check status (wait 10 seconds)
curl $API_URL/reports | jq '.reports[0]'


### Test Automated Reports

# Trigger EventBridge rule manually
aws events put-events --entries '[{
  "Source": "manual.test",
  "DetailType": "Test Trigger",
  "Detail": "{\"reportType\": \"daily\", \"automated\": true}"
}]'

# Check for automated reports (wait 10 seconds)
curl $API_URL/reports | jq '.reports[] | select(.automated == true)'

