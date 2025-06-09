/**
 * Order Management Service Class
 * 
 * This class provides order management functionality for Agentforce agents.
 * It demonstrates how to create custom Apex classes for order-related agent actions.
 * Note: This example returns mock data for demonstration purposes.
 */
public with sharing class OrderManagementService {
    
    /**
     * Get order information by order ID
     * Note: Returns Order Response
     */
    @InvocableMethod(label='Get Order Info' description='Retrieves order information by ID')
    public static List<OrderResponse> getOrderInfo(List<OrderRequest> requests) {
        List<OrderResponse> responses = new List<OrderResponse>();
        
        for (OrderRequest request : requests) {
            OrderResponse response = new OrderResponse();
            response.status = 'success';
            response.orderDetails = 'Order #' + request.orderId + ': 2 items, Status: Processing';
            responses.add(response);
        }
        
        return responses;
    }
    
    // Request class for order info
    public class OrderRequest {
        @InvocableVariable(required=true description='Order ID to retrieve')
        public String orderId;
        
        @InvocableVariable(required=true description='Customer ID for verification')
        public String customerId;
    }
    
    // Response class matching Action outputs exactly
    public class OrderResponse {
        @InvocableVariable(description='Status of the order info retrieval')
        public String status;
        
        @InvocableVariable(description='Details of the order')
        public String orderDetails;
    }
} 