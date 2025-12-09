from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # VAPI Configuration
    vapi_api_key: str
    vapi_phone_number_id: str
    vapi_assistant_id: str
    vapi_api_url: str = "https://api.vapi.ai"
    
    # Twilio Configuration
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    
    # Database Configuration
    database_url: str = "sqlite:///./bills.db"
    
    # Application Configuration
    secret_key: str = "change-this-secret-key-in-production"
    api_base_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    debug: bool = True
    
    # Payment Gateway Configuration
    payment_gateway_url: str = ""
    payment_gateway_key: str = ""
    payment_callback_url: str = ""
    
    # SMS Templates
    sms_payment_link_template: str = "Dear customer, your bill of Rs.{amount} is due on {due_date}. Pay now: {payment_link}"
    sms_reminder_template: str = "Reminder: Your bill of Rs.{amount} is overdue. Please pay immediately: {payment_link}"
    sms_thank_you_template: str = "Thank you for your payment of Rs.{amount}. Your payment has been received successfully."
    
    # Call Configuration
    max_call_duration: int = 300
    call_retry_attempts: int = 3
    reminder_interval_hours: int = 24
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
