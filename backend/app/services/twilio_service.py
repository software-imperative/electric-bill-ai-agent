from twilio.rest import Client
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class TwilioService:
    """Service for sending SMS via Twilio"""
    
    def __init__(self):
        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token
        self.phone_number = settings.twilio_phone_number
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_sms(self, to_number: str, message: str) -> dict:
        """
        Send SMS to a phone number
        
        Args:
            to_number: Recipient phone number
            message: SMS message content
            
        Returns:
            Message SID and status
        """
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            
            logger.info(f"SMS sent to {to_number}, SID: {message_obj.sid}")
            
            return {
                "success": True,
                "sid": message_obj.sid,
                "status": message_obj.status,
                "to": to_number
            }
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {to_number}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "to": to_number
            }
    
    def send_payment_link(
        self,
        to_number: str,
        customer_name: str,
        bill_amount: float,
        due_date: str,
        payment_link: str
    ) -> dict:
        """
        Send payment link SMS to customer
        
        Args:
            to_number: Customer phone number
            customer_name: Customer name
            bill_amount: Bill amount
            due_date: Due date
            payment_link: Payment URL
            
        Returns:
            SMS send result
        """
        message = settings.sms_payment_link_template.format(
            amount=bill_amount,
            due_date=due_date,
            payment_link=payment_link
        )
        
        return self.send_sms(to_number, message)
    
    def send_reminder(
        self,
        to_number: str,
        bill_amount: float,
        payment_link: str
    ) -> dict:
        """
        Send payment reminder SMS
        
        Args:
            to_number: Customer phone number
            bill_amount: Bill amount
            payment_link: Payment URL
            
        Returns:
            SMS send result
        """
        message = settings.sms_reminder_template.format(
            amount=bill_amount,
            payment_link=payment_link
        )
        
        return self.send_sms(to_number, message)
    
    def send_thank_you(
        self,
        to_number: str,
        bill_amount: float
    ) -> dict:
        """
        Send thank you SMS after payment
        
        Args:
            to_number: Customer phone number
            bill_amount: Paid amount
            
        Returns:
            SMS send result
        """
        message = settings.sms_thank_you_template.format(
            amount=bill_amount
        )
        
        return self.send_sms(to_number, message)
    
    def get_message_status(self, message_sid: str) -> dict:
        """
        Get status of a sent message
        
        Args:
            message_sid: Twilio message SID
            
        Returns:
            Message status information
        """
        try:
            message = self.client.messages(message_sid).fetch()
            
            return {
                "success": True,
                "sid": message.sid,
                "status": message.status,
                "to": message.to,
                "error_code": message.error_code,
                "error_message": message.error_message
            }
            
        except Exception as e:
            logger.error(f"Failed to get message status for {message_sid}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
