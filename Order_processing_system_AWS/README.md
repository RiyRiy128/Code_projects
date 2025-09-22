# Order Processing System

A serverless pseudo order processing system built with AWS Lambda, API Gateway, and Step Functions which essentially simulates real order flow to an extent

## Architecture

- **API Gateway**: REST endpoints for order submission and status checking
- **Lambda Functions**: Represents microservices for each processing step
- **Step Functions**: Orchestrates the order workflow
- **DynamoDB**: Stores order data

## Workflow

1. **Order Submission** → API Gateway receives order
2. **Validation** → Validates order data and customer info
3. **Payment Processing** → Processes payment (simulated)
4. **Inventory Update** → Updates product inventory
5. **Notification** → Sends confirmation to customer
6. **Error Handling** → Manages failures at any step

## Deployment

1. Install AWS SAM CLI
2. Configure AWS credentials
3. Run deployment:
   ```bash
   ./deploy.sh
   ```

## API Endpoints

### Submit sample Order
### do a curl request with the payload below
POST /orders
Content-Type: application/json

{
  "customerId": "cust_12345",
  "items": [
    {
      "productId": "prod_001",
      "name": "Product Name",
      "quantity": 2,
      "price": 99.99
    }
  ],
  "totalAmount": 199.98
}
### curl -v -X POST https://gateway_invoke_url/stage/orders -H "Content-Type:application/json" -d @test_order.json
or you may curl it with json payload instead

### Get the Order Status
GET /orders/{orderId}
curl -v https://gateway_invoke_url/stage/orders/order_id_here 


## Resources used

- Python 3.13
- AWS Lambda
- AWS API Gateway
- AWS Step Functions
- AWS DynamoDB
- AWS SAM (Serverless Application Model)/Cloudformation