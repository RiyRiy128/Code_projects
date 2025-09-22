import json

def lambda_handler(event, context):
    """Validates order data and customer information"""
    
    order = event
    
    # Validation checks list 
    errors = []
    
    if not order.get('customerId'):
        errors.append('Customer ID is required')
    
    if not order.get('items') or len(order['items']) == 0:
        errors.append('Order must contain at least one item')
    
    if not order.get('totalAmount') or float(order['totalAmount']) <= 0:
        errors.append('Total amount must be greater than 0')
    
    # Validates items and populates the errors list
    for item in order.get('items', []):
        if not item.get('productId'):
            errors.append('Product ID is required for all items')
        if not item.get('quantity') or int(item['quantity']) <= 0:
            errors.append('Quantity must be greater than 0')
        if not item.get('price') or float(item['price']) <= 0:
            errors.append('Price must be greater than 0')
    
    if errors:
        raise Exception(f"Validation failed: {', '.join(errors)}")
    
    # Adds a validation timestamp
    order['validatedAt'] = context.aws_request_id
    order['status'] = 'VALIDATED'
    
    return order