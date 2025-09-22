import json
import random
import time

def lambda_handler(event, context):
    """Simulates payment processing, since I can't actually do this realistically without a payment authority/provider"""
    
    order = event
    
    # Simulate transaction time by sleeping
    time.sleep(1)
    
    # Simulate payment processing (with a 90% success rate, to make it akin to realism)
    if random.random() < 0.9:
        # Payment successful
        order['paymentId'] = f"pay_{context.aws_request_id[:8]}"
        order['paymentStatus'] = 'COMPLETED'
        order['status'] = 'PAYMENT_PROCESSED'
        
        return order
    else:
        # Payment failed
        raise Exception("Payment processing failed: Insufficient funds")