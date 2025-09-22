import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

#This function is used to handle the failure of the order processing. It will update the order status in the DynamoDB table and log the failure.
def update_order_status(order_id, error_info, cause):
    table = dynamodb.Table(os.environ['ORDERS_TABLE'])
    try:
        table.update_item(
            Key={'orderId': order_id},
            UpdateExpression='SET #status = :status, #error = :error, #updatedAt = :updatedAt',
            ExpressionAttributeNames={
                '#status': 'status',
                '#error': 'error',
                '#updatedAt': 'updatedAt'
            },
            ExpressionAttributeValues={
                ':status': 'FAILED',
                ':error': {
                    'message': error_info,
                    'cause': cause,
                    'timestamp': datetime.utcnow().isoformat()
                },
                ':updatedAt': datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        print(f"Failed to update order status: {str(e)}")

def lambda_handler(event, context):
    
    
    # Grab error information
    error_info = event.get('Error', 'Unknown error')
    cause = event.get('Cause', 'No cause provided')
    
    # Get the original order data
    order_data = event
    if 'orderId' in order_data:
        order_id = order_data['orderId']
        
        # Update order status in DynamoDB
        update_order_status(order_id, error_info, cause)
    
    # Log the failure
    failure_log = {
        'orderId': order_data.get('orderId', 'unknown'),
        'error': error_info,
        'cause': cause,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    print(f"Order processing failed: {json.dumps(failure_log)}")
    
    return {
        'status': 'FAILED',
        'error': error_info,
        'orderId': order_data.get('orderId')
    }