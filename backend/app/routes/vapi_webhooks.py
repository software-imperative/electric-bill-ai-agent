from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.call import VapiWebhookEvent
from app.services.vapi_service import VapiService
from app.services.twilio_service import TwilioService
from app.services.bill_service import BillService
from app.services.payment_service import PaymentService
from app.models.call_log import CallLog, CallStatus, CallOutcome
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/webhooks/vapi", tags=["VAPI Webhooks"])

vapi_service = VapiService()
twilio_service = TwilioService()


@router.post("/events")
async def handle_vapi_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle incoming webhooks from VAPI
    
    This endpoint receives various events from VAPI including:
    - Call status updates
    - Transcripts
    - Function calls
    - End of call reports
    """
    try:
        event_data = await request.json()
        message_type = event_data.get('message', {}).get('type') or event_data.get('type', '')
        logger.info(f"Received VAPI webhook: {message_type}")
        
        # Log full event data for debugging tool-calls
        if message_type == "tool-calls":
            logger.info(f"Tool-calls event data: {event_data}")
        
        # Process the webhook event
        processed = vapi_service.process_webhook_event(event_data)
        
        message_type = processed.get("type")
        call_id = processed.get("call_id")
        
        # Log call_id extraction for debugging
        if message_type == "tool-calls":
            logger.info(f"Extracted call_id: {call_id} from event")
        
        # Find call log
        call_log = None
        if call_id:
            call_log = db.query(CallLog).filter(CallLog.vapi_call_id == call_id).first()
        
        # If call_log not found but we have call_id, log for debugging
        if not call_log and call_id:
            logger.warning(f"Call log not found for call_id: {call_id}")
            # Try to find latest call log as fallback (for tool-calls that might not have call_id)
            call_log = db.query(CallLog).order_by(CallLog.created_at.desc()).first()
            if call_log:
                logger.info(f"Using latest call log as fallback: {call_log.id}, vapi_call_id: {call_log.vapi_call_id}")
        
        # For tool-calls without call_id, try to use latest call log
        if not call_log and message_type == "tool-calls":
            call_log = db.query(CallLog).order_by(CallLog.created_at.desc()).first()
            if call_log:
                logger.info(f"Using latest call log for tool-calls: {call_log.id}, vapi_call_id: {call_log.vapi_call_id}")
        
        # Some events don't require call_log (like assistant.started)
        if not call_log and message_type in ["status-update", "end-of-call-report", "function-call", "tool-calls", "transcript"]:
            logger.warning(f"Call log not found for call_id: {call_id}, event: {message_type}")
            # For tool-calls, log the full event to debug
            if message_type == "tool-calls":
                logger.error(f"Full tool-calls event: {event_data}")
            return {"status": "ok", "message": "Call log not found, skipping event"}
        
        # Handle different event types only if we have a call_log
        if call_log:
            if message_type == "status-update":
                await handle_status_update(db, call_log, processed)
            
            elif message_type == "transcript":
                await handle_transcript(db, call_log, processed)
            
            elif message_type in ["function-call", "tool-calls"]:
                result = await handle_function_call(db, call_log, processed)
                # Return function result if needed (for VAPI function responses)
                if result and message_type == "tool-calls":
                    db.commit()
                    return result
            
            elif message_type == "end-of-call-report":
                await handle_end_of_call(db, call_log, processed)
            
            db.commit()
        
        return {"status": "ok", "message": "Webhook processed successfully"}
        
    except Exception as e:
        logger.error(f"Error processing VAPI webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def handle_status_update(db: Session, call_log: CallLog, processed: dict):
    """Handle call status updates"""
    status = processed.get("status", "").lower()
    
    status_mapping = {
        "queued": CallStatus.INITIATED,
        "ringing": CallStatus.RINGING,
        "in-progress": CallStatus.IN_PROGRESS,
        "completed": CallStatus.COMPLETED,
        "failed": CallStatus.FAILED,
        "no-answer": CallStatus.NO_ANSWER,
        "busy": CallStatus.BUSY
    }
    
    if status in status_mapping:
        call_log.status = status_mapping[status]
        
        if status == "in-progress" and not call_log.started_at:
            call_log.started_at = datetime.utcnow()


async def handle_transcript(db: Session, call_log: CallLog, processed: dict):
    """Handle transcript updates"""
    transcript_text = processed.get("transcript", "")
    role = processed.get("role", "")
    
    if call_log.transcript:
        call_log.transcript += f"\n{role}: {transcript_text}"
    else:
        call_log.transcript = f"{role}: {transcript_text}"


async def handle_function_call(db: Session, call_log: CallLog, processed: dict):
    """Handle function calls from VAPI assistant"""
    function_name = processed.get("function_name")
    parameters = processed.get("function_parameters", {})
    
    logger.info(f"Function called: {function_name} with params: {parameters}")
    
    # Handle send_payment_link function
    if function_name == "send_payment_link":
        bill = BillService.get_bill(db, call_log.bill_id)
        
        if not bill:
            logger.error(f"Bill not found for call_log.bill_id: {call_log.bill_id}")
            return {"success": False, "error": "Bill not found"}
        
        logger.info(f"Sending SMS to {bill.customer_phone} for bill {bill.bill_number}")
        logger.info(f"Payment link: {bill.payment_link}")
        logger.info(f"Bill amount: {bill.bill_amount}, Due date: {bill.due_date}")
        
        try:
            result = twilio_service.send_payment_link(
                to_number=bill.customer_phone,
                customer_name=bill.customer_name,
                bill_amount=bill.bill_amount,
                due_date=bill.due_date.strftime("%d-%m-%Y"),
                payment_link=bill.payment_link
            )
            
            logger.info(f"SMS send result: {result}")
            
            if result.get("success"):
                call_log.sms_sent = 1
                call_log.sms_sid = result.get("sid")
                logger.info(f"✅ Payment link sent successfully to {bill.customer_phone}, SMS SID: {result.get('sid')}")
                return {"success": True, "message": "SMS sent successfully", "sid": result.get("sid")}
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"❌ Failed to send SMS: {error_msg}")
                call_log.error_message = error_msg
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Error sending SMS: {str(e)}"
            logger.error(f"❌ {error_msg}", exc_info=True)
            call_log.error_message = error_msg
            return {"success": False, "error": error_msg}
    
    # Handle confirm_payment function
    elif function_name == "confirm_payment":
        call_log.outcome = CallOutcome.PAYMENT_CONFIRMED
        return {"success": True, "message": "Payment confirmed"}
    
    # Handle customer_disputed function
    elif function_name == "customer_disputed":
        call_log.outcome = CallOutcome.CUSTOMER_DISPUTED
        
        # Add note to bill
        bill = BillService.get_bill(db, call_log.bill_id)
        if bill:
            dispute_reason = parameters.get("reason", "No reason provided")
            bill.notes = f"Customer disputed: {dispute_reason}"
        
        return {"success": True, "message": "Dispute recorded"}
    
    return {"success": True, "message": "Function processed"}


async def handle_end_of_call(db: Session, call_log: CallLog, processed: dict):
    """Handle end of call report"""
    call_log.status = CallStatus.COMPLETED
    call_log.ended_at = datetime.utcnow()
    call_log.duration = processed.get("duration")
    call_log.recording_url = processed.get("recording_url")
    
    # Calculate duration if not provided
    if not call_log.duration and call_log.started_at:
        duration_delta = call_log.ended_at - call_log.started_at
        call_log.duration = int(duration_delta.total_seconds())
    
    # Update bill status
    bill = BillService.get_bill(db, call_log.bill_id)
    if bill:
        BillService.mark_bill_called(db, bill.id)
        
        # If payment was confirmed during call, update accordingly
        if call_log.outcome == CallOutcome.PAYMENT_CONFIRMED:
            logger.info(f"Payment confirmed for bill {bill.bill_number}")
