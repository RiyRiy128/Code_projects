import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        table = dynamodb.Table(os.environ['REPORTS_TABLE'])
        
        # Get query parameters
        query_params = event.get('queryStringParameters') or {}
        status = query_params.get('status')
        limit = int(query_params.get('limit', 20))
        
        if limit > 100:
            limit = 100
        
        if status:
            # Query by status using Non-primary-key/Index
            response = table.query(
                IndexName='StatusIndex',
                KeyConditionExpression=Key('status').eq(status),
                Limit=limit,
                ScanIndexForward=False  # Sort by newest first
            )
        else:
            # Scan all reports
            response = table.scan(Limit=limit)
        
        reports = response.get('Items', [])
        
        # Sort by the creation dates if not using secondary keys
        if not status:
            reports.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
        
        return create_response(200, {
            'reports': reports,
            'count': len(reports)
        })
        
    except ValueError:
        return create_response(400, {'error': 'Invalid limit parameter'})
    except Exception as e:
        return create_response(500, {'error': str(e)})

def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body, default=str)
    }