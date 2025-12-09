# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication. For production, implement JWT or API key authentication.

---

## Bills API

### Create Bill
Create a new electricity bill.

**Endpoint:** `POST /api/bills/`

**Request Body:**
```json
{
  "customer_name": "Rajesh Kumar",
  "customer_phone": "+919876543210",
  "customer_email": "rajesh@example.com",
  "consumer_number": "CONS12345",
  "bill_number": "BILL2024001",
  "bill_amount": 2500.50,
  "due_date": "2024-12-31T00:00:00Z",
  "billing_period": "December 2024"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "customer_name": "Rajesh Kumar",
  "customer_phone": "+919876543210",
  "bill_number": "BILL2024001",
  "bill_amount": 2500.50,
  "status": "pending",
  "payment_link": "https://payment-gateway.com/pay/abc123",
  "created_at": "2024-12-08T10:00:00Z"
}
```

---

### Get All Bills
Retrieve list of bills with optional filtering.

**Endpoint:** `GET /api/bills/`

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)
- `status` (string): Filter by status (pending, called, paid, overdue)

**Example:**
```
GET /api/bills/?status=pending&limit=50
```

**Response:** `200 OK`
```json
{
  "total": 150,
  "bills": [...]
}
```

---

### Get Bill by ID
Retrieve a specific bill.

**Endpoint:** `GET /api/bills/{bill_id}`

**Response:** `200 OK`
```json
{
  "id": 1,
  "customer_name": "Rajesh Kumar",
  ...
}
```

---

### Update Bill
Update bill information.

**Endpoint:** `PUT /api/bills/{bill_id}`

**Request Body:**
```json
{
  "status": "paid",
  "notes": "Payment received via UPI"
}
```

**Response:** `200 OK`

---

### Delete Bill
Delete a bill.

**Endpoint:** `DELETE /api/bills/{bill_id}`

**Response:** `200 OK`
```json
{
  "message": "Bill deleted successfully"
}
```

---

### Initiate Call
Trigger AI voice call for a bill.

**Endpoint:** `POST /api/bills/{bill_id}/call`

**Response:** `200 OK`
```json
{
  "message": "Call initiated successfully",
  "call_id": "vapi_call_123",
  "bill_id": 1
}
```

---

### Get Pending Bills
Get all bills pending for calls.

**Endpoint:** `GET /api/bills/pending/list`

**Response:** `200 OK`
```json
{
  "total": 25,
  "bills": [...]
}
```

---

### Get Overdue Bills
Get all overdue bills.

**Endpoint:** `GET /api/bills/overdue/list`

**Response:** `200 OK`
```json
{
  "total": 10,
  "bills": [...]
}
```

---

## Call Logs API

### Get Call Logs
Retrieve call logs with optional filtering.

**Endpoint:** `GET /api/calls/`

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Records per page
- `bill_id` (int): Filter by bill ID
- `status` (string): Filter by call status

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "bill_id": 1,
    "vapi_call_id": "vapi_123",
    "customer_phone": "+919876543210",
    "status": "completed",
    "outcome": "payment_confirmed",
    "duration": 180,
    "transcript": "...",
    "created_at": "2024-12-08T10:00:00Z"
  }
]
```

---

### Get Call Log by ID
Retrieve specific call log.

**Endpoint:** `GET /api/calls/{call_log_id}`

**Response:** `200 OK`

---

### Get Call Log by VAPI ID
Retrieve call log by VAPI call ID.

**Endpoint:** `GET /api/calls/vapi/{vapi_call_id}`

**Response:** `200 OK`

---

## Payments API

### Payment Callback
Handle payment gateway callbacks.

**Endpoint:** `POST /api/payments/callback`

**Request Body:**
```json
{
  "payment_id": "PAY123",
  "transaction_id": "TXN456",
  "status": "success",
  "amount": 2500.50,
  "payment_method": "upi",
  "gateway_response": {}
}
```

**Response:** `200 OK`
```json
{
  "status": "success",
  "message": "Payment callback processed",
  "payment_status": "completed"
}
```

---

### Get Payment by ID
Retrieve payment details.

**Endpoint:** `GET /api/payments/{payment_id}`

**Response:** `200 OK`

---

### Get Payment by Bill
Get payment for a specific bill.

**Endpoint:** `GET /api/payments/bill/{bill_id}`

**Response:** `200 OK`

---

## VAPI Webhooks

### VAPI Events Webhook
Receive events from VAPI.

**Endpoint:** `POST /api/webhooks/vapi/events`

**Request Body:** (Sent by VAPI)
```json
{
  "message": {
    "type": "status-update",
    "status": "in-progress"
  },
  "call": {
    "id": "vapi_call_123"
  }
}
```

**Event Types:**
- `status-update`: Call status changes
- `transcript`: Real-time transcript
- `function-call`: AI called a function
- `end-of-call-report`: Call completed

**Response:** `200 OK`
```json
{
  "status": "ok",
  "message": "Webhook processed successfully"
}
```

---

## Health Check

### Health Check
Check API health status.

**Endpoint:** `GET /health`

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "bill-collection-ai-agent"
}
```

---

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Error Response Format

```json
{
  "detail": "Error message description"
}
```

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints directly.

Alternative documentation: `http://localhost:8000/redoc`
