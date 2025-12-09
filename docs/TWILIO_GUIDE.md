# Twilio Setup Guide

This guide will help you set up Twilio for sending SMS payment links in the Adani Bill Collection AI Agent.

## Prerequisites

- Twilio account ([Sign up here](https://www.twilio.com/try-twilio))
- Credit card for verification (Twilio offers free trial credits)

## Step 1: Create a Twilio Account

1. Go to [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up with your email
3. Verify your email address
4. Complete phone verification
5. Answer the onboarding questions

## Step 2: Get Your Account Credentials

1. After logging in, go to the **Console Dashboard**
2. You'll see your credentials:
   - **Account SID**: Your unique account identifier
   - **Auth Token**: Your authentication token (click to reveal)

3. Copy these and add to your `.env` file:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   ```

## Step 3: Get a Phone Number

### For Trial Account:
1. Twilio provides a trial phone number automatically
2. Go to **Phone Numbers** → **Manage** → **Active Numbers**
3. You'll see your trial number listed

### For Production (Paid Account):
1. Go to **Phone Numbers** → **Buy a Number**
2. Select **India** as the country
3. Choose capabilities:
   - ✅ SMS
   - ✅ Voice (if needed for VAPI)
4. Search for available numbers
5. Purchase a number

4. Copy the phone number and add to `.env`:
   ```
   TWILIO_PHONE_NUMBER=+91XXXXXXXXXX
   ```

## Step 4: Verify Phone Numbers (Trial Account Only)

If using a trial account, you need to verify recipient phone numbers:

1. Go to **Phone Numbers** → **Verified Caller IDs**
2. Click **Add a new number**
3. Enter the phone number to verify
4. Complete the verification process (SMS or call)
5. Repeat for all test numbers

**Note**: Production accounts can send to any number without verification.

## Step 5: Configure SMS Settings

1. Go to **Messaging** → **Settings** → **Geo Permissions**
2. Ensure **India** is enabled for SMS
3. Configure other countries if needed

## Step 6: Set Up Messaging Service (Optional but Recommended)

For better deliverability and features:

1. Go to **Messaging** → **Services**
2. Click **Create Messaging Service**
3. Give it a name: "Adani Bill Collection"
4. Select use case: **Notifications, Outbound Only**
5. Add your phone number to the service
6. Complete setup

## Step 7: Configure SMS Templates

### Payment Link SMS Template
```
Dear {name}, your Adani electricity bill of Rs.{amount} is due on {due_date}. Pay now: {payment_link}
```

### Reminder SMS Template
```
Reminder: Your Adani electricity bill of Rs.{amount} is overdue. Please pay immediately: {payment_link}
```

### Thank You SMS Template
```
Thank you for your payment of Rs.{amount}. Your Adani electricity bill has been received successfully.
```

These templates are already configured in your `.env` file and can be customized.

## Step 8: Test SMS Sending

Test your Twilio integration:

```python
from twilio.rest import Client

account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

message = client.messages.create(
    body='Test message from Adani Bill Collection',
    from_='+91XXXXXXXXXX',  # Your Twilio number
    to='+91YYYYYYYYYY'      # Verified number (for trial)
)

print(f"Message SID: {message.sid}")
```

## Step 9: Monitor SMS Delivery

1. Go to **Monitor** → **Logs** → **Messaging**
2. View all sent messages
3. Check delivery status:
   - **Queued**: Message is queued
   - **Sent**: Sent to carrier
   - **Delivered**: Successfully delivered
   - **Failed**: Delivery failed
   - **Undelivered**: Could not be delivered

## Step 10: Set Up Webhooks (Optional)

For delivery status updates:

1. Go to **Phone Numbers** → **Active Numbers** → Select your number
2. Scroll to **Messaging**
3. Set **Status Callback URL**:
   ```
   https://your-domain.com/api/webhooks/twilio/status
   ```
4. This will notify your backend of delivery status

## Important Considerations

### Trial Account Limitations
- Can only send to verified numbers
- Messages include "Sent from a Twilio trial account" prefix
- Limited free credits (~$15 USD)

### Production Account Benefits
- Send to any number
- No trial message prefix
- Higher sending limits
- Better deliverability

### Pricing (India)
- **SMS**: ~₹0.50 - ₹1.00 per message
- **Phone Number**: ~₹1,000/month
- Check current pricing: [Twilio Pricing](https://www.twilio.com/sms/pricing/in)

### Compliance
- Follow TRAI regulations for commercial SMS in India
- Register your sender ID if needed
- Include opt-out instructions
- Maintain DND (Do Not Disturb) registry compliance

### Best Practices

1. **Message Length**: Keep under 160 characters to avoid multi-part messages
2. **Timing**: Send between 9 AM - 9 PM to avoid disturbing customers
3. **Personalization**: Always include customer name and bill details
4. **Clear CTAs**: Make payment links prominent and easy to click
5. **Error Handling**: Implement retry logic for failed messages

### Rate Limits
- Trial: 1 message per second
- Production: Higher limits based on account type
- Implement queuing for bulk SMS

## Troubleshooting

### SMS Not Delivered
- Check phone number format (+91XXXXXXXXXX)
- Verify number is not on DND list
- Check Twilio account balance
- Review error logs in Twilio console

### "Unverified Number" Error
- Verify the recipient number in Twilio console
- Or upgrade to a paid account

### High Costs
- Monitor usage in Twilio console
- Set up usage alerts
- Implement SMS deduplication

### Poor Deliverability
- Use a Messaging Service
- Register sender ID
- Avoid spam trigger words
- Keep messages concise

## Security Best Practices

1. **Never commit credentials**: Keep `.env` file out of version control
2. **Rotate tokens**: Regularly update auth tokens
3. **Use environment variables**: Don't hardcode credentials
4. **Monitor usage**: Set up alerts for unusual activity
5. **Restrict IP access**: Configure IP whitelist in Twilio console

## Upgrading to Production

When ready for production:

1. Add payment method to Twilio account
2. Purchase a dedicated phone number
3. Remove trial account limitations
4. Set up auto-recharge to avoid service interruption
5. Configure usage alerts
6. Consider purchasing multiple numbers for load distribution

## Integration with VAPI

For voice calls via VAPI:
1. VAPI can use your Twilio credentials
2. Configure in VAPI dashboard under Transport settings
3. This allows VAPI to make calls using your Twilio number

## Next Steps

After setup:
1. Test SMS sending with sample bills
2. Monitor delivery rates
3. Optimize message templates based on response
4. Scale up gradually

For more information:
- [Twilio Documentation](https://www.twilio.com/docs)
- [Twilio SMS Best Practices](https://www.twilio.com/docs/sms/best-practices)
- [India SMS Guidelines](https://www.twilio.com/docs/sms/india)
