# VAPI Assistant Creation Guide - Copy-Paste Ready

## 📋 Quick Reference for VAPI Dashboard

Use this guide to create your assistant directly on the VAPI dashboard.

---

## 1️⃣ FIRST MESSAGE

Copy and paste this into the "First Message" field:

```
Hello, good {{timeOfDay}}! This is Adani Electricity. Am I speaking with {{customerName}}?
```

**IMPORTANT:** The first message greets and asks for name confirmation. The AI will:
1. Wait for customer to confirm their name (say "yes")
2. Then ask: "I'm calling regarding bill number {{billNumber}}. Is this your bill number?"
3. Wait for bill number confirmation (say "yes")
4. Only after both confirmations, proceed with bill details

**Note:** The variables {{customerName}} and {{timeOfDay}} will be automatically populated when your backend initiates the call.

---

## 2️⃣ SYSTEM PROMPT

Copy and paste this into the "System Prompt" field (copy from `vapi_config/system_prompt.txt`):

**IMPORTANT:** The full system prompt is in `vapi_config/system_prompt.txt`. Copy the entire content from that file.

**Key Features:**
- ✅ Confirms bill number FIRST, then name
- ✅ Speaks amounts naturally (e.g., "two thousand five hundred rupees")
- ✅ Speaks dates naturally (e.g., "first of June, twenty twenty-five")
- ✅ Human-like conversation style
- ✅ Short, natural responses

**Quick Summary:**
The system prompt emphasizes:
1. **Confirmation First:** Ask for bill number confirmation, then name confirmation
2. **Natural Speech:** Speak amounts and dates like a human would
3. **Conversational:** Short responses, wait for customer replies
4. **Human-like:** Sound like talking to a friend, not a robot

---

## 3️⃣ FUNCTIONS / TOOLS

Add these 3 functions in the "Functions" section of VAPI dashboard:

### Function 1: send_payment_link

**Function Name:**
```
send_payment_link
```

**Description:**
```
Send SMS with payment link to the customer's phone number. Call this function when the customer agrees to receive the payment link.
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "customer_confirmed": {
      "type": "boolean",
      "description": "Whether the customer confirmed they want to receive the payment link"
    }
  },
  "required": ["customer_confirmed"]
}
```

---

### Function 2: confirm_payment

**Function Name:**
```
confirm_payment
```

**Description:**
```
Mark that the customer has confirmed they will make the payment. Call this when customer explicitly states they will pay.
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "payment_commitment": {
      "type": "string",
      "description": "Customer's commitment - immediate, today, tomorrow, or later",
      "enum": ["immediate", "today", "tomorrow", "later"]
    },
    "notes": {
      "type": "string",
      "description": "Any additional notes or comments from the customer"
    }
  },
  "required": ["payment_commitment"]
}
```

---

### Function 3: customer_disputed

**Function Name:**
```
customer_disputed
```

**Description:**
```
Record when customer disputes the bill amount or claims they already paid. Call this to flag the bill for investigation.
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "dispute_type": {
      "type": "string",
      "description": "Type of dispute",
      "enum": ["already_paid", "wrong_amount", "not_my_bill", "other"]
    },
    "reason": {
      "type": "string",
      "description": "Customer's explanation for the dispute"
    },
    "payment_reference": {
      "type": "string",
      "description": "Payment reference number if customer claims they already paid"
    }
  },
  "required": ["dispute_type", "reason"]
}
```

---

## 4️⃣ ASSISTANT SETTINGS

### Basic Settings
- **Assistant Name:** `Adani Bill Collection Assistant`
- **Language:** English (India)

### Model Settings
- **Provider:** OpenAI
- **Model:** `gpt-4` (recommended) or `gpt-3.5-turbo` (cost-effective)
- **Temperature:** `0.8` (increased for more natural, conversational responses)
- **Max Tokens:** `150` (reduced to encourage shorter, more natural responses)

### Voice Settings
- **Provider:** ElevenLabs (recommended) or PlayHT
- **Voice:** Choose a professional Indian voice like:
  - ElevenLabs: "Bella" or "Rachel" (female) / "Adam" or "Antoni" (male)
  - PlayHT: "Hindi Female" or "English (India) Female"
- **Stability:** `0.5`
- **Similarity Boost:** `0.75`
- **Speed:** `1.0`

### Advanced Settings
- **Recording Enabled:** ✅ Yes
- **End Call Function Enabled:** ✅ Yes
- **Silence Timeout:** `30` seconds
- **Max Call Duration:** `300` seconds (5 minutes)
- **Background Sound:** Office
- **Background Denoising:** ✅ Yes
- **Backchannel:** ✅ Yes (for natural "mm-hmm" responses)

---

## 5️⃣ SERVER URL (Webhook Configuration)

**Server URL:**
```
https://your-backend-domain.com/api/webhooks/vapi/events
https://8c8cb2ac7a45.ngrok-free.app/api/webhooks/vapi/events
```

**Important:** Replace `your-backend-domain.com` with your actual backend URL. For local testing with ngrok:
```
https://your-ngrok-url.ngrok.io/api/webhooks/vapi/events
```

**Server URL Secret:** Generate a random secret and add it to your `.env` file

---

## 6️⃣ VARIABLES TO SET

When creating the assistant, set up these variables (they'll be populated dynamically):

```json
{
  "customerName": "",
  "billAmount": "",
  "dueDate": "",
  "consumerNumber": "",
  "billNumber": "",
  "paymentLink": ""
}
```

---

## 7️⃣ STEP-BY-STEP CREATION ON VAPI DASHBOARD

1. **Login to VAPI Dashboard** → Go to Assistants
2. **Click "Create Assistant"**
3. **Fill Basic Info:**
   - Name: Adani Bill Collection Assistant
   - Description: AI assistant for electricity bill collection
4. **Paste System Prompt** (from section 2 above)
5. **Paste First Message** (from section 1 above)
6. **Configure Model:**
   - Select OpenAI → GPT-4
   - Set Temperature: 0.7
   - Max Tokens: 250
7. **Configure Voice:**
   - Select ElevenLabs
   - Choose professional voice
   - Set stability: 0.5, similarity: 0.75, speed: 1.0
8. **Add Functions:**
   - Click "Add Function"
   - Add all 3 functions from section 3
9. **Set Advanced Options:**
   - Enable recording
   - Set max duration: 300s
   - Set silence timeout: 30s
10. **Configure Server URL:**
    - Add your webhook URL
    - Generate and save secret
11. **Save Assistant**
12. **Copy Assistant ID** and add to your `.env` file

---

## 8️⃣ TESTING YOUR ASSISTANT

After creation:

1. Click "Test" button in VAPI dashboard
2. Make a test call to your phone
3. Verify:
   - ✅ Voice quality is good
   - ✅ AI follows the script
   - ✅ Functions are called correctly
   - ✅ Variables are populated
4. Review transcript and recording
5. Adjust prompts if needed

---

## 9️⃣ ENVIRONMENT VARIABLES TO ADD

After creating the assistant, add these to your `.env` file:

```env
VAPI_API_KEY=your_vapi_api_key_from_dashboard
VAPI_ASSISTANT_ID=your_created_assistant_id
VAPI_PHONE_NUMBER_ID=your_vapi_phone_number_id
```

---

## 🎯 Quick Tips

1. **Voice Selection:** Test multiple voices to find the most natural one for Indian customers
2. **Temperature:** Lower (0.5-0.6) for more consistent responses, higher (0.7-0.8) for more natural conversation
3. **First Message:** Keep it concise but warm to build rapport
4. **System Prompt:** The more specific, the better the AI performs
5. **Functions:** Test each function individually before going live
6. **Webhook:** Ensure your backend is accessible from internet (use ngrok for local testing)

---

## 🔧 Troubleshooting

**Issue:** AI not following script
- **Solution:** Make system prompt more specific, reduce temperature

**Issue:** Functions not being called
- **Solution:** Verify webhook URL is correct and accessible

**Issue:** Poor voice quality
- **Solution:** Try different voice provider or adjust stability/speed settings

**Issue:** Call drops early
- **Solution:** Increase max duration and silence timeout

---

## 📞 Support Resources

- VAPI Documentation: https://docs.vapi.ai
- VAPI Discord: Join for community support
- API Reference: https://docs.vapi.ai/api-reference

---

## ✅ Checklist Before Going Live

- [ ] System prompt tested and refined
- [ ] First message sounds natural
- [ ] All 3 functions added and tested
- [ ] Voice quality verified
- [ ] Webhook URL configured and tested
- [ ] Variables properly set
- [ ] Test calls completed successfully
- [ ] Recording and transcripts reviewed
- [ ] Assistant ID added to .env
- [ ] Backend webhook handler working

---

**You're ready to create your VAPI assistant! 🚀**
