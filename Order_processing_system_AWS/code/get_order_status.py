import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # Gets the order ID from the event path parameters
        order_id = event['pathParameters']['orderId']
        
        # Go and check the DDB table for the order
        table = dynamodb.Table(os.environ['ORDERS_TABLE'])
        response = table.get_item(Key={'orderId': order_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'error': 'Order not found'
                })
            }
        
        order = response['Item']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'orderId': order['orderId'],
                'status': order['status'],
                'customerId': order['customerId'],
                'totalAmount': str(order['totalAmount']),
                'timestamp': order['timestamp']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }