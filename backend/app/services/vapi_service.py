import httpx
from typing import Optional, Dict, Any
from app.config import get_settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


def get_time_of_day() -> str:
    """Get time of day greeting based on current hour"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "evening"  # Default to evening for night/early morning


class VapiService:
    """Service for interacting with VAPI.ai API"""
    
    def __init__(self):
        self.api_key = settings.vapi_api_key
        self.api_url = settings.vapi_api_url
        self.assistant_id = settings.vapi_assistant_id
        self.phone_number_id = settings.vapi_phone_number_id
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def initiate_call(
        self,
        phone_number: str,
        bill_data: Dict[str, Any],
        assistant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initiate an outbound call via VAPI
        
        Args:
            phone_number: Customer phone number
            bill_data: Bill information to pass to the assistant
            assistant_id: Optional custom assistant ID
            
        Returns:
            Call response from VAPI API
        """
        try:
            # Get time of day for greeting
            time_of_day = get_time_of_day()
            
            # Ensure all required variables are present and not None
            customer_name = bill_data.get("customer_name") or ""
            bill_number = bill_data.get("bill_number") or ""
            bill_amount = bill_data.get("bill_amount") or 0
            due_date = bill_data.get("due_date") or ""
            
            # Validate required fields
            if not customer_name:
                logger.warning(f"Customer name is empty for phone {phone_number}")
            if not bill_number:
                logger.warning(f"Bill number is empty for phone {phone_number}")
            
            # Log for debugging
            logger.info(f"Initiating call with variables - customerName: '{customer_name}', billNumber: '{bill_number}', timeOfDay: '{time_of_day}'")
            logger.info(f"Full bill_data: {bill_data}")
            
            payload = {
                "assistantId": assistant_id or self.assistant_id,
                "phoneNumberId": self.phone_number_id,
                "customer": {
                    "number": phone_number
                },
                "assistantOverrides": {
                    "variableValues": {
                        "customerName": str(customer_name) if customer_name else "",
                        "billAmount": str(bill_amount) if bill_amount else "0",
                        "dueDate": str(due_date) if due_date else "",
                        "consumerNumber": str(bill_data.get("consumer_number", "")),
                        "billNumber": str(bill_number) if bill_number else "",
                        "paymentLink": str(bill_data.get("payment_link", "")),
                        "timeOfDay": str(time_of_day)
                    }
                }
            }
            
            logger.info(f"VAPI Payload variableValues: {payload['assistantOverrides']['variableValues']}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/call/phone",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"VAPI API error: {str(e)}")
            raise Exception(f"Failed to initiate call: {str(e)}")
    
    async def get_call_details(self, call_id: str) -> Dict[str, Any]:
        """Get details of a specific call"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/call/{call_id}",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to get call details: {str(e)}")
            raise Exception(f"Failed to get call details: {str(e)}")
    
    async def end_call(self, call_id: str) -> Dict[str, Any]:
        """End an ongoing call"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/call/{call_id}/end",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to end call: {str(e)}")
            raise Exception(f"Failed to end call: {str(e)}")
    
    def process_webhook_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming webhook event from VAPI
        
        Returns:
            Processed event data with extracted information
        """
        message = event_data.get("message", {})
        message_type = message.get("type", "")
        
        # Extract call_id from multiple possible locations
        call_id = (
            event_data.get("call", {}).get("id") or
            event_data.get("callId") or
            event_data.get("call_id")
        )
        
        processed = {
            "type": message_type,
            "call_id": call_id,
            "status": message.get("status"),
            "timestamp": event_data.get("timestamp", datetime.utcnow().isoformat())
        }
        
        # Extract transcript if available
        if message_type == "transcript":
            processed["transcript"] = message.get("transcript", "")
            processed["role"] = message.get("role", "")
        
        # Extract function call if available (handle both function-call and tool-calls)
        if message_type in ["function-call", "tool-calls"]:
            # Try different possible structures
            function_call = (
                message.get("functionCall") or
                message.get("toolCall") or
                message.get("toolCalls", [{}])[0] if isinstance(message.get("toolCalls"), list) else {}
            )
            
            processed["function_name"] = (
                function_call.get("name") or
                function_call.get("function", {}).get("name") or
                message.get("name")
            )
            processed["function_parameters"] = (
                function_call.get("parameters") or
                function_call.get("arguments") or
                message.get("parameters") or
                {}
            )
        
        # Extract call status updates
        if message_type in ["status-update", "end-of-call-report"]:
            processed["duration"] = event_data.get("call", {}).get("duration")
            processed["ended_reason"] = event_data.get("call", {}).get("endedReason")
            processed["recording_url"] = event_data.get("artifact", {}).get("recordingUrl")
            processed["transcript_url"] = event_data.get("artifact", {}).get("transcript")
        
        return processed
