import json
import boto3
import os


s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    try:
        report_id = event['pathParameters']['reportId']
        
        # Get report data from DDB
        table = dynamodb.Table(os.environ['REPORTS_TABLE'])
        response = table.get_item(Key={'reportId': report_id})
        
        if 'Item' not in response:
            return create_response(404, {'error': 'Report not found'})
        
        report = response['Item']
        
        # If report is completed, generate presigned URL for download
        if report['status'] == 'COMPLETED' and 'fileKey' in report:
            try:
                download_url = s3.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': os.environ['REPORTS_BUCKET'],
                        'Key': report['fileKey']
                    },
                    # Expires in an hour
                    ExpiresIn=3600  
                )
                report['downloadUrl'] = download_url
            except Exception as e:
                print(f"Error generating presigned URL: {str(e)}")
        
        return create_response(200, report)
        
    except Exception as e:
        return create_response(500, {'error': str(e)})

# Response generation helper
def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, default=str)
    }