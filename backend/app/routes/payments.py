from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.payment import PaymentCallbackRequest, PaymentResponse
from app.services.payment_service import PaymentService
from app.services.bill_service import BillService
from app.services.twilio_service import TwilioService
from app.models.payment import PaymentStatus
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/payments", tags=["Payments"])

twilio_service = TwilioService()


@router.post("/callback")
async def payment_callback(
    callback_data: PaymentCallbackRequest,
    db: Session = Depends(get_db)
):
    """
    Handle payment gateway callback
    
    This endpoint receives payment status updates from the payment gateway
    """
    try:
        logger.info(f"Payment callback received: {callback_data.payment_id}")
        
        # Process the payment callback
        payment = PaymentService.process_payment_callback(
            db=db,
            payment_id=callback_data.payment_id,
            transaction_id=callback_data.transaction_id,
            status=callback_data.status,
            payment_method=callback_data.payment_method,
            gateway_response=str(callback_data.gateway_response) if callback_data.gateway_response else None
        )
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # If payment is completed, update bill and send thank you SMS
        if payment.status == PaymentStatus.COMPLETED:
            bill = BillService.mark_bill_paid(
                db=db,
                bill_id=payment.bill_id,
                payment_id=payment.payment_id,
                payment_date=payment.payment_date
            )
            
            if bill:
                # Send thank you SMS
                twilio_service.send_thank_you(
                    to_number=bill.customer_phone,
                    bill_amount=bill.bill_amount
                )
                
                logger.info(f"Bill {bill.bill_number} marked as paid")
        
        return {
            "status": "success",
            "message": "Payment callback processed",
            "payment_status": payment.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing payment callback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    """Get payment details by payment ID"""
    payment = PaymentService.get_payment(db, payment_id)
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return payment


@router.get("/bill/{bill_id}", response_model=PaymentResponse)
def get_payment_by_bill(bill_id: int, db: Session = Depends(get_db)):
    """Get payment details for a specific bill"""
    payment = PaymentService.get_payment_by_bill(db, bill_id)
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for this bill")
    
    return payment
