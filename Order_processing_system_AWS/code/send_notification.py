import json
from datetime import datetime

def lambda_handler(event, context):
    """Sends order confirmation notification"""
    
    order = event
    
    # Simulate sending email/SMS notification
    notification = {
        'type': 'ORDER_CONFIRMATION',
        'customerId': order['customerId'],
        'orderId': order['orderId'],
        'message': f"Your order {order['orderId']} has been confirmed and is being processed.",
        'sentAt': datetime.utcnow().isoformat()
    }
    
    #The real implementation would most probably use a combination of SNS/SES but I don't do that here since it would involve setting up actual contact points to integrate
    
    print(f"Notification sent: {json.dumps(notification)}")
    
    order['notification'] = notification
    order['status'] = 'COMPLETED'
    
    return order