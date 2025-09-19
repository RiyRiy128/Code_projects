import json
import boto3
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        # Validates if the report type is specified
        if 'reportType' not in body:
            return create_response(400, {'error': 'reportType is required'})
        
        # Generate report ID
        report_id = str(uuid.uuid4())
        
        # Create report record
        report = {
            'reportId': report_id,
            'reportType': body['reportType'],
            'parameters': body.get('parameters', {}),
            'status': 'REQUESTED',
            'requestedBy': body.get('userId', 'anonymous'),
            'createdAt': datetime.utcnow().isoformat(),
            'automated': False
        }
        
        # Store it in DynamoDB
        table = dynamodb.Table(os.environ['REPORTS_TABLE'])
        table.put_item(Item=report)
        
        # Trigger report generation function asynchronously
        lambda_client.invoke(
            FunctionName=os.environ['GENERATE_FUNCTION_NAME'],
            InvocationType='Event', 
            Payload=json.dumps(report)
        )

        print(f"Report generation started: {report_id}")
        

        #We'll return 202 because the report is being processed/generated still
        return create_response(202, {
            'reportId': report_id,
            'status': 'REQUESTED',
            'message': 'Report generation started'
        })
        
    except json.JSONDecodeError:
        return create_response(400, {'error': 'Invalid JSON'})
    except Exception as e:
        return create_response(500, {'error': str(e)})


# Helper response function
def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body, default=str)
    }