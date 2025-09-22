import json
import boto3
import os
import csv
import io
from datetime import datetime, timedelta
import random

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # This allows generation in the console/direct invocation as well as through API Gateway invocation
        if 'reportId' in event:
            
            report_data = event
        else:
            # EventBridge scheduled event
            report_data = {
                'reportId': f"auto-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
                'reportType': event.get('reportType', 'daily'),
                'parameters': {},
                'status': 'REQUESTED',
                'automated': event.get('automated', True),
                'createdAt': datetime.utcnow().isoformat()
            }
            
            # Store automated report in DynamoDB
            table = dynamodb.Table(os.environ['REPORTS_TABLE'])
            table.put_item(Item=report_data)
        
        report_id = report_data['reportId']
        report_type = report_data['reportType']
        
        # Update status to GENERATING for building report
        update_report_status(report_id, 'GENERATING')
        
        # Generate report based on type
        if report_type == 'daily':
            report_content = generate_daily_report()
        elif report_type == 'weekly':
            report_content = generate_weekly_report()
        elif report_type == 'monthly':
            report_content = generate_monthly_report()
        else:
            report_content = generate_custom_report(report_data.get('parameters', {}))
        
        # Save report to S3 bucket
        file_key = f"reports/{report_id}/{report_type}_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        
        s3.put_object(
            Bucket=os.environ['REPORTS_BUCKET'],
            Key=file_key,
            Body=report_content,
            ContentType='text/csv'
        )
        
        # Update report status to COMPLETED after upload is done
        table = dynamodb.Table(os.environ['REPORTS_TABLE'])
        table.update_item(
            Key={'reportId': report_id},
            UpdateExpression='SET #status = :status, fileKey = :fileKey, completedAt = :completedAt',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'COMPLETED',
                ':fileKey': file_key,
                ':completedAt': datetime.utcnow().isoformat()
            }
        )
        
        print(f"Report {report_id} generated successfully")
        return {'statusCode': 200, 'reportId': report_id, 'fileKey': file_key}
        
    except Exception as e:
        # Update status to FAILED

        if 'reportId' is not None:
            update_report_status(report_id, 'FAILED', str(e))
        raise e




#=================
#helpers
#=================

#helper function to update the status in DDB
def update_report_status(report_id, status, error=None):
    table = dynamodb.Table(os.environ['REPORTS_TABLE'])
    update_expression = 'SET #status = :status, updatedAt = :updatedAt'
    expression_values = {
        ':status': status,
        ':updatedAt': datetime.utcnow().isoformat()
    }
    
    if error:
        update_expression += ', errorMessage = :error'
        expression_values[':error'] = error
    
    table.update_item(
        Key={'reportId': report_id},
        UpdateExpression=update_expression,
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues=expression_values
    )
# Simulates daily metrics
def generate_daily_report():
    
    data = []
    for hour in range(24):
        data.append({
            'hour': f"{hour:02d}:00",
            'users': random.randint(50, 500),
            'requests': random.randint(1000, 5000),
            'errors': random.randint(0, 50)
        })
    
    return create_csv_content(data)

# Simulates weekly metrics

def generate_weekly_report():
    data = []
    for day in range(7):
        date = datetime.utcnow() - timedelta(days=day)
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'users': random.randint(1000, 10000),
            'revenue': round(random.uniform(5000, 50000), 2),
            'orders': random.randint(100, 1000)
        })
    
    return create_csv_content(data)


# Simulates monthly metrics
def generate_monthly_report():
    
    data = []
    for week in range(4):
        data.append({
            'week': f"Week {week + 1}",
            'total_users': random.randint(10000, 50000),
            'total_revenue': round(random.uniform(100000, 500000), 2),
            'avg_order_value': round(random.uniform(50, 200), 2)
        })
    
    return create_csv_content(data)

# if the report type isn't a time based type, function will generate custom report
def generate_custom_report(parameters):
    # Generate custom report based on parameters
    data = [{
        'parameter': key,
        'value': value,
        'timestamp': datetime.utcnow().isoformat()
    } for key, value in parameters.items()]
    
    return create_csv_content(data)

# Creates CSV report
def create_csv_content(data):
    if not data:
        return "No data available"
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    
    return output.getvalue()