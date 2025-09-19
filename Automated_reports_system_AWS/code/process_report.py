import json
import boto3
import os
from datetime import datetime


sns = boto3.client('sns')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# This function will be triggered when a report is pushed to the bucket
def lambda_handler(event, context):
   
    try:
        # Process the S3 event
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            print(f"Processing report: {key}")
            
            # Extract report ID from file path
            report_id = extract_report_id_from_key(key)
            if not report_id:
                print(f"Could not extract report ID from key: {key}")
                continue
            
            # Get report metadata
            table = dynamodb.Table(os.environ['REPORTS_TABLE'])
            response = table.get_item(Key={'reportId': report_id})
            
            if 'Item' not in response:
                print(f"Report not found in database: {report_id}")
                continue
            
            report = response['Item']
            
            # Get file size and metadata
            s3_response = s3.head_object(Bucket=bucket, Key=key)
            file_size = s3_response['ContentLength']
            
            # Update report with processing info
            table.update_item(
                Key={'reportId': report_id},
                UpdateExpression='SET processedAt = :processedAt, fileSize = :fileSize, #status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':processedAt': datetime.utcnow().isoformat(),
                    ':fileSize': file_size,
                    ':status': 'PROCESSED'
                }
            )
            
            # Send notification
            await_send_notification(report, key, file_size)
            
            # Depending on what the report type is, additional processing will be done
            if report['reportType'] == 'daily' and report.get('automated'):
                
                perform_daily_analysis(report, bucket, key)
            
        return {'statusCode': 200, 'message': 'Reports processed successfully'}
        
    except Exception as e:
        print(f"Error processing report: {str(e)}")
        return {'statusCode': 500, 'error': str(e)}


# Grabs the reportId from the key path
def extract_report_id_from_key(key):
    
    try:

        parts = key.split('/')
        if len(parts) >= 2 and parts[0] == 'reports':
            return parts[1]
    except:
        pass
    return None


# Simply logs/simulates SNS notification but can be altered to actually send one
def await_send_notification(report, file_key, file_size):
   
    try:
        message = {
            'reportId': report['reportId'],
            'reportType': report['reportType'],
            'status': 'PROCESSED',
            'fileKey': file_key,
            'fileSize': file_size,
            'automated': report.get('automated', False),
            'completedAt': datetime.utcnow().isoformat()
        }
        
        subject = f"Report {report['reportId']} - {report['reportType'].title()} Report Ready"
        
        # If this was a real implementation, you would have SNS topic ARN from environment or statically defined here, but this is a simulation so I'll make log simply
        
        print(f"Notification sent: {subject}")
        print(f"Message: {json.dumps(message, indent=2)}")
        
        # Can cncomment below to actually send the SNS notification
        # sns.publish(
        #     TopicArn=os.environ.get('SNS_TOPIC_ARN'),
        #     Subject=subject,
        #     Message=json.dumps(message, indent=2)
        # )
        
    except Exception as e:
        print(f"Error sending notification: {str(e)}")


# Helper to perform simple analysis and update the report(s)
def perform_daily_analysis(report, bucket, key):

    try:
        
        # Fetch the report and populate
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        
        # Strip by lines and remove the header
        lines = content.strip().split('\n')
        data_rows = len(lines) - 1  
        
        # Update report with analysis
        table = dynamodb.Table(os.environ['REPORTS_TABLE'])
        table.update_item(
            Key={'reportId': report['reportId']},
            UpdateExpression='SET analysis = :analysis',
            ExpressionAttributeValues={
                ':analysis': {
                    'dataPoints': data_rows,
                    'analyzedAt': datetime.utcnow().isoformat(),
                    'summary': f"Daily report contains {data_rows} data points"
                }
            }
        )
        
        print(f"Analysis is completed for report {report['reportId']}: {data_rows} data points")
        
    except Exception as e:
        print(f"There was an error performing analysis: {str(e)}")