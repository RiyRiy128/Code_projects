import json
import random

def lambda_handler(event, context):
    """Updates inventory for ordered items"""
    
    order = event
    
    # Simulate inventory updates
    inventory_updates = []
    
    for item in order['items']:
        product_id = item['productId']
        quantity = int(item['quantity'])
        
        # Simulate checking inventory with a random probability
        if random.random() < 0.95:
            inventory_updates.append({
                'productId': product_id,
                'quantityReserved': quantity,
                'status': 'RESERVED'
            })
        else:
            # Insufficient inventory
            raise Exception(f"Insufficient inventory for product {product_id}")
    
    order['inventoryUpdates'] = inventory_updates
    order['status'] = 'INVENTORY_UPDATED'
    
    return order