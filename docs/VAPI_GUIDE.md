# VAPI Configuration Guide

This guide will help you set up your VAPI.ai assistant for the Adani Bill Collection AI Agent.

## Prerequisites

- VAPI.ai account ([Sign up here](https://vapi.ai))
- Twilio account for phone numbers
- Backend server URL (for webhooks)

## Step 1: Create a VAPI Account

1. Go to [https://vapi.ai](https://vapi.ai)
2. Sign up for an account
3. Complete the onboarding process

## Step 2: Get Your API Key

1. Navigate to **Settings** → **API Keys**
2. Click **Create New API Key**
3. Copy the API key and save it securely
4. Add it to your `.env` file:
   ```
   VAPI_API_KEY=your_api_key_here
   ```

## Step 3: Purchase a Phone Number

1. Go to **Phone Numbers** section
2. Click **Buy Phone Number**
3. Select your country (India for Adani)
4. Choose a phone number
5. Complete the purchase
6. Copy the Phone Number ID and add to `.env`:
   ```
   VAPI_PHONE_NUMBER_ID=your_phone_number_id
   ```

## Step 4: Create the Assistant

### Option A: Via Dashboard (Recommended for First Time)

1. Navigate to **Assistants** → **Create Assistant**
2. Fill in the basic details:
   - **Name**: Adani Bill Collection Assistant
   - **Model**: GPT-4 (recommended) or GPT-3.5-turbo
   - **Voice Provider**: ElevenLabs or PlayHT
   - **Voice**: Choose a professional, clear voice (e.g., "Rachel" for female or "Adam" for male)

3. **System Prompt**: Copy the content from `vapi_config/system_prompt.txt`

4. **First Message**: Copy the content from `vapi_config/first_message.txt`

5. **Model Settings**:
   - Temperature: 0.7
   - Max Tokens: 250
   - Enable Emotion Recognition: Yes

6. **Voice Settings**:
   - Stability: 0.5
   - Similarity Boost: 0.75
   - Speed: 1.0

7. **Advanced Settings**:
   - Recording Enabled: Yes
   - Max Duration: 300 seconds (5 minutes)
   - Silence Timeout: 30 seconds
   - Background Sound: Office
   - Background Denoising: Yes

### Option B: Via API

Use the configuration in `vapi_config/assistant_config.json` to create the assistant programmatically:

```bash
curl -X POST https://api.vapi.ai/assistant \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @vapi_config/assistant_config.json
```

## Step 5: Configure Functions

1. In the Assistant settings, go to **Functions**
2. Add the following functions from `vapi_config/functions.json`:

### Function 1: send_payment_link
- **Name**: `send_payment_link`
- **Description**: Send SMS with payment link to customer
- **Parameters**: See `functions.json`

### Function 2: confirm_payment
- **Name**: `confirm_payment`
- **Description**: Mark customer payment commitment
- **Parameters**: See `functions.json`

### Function 3: customer_disputed
- **Name**: `customer_disputed`
- **Description**: Record bill dispute
- **Parameters**: See `functions.json`

### Function 4: schedule_callback
- **Name**: `schedule_callback`
- **Description**: Schedule callback request
- **Parameters**: See `functions.json`

## Step 6: Configure Webhooks

1. In Assistant settings, go to **Server URL**
2. Enter your backend webhook URL:
   ```
   https://your-domain.com/api/webhooks/vapi/events
   ```
3. Generate and save a webhook secret
4. Add to `.env`:
   ```
   VAPI_WEBHOOK_SECRET=your_webhook_secret
   ```

## Step 7: Configure Variables

Set up the following variables in your assistant:

- `customerName`: Customer's name
- `billAmount`: Bill amount in Rupees
- `dueDate`: Bill due date
- `consumerNumber`: Consumer number
- `billNumber`: Bill reference number
- `paymentLink`: Payment URL
- `timeOfDay`: Time of day greeting (morning/afternoon/evening)

These will be populated dynamically when initiating calls from the backend.

## Step 8: Test the Assistant

1. Go to **Assistants** → Select your assistant
2. Click **Test** button
3. Make a test call to verify:
   - Voice quality
   - System prompt behavior
   - Function calling works
   - Variables are populated correctly

## Step 9: Save Assistant ID

1. After creating the assistant, copy the Assistant ID
2. Add to `.env`:
   ```
   VAPI_ASSISTANT_ID=your_assistant_id
   ```

## Step 10: Configure Transport (Twilio Integration)

1. In Assistant settings, go to **Transport**
2. Select **Twilio**
3. Enter your Twilio credentials:
   - Account SID
   - Auth Token
4. Enable call recording if needed

## Important Notes

### Voice Selection
- Choose a voice that sounds professional and clear
- Test with Indian phone numbers to ensure good quality
- Consider regional accents if targeting specific areas

### System Prompt Tips
- Keep the prompt focused on bill collection
- Include clear instructions for handling objections
- Specify when to use each function
- Maintain a polite and professional tone

### Function Calling
- Functions are called automatically by the AI based on conversation
- Ensure your backend webhook handles all function calls
- Test each function thoroughly

### Rate Limiting
- VAPI has rate limits based on your plan
- For production, consider upgrading to a higher tier
- Implement queuing in your backend for bulk calls

### Monitoring
- Use VAPI dashboard to monitor call quality
- Review call recordings regularly
- Analyze transcripts for improvement opportunities

## Troubleshooting

### Calls Not Connecting
- Verify phone number is active
- Check Twilio integration
- Ensure sufficient balance in VAPI account

### Functions Not Working
- Verify webhook URL is accessible
- Check webhook secret matches
- Review function definitions

### Poor Voice Quality
- Try different voice providers
- Adjust voice settings (stability, speed)
- Check internet connection quality

### Assistant Not Following Prompt
- Reduce temperature for more consistent behavior
- Make system prompt more specific
- Add more examples in the prompt

## Next Steps

After configuration:
1. Test with a few sample bills
2. Monitor call quality and outcomes
3. Adjust prompts based on results
4. Scale up gradually

For more information, visit [VAPI Documentation](https://docs.vapi.ai)
