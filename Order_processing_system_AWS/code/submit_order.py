import json
import boto3
import uuid
import os
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
stepfunctions = boto3.client('stepfunctions')


#Helper function since dynamodb doesn't support float types, have to convert it to decimal - returned thi:{"error": "Float types are not supported. Use Decimal types instead."}% on testing prior to helper
def convert_floats_to_decimal(obj):
    if isinstance(obj, list):
        return [convert_floats_to_decimal(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_floats_to_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj
#Step functions can't serialize decimals in JSON, so we convert it back with this helper for the state machine input
def convert_decimals_to_float(obj):
    
    if isinstance(obj, list):
        return [convert_decimals_to_float(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimals_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def lambda_handler(event, context):
    try:
        
        body = json.loads(event['body'])
        
        # Generate order ID
        order_id = str(uuid.uuid4())
        
        # Create an order record here
        order = {
            'orderId': order_id,
            'customerId': body['customerId'],
            'items': convert_floats_to_decimal(body['items']),
            'totalAmount': Decimal(str(body['totalAmount'])),
            'status': 'SUBMITTED',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Stores it in DynamoDB
        table = dynamodb.Table(os.environ['ORDERS_TABLE'])
        table.put_item(Item=order)
        
        #call helper to revert/convert 
        order_for_stepfunctions = convert_decimals_to_float(order)

        # Start the order flow state machine
        stepfunctions.start_execution(
            stateMachineArn=os.environ.get('STATE_MACHINE_ARN'),
            name=f"order-{order_id}",
            input=json.dumps(order_for_stepfunctions)
        )
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'orderId': order_id,
                'status': 'SUBMITTED',
                'message': 'Order submitted successfully'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }