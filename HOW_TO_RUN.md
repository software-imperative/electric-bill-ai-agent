# 🚀 How to Run the Project - Step by Step Guide

This guide will walk you through running the Adani Bill Collection AI Agent project from scratch.

---

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ **Python 3.9 or higher** installed
  - Check: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/
  
- ✅ **VAPI.ai account** (for voice calls)
  - Sign up: https://vapi.ai
  
- ✅ **Twilio account** (for SMS)
  - Sign up: https://www.twilio.com/try-twilio
  
- ✅ **ngrok** (for local webhook testing)
  - Download: https://ngrok.com/download
  - Or use: `choco install ngrok` (if you have Chocolatey)

---

## 🎯 Step-by-Step Setup

### Step 1: Navigate to Project Directory

Open Command Prompt or PowerShell and navigate to your project:

```bash
cd "d:\Voice Agent\Electric bill AI Agent"
```

---

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory

```bash
cd backend
```

#### 2.2 Create Virtual Environment

```bash
python -m venv venv
```

#### 2.3 Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 2.4 Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn
- SQLAlchemy
- Twilio
- Pydantic
- And other required packages

#### 2.5 Create Environment File

Create a `.env` file in the `backend` directory:

```bash
# On Windows
copy NUL .env
notepad .env

# On Mac/Linux
touch .env
nano .env
```

#### 2.6 Configure Environment Variables

Add the following to your `.env` file:

```env
# VAPI Configuration (Get from https://vapi.ai/dashboard)
VAPI_API_KEY=your_vapi_api_key_here
VAPI_PHONE_NUMBER_ID=your_phone_number_id_here
VAPI_ASSISTANT_ID=your_assistant_id_here
VAPI_API_URL=https://api.vapi.ai

# Twilio Configuration (Get from https://console.twilio.com)
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890

# Database Configuration
DATABASE_URL=sqlite:///./bills.db

# Application Configuration
SECRET_KEY=your_secret_key_here
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
DEBUG=True

# SMS Templates (Optional - uses defaults if not set)
SMS_PAYMENT_LINK_TEMPLATE=Dear customer, your bill of Rs.{amount} is due on {due_date}. Pay now: {payment_link}
SMS_REMINDER_TEMPLATE=Reminder: Your bill of Rs.{amount} is overdue. Please pay immediately: {payment_link}
SMS_THANK_YOU_TEMPLATE=Thank you for your payment of Rs.{amount}. Your payment has been received successfully.
```

**Generate Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as `SECRET_KEY` in your `.env` file.

#### 2.7 Run the Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **Backend is running!** Keep this terminal open.

**Test it:** Open browser → http://localhost:8000/docs

---

### Step 3: Expose Backend with ngrok (For VAPI Webhooks)

VAPI needs to send webhooks to your backend. Since it's running locally, we need to expose it.

#### 3.1 Open a NEW Terminal

Keep the backend terminal running, open a new terminal window.

#### 3.2 Start ngrok

```bash
ngrok http 8000
```

**Expected Output:**
```
Forwarding    https://xxxx-xx-xx-xx.ngrok-free.app -> http://localhost:8000
```

#### 3.3 Copy the HTTPS URL

Copy the `https://xxxx.ngrok-free.app` URL - you'll need this for VAPI webhook configuration.

✅ **Backend is now accessible from internet!** Keep this terminal open.

---

### Step 4: Frontend Setup

#### 4.1 Open a NEW Terminal

Navigate to frontend directory:

```bash
cd "d:\Voice Agent\Electric bill AI Agent\frontend"
```

#### 4.2 Start Frontend Server

```bash
python -m http.server 3000
```

**Expected Output:**
```
Serving HTTP on :: port 3000 (http://[::]:3000/) ...
```

✅ **Frontend is running!**

**Access Dashboard:** Open browser → http://localhost:3000

---

### Step 5: Configure VAPI Assistant

#### 5.1 Get VAPI Credentials

1. Go to https://vapi.ai/dashboard
2. Navigate to **Settings** → **API Keys**
3. Copy your API key → Add to `.env` as `VAPI_API_KEY`

#### 5.2 Purchase/Get Phone Number

1. Go to **Phone Numbers** in VAPI dashboard
2. Purchase or use existing phone number
3. Copy Phone Number ID → Add to `.env` as `VAPI_PHONE_NUMBER_ID`

#### 5.3 Create Assistant

1. Go to **Assistants** → **Create Assistant**
2. Use the configuration from `vapi_config/assistant_config.json`
3. Set **System Prompt** from `vapi_config/system_prompt.txt`
4. Set **First Message** from `vapi_config/first_message.txt`
5. Add **Functions** from `vapi_config/functions.json`
6. Set **Server URL** (Webhook): `https://your-ngrok-url.ngrok-free.app/api/webhooks/vapi/events`
   - Replace with your actual ngrok URL from Step 3.3

#### 5.4 Save Assistant ID

After creating the assistant:
1. Copy the Assistant ID
2. Add to your `.env` file: `VAPI_ASSISTANT_ID=your_assistant_id_here`
3. Restart the backend server (Ctrl+C and run uvicorn command again)

---

### Step 6: Configure Twilio

#### 6.1 Get Twilio Credentials

1. Go to https://console.twilio.com
2. Copy **Account SID** → Add to `.env` as `TWILIO_ACCOUNT_SID`
3. Copy **Auth Token** → Add to `.env` as `TWILIO_AUTH_TOKEN`

#### 6.2 Get Phone Number

1. Go to **Phone Numbers** → **Manage** → **Active Numbers**
2. Copy your phone number → Add to `.env` as `TWILIO_PHONE_NUMBER`
3. Format: `+1234567890` (include country code with +)

**Note:** If using Twilio trial account, you can only send SMS to verified numbers.

---

### Step 7: Seed Sample Data (Optional)

To test with sample bills:

#### 7.1 Open a NEW Terminal

Navigate to backend directory:

```bash
cd "d:\Voice Agent\Electric bill AI Agent\backend"
venv\Scripts\activate  # Activate venv if not already active
```

#### 7.2 Run Seed Script

```bash
python seed_data.py
```

**Expected Output:**
```
🌱 Seeding database with sample bills...
============================================================
✅ Created bill for Mayur Gadekar - ₹2450.5 - Status: overdue
✅ Created bill for Rajesh Kumar Singh - ₹3200.0 - Status: overdue
...
🎉 Successfully created 10 bills!
```

---

### Step 8: Test the System

#### 8.1 Access Dashboard

Open browser → http://localhost:3000

You should see:
- Dashboard with statistics
- Bills table (if you seeded data)
- Navigation menu

#### 8.2 Create a Test Bill

1. Click **"Add New Bill"** button
2. Fill in the form:
   - Customer Name: Test Customer
   - Phone: +919876543210 (use your verified number for testing)
   - Consumer Number: TEST001
   - Bill Number: BILL001
   - Amount: 1500
   - Due Date: Select a future date
3. Click **"Add Bill"**

#### 8.3 Initiate a Test Call

1. Find the bill in the table
2. Click **"📞 Call"** button
3. The AI will call the phone number
4. Answer and test the conversation

#### 8.4 Verify Everything Works

- ✅ Call connects
- ✅ AI speaks the greeting
- ✅ SMS is sent when you agree
- ✅ Call log appears in dashboard
- ✅ Bill status updates

---

## 📊 Running Terminals Summary

You should have **3 terminals running**:

1. **Backend Server** (Port 8000)
   ```bash
   cd backend
   venv\Scripts\activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **ngrok** (Exposing backend)
   ```bash
   ngrok http 8000
   ```

3. **Frontend Server** (Port 3000)
   ```bash
   cd frontend
   python -m http.server 3000
   ```

---

## 🔍 Quick Access URLs

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **ngrok URL:** https://your-ngrok-url.ngrok-free.app

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.9+

# Check if port 8000 is in use
netstat -ano | findstr :8000

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend shows API error

1. Check backend is running: http://localhost:8000/health
2. Check `frontend/assets/js/api.js` - `API_BASE_URL` should be `http://localhost:8000`
3. Clear browser cache (Ctrl+Shift+Delete)
4. Check browser console for errors (F12)

### VAPI calls not working

1. Verify ngrok is running
2. Check webhook URL in VAPI dashboard matches ngrok URL
3. Verify VAPI credentials in `.env`
4. Check backend logs for webhook errors
5. Ensure phone number is active in VAPI

### SMS not sending

1. Check Twilio credentials in `.env`
2. Verify phone number format (+91XXXXXXXXXX)
3. Check Twilio account balance
4. If using trial account, verify recipient number
5. Review Twilio error logs in console

### Database errors

```bash
# Delete and recreate database
cd backend
del bills.db  # On Windows
# rm bills.db  # On Mac/Linux

# Restart backend (will recreate tables)
uvicorn app.main:app --reload
```

### Module not found errors

```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 🛑 Stopping the Project

To stop all services:

1. **Stop Backend:** Press `Ctrl+C` in backend terminal
2. **Stop ngrok:** Press `Ctrl+C` in ngrok terminal
3. **Stop Frontend:** Press `Ctrl+C` in frontend terminal

---

## 🔄 Restarting the Project

Next time you want to run:

```bash
# Terminal 1: Backend
cd "d:\Voice Agent\Electric bill AI Agent\backend"
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: ngrok
ngrok http 8000

# Terminal 3: Frontend
cd "d:\Voice Agent\Electric bill AI Agent\frontend"
python -m http.server 3000
```

**Note:** If ngrok URL changes, update it in VAPI dashboard webhook settings.

---

## ✅ Checklist

Before running, ensure:

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with all credentials
- [ ] VAPI account created and assistant configured
- [ ] Twilio account created and phone number obtained
- [ ] ngrok installed and running
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 3000
- [ ] VAPI webhook URL configured with ngrok URL

---

## 🎉 You're All Set!

Once everything is running:

1. ✅ Access dashboard at http://localhost:3000
2. ✅ Create bills and initiate calls
3. ✅ Monitor call logs and payments
4. ✅ View analytics and statistics

For more details, see:
- [QUICKSTART.md](QUICKSTART.md)
- [docs/SETUP.md](docs/SETUP.md)
- [docs/VAPI_GUIDE.md](docs/VAPI_GUIDE.md)
- [docs/TWILIO_GUIDE.md](docs/TWILIO_GUIDE.md)

---

## 📞 Need Help?

1. Check the troubleshooting section above
2. Review API documentation at http://localhost:8000/docs
3. Check backend terminal for error logs
4. Review VAPI/Twilio console for service-specific errors

