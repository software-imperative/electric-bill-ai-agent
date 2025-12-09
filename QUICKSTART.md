# 🚀 Quick Start Guide - Run the Project

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9+ installed
- ✅ VAPI account created
- ✅ Twilio account created
- ✅ ngrok installed (for local testing)

---

## Step 1: Backend Setup (5 minutes)

### 1.1 Navigate to Backend Directory
```bash
cd "d:\Voice Agent\Electric bill AI Agent\backend"
```

### 1.2 Create Virtual Environment
```bash
python -m venv venv
```

### 1.3 Activate Virtual Environment
```bash
# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### 1.4 Install Dependencies
```bash
pip install -r requirements.txt
```

### 1.5 Configure Environment Variables
```bash
# Copy the example file
copy .env.example .env

# Open .env file and fill in your credentials
notepad .env
```

**Required Variables in .env:**
```env
# VAPI Configuration
VAPI_API_KEY=your_vapi_api_key
VAPI_PHONE_NUMBER_ID=your_phone_number_id
VAPI_ASSISTANT_ID=your_assistant_id

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+91XXXXXXXXXX

# Database
DATABASE_URL=sqlite:///./bills.db

# Application
SECRET_KEY=your_secret_key_here
API_BASE_URL=http://localhost:8000
DEBUG=True
```

**Generate Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 1.6 Run the Backend Server
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

**✅ Backend is running!** Keep this terminal open.

**Test it:** Open browser → http://localhost:8000/docs

---

## Step 2: Expose Backend with ngrok (For VAPI Webhooks)

### 2.1 Open New Terminal
Keep the backend terminal running, open a new terminal.

### 2.2 Start ngrok
```bash
ngrok http 8000
```

**Expected Output:**
```
Forwarding    https://xxxx-xx-xx-xx.ngrok-free.app -> http://localhost:8000
```

### 2.3 Copy the HTTPS URL
Copy the `https://xxxx.ngrok-free.app` URL - you'll need this for VAPI webhook configuration.

**✅ Backend is now accessible from internet!** Keep this terminal open.

---

## Step 3: Frontend Setup (2 minutes)

### 3.1 Open New Terminal
Navigate to frontend directory:
```bash
cd "d:\Voice Agent\Electric bill AI Agent\frontend"
```

### 3.2 Update API URL (if needed)
Open `assets/js/api.js` and verify:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### 3.3 Start Frontend Server
```bash
python -m http.server 3000
```

**Expected Output:**
```
Serving HTTP on :: port 3000 (http://[::]:3000/) ...
```

**✅ Frontend is running!**

**Access Dashboard:** Open browser → http://localhost:3000

---

## Step 4: Configure VAPI Assistant

### 4.1 Create VAPI Assistant
1. Go to https://vapi.ai/dashboard
2. Navigate to **Assistants** → **Create Assistant**
3. Use the content from `vapi_config/VAPI_ASSISTANT_CREATION.md`

### 4.2 Set Webhook URL
In VAPI Assistant settings:
- **Server URL:** `https://your-ngrok-url.ngrok-free.app/api/webhooks/vapi/events`
- Replace with your actual ngrok URL from Step 2.3

### 4.3 Save Assistant ID
After creating the assistant:
1. Copy the Assistant ID
2. Add to your `.env` file:
```env
VAPI_ASSISTANT_ID=your_assistant_id_here
```
3. Restart the backend server (Ctrl+C and run uvicorn command again)

---

## Step 5: Test the System

### 5.1 Access the Dashboard
Open: http://localhost:3000

### 5.2 Create a Test Bill
1. Click **"Add New Bill"** button
2. Fill in the form:
   - Customer Name: Test Customer
   - Phone: +919876543210 (use your verified number for testing)
   - Consumer Number: TEST001
   - Bill Number: BILL001
   - Amount: 1500
   - Due Date: Select a future date
3. Click **"Add Bill"**

### 5.3 Initiate a Test Call
1. Find the bill in the table
2. Click **"📞 Call"** button
3. The AI will call the phone number
4. Answer and test the conversation

### 5.4 Verify Everything Works
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

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check if port 8000 is in use
netstat -ano | findstr :8000
```

### Frontend shows API error
1. Check backend is running (http://localhost:8000/health)
2. Check API_BASE_URL in `frontend/assets/js/api.js`
3. Clear browser cache (Ctrl+Shift+Delete)

### VAPI calls not working
1. Verify ngrok is running
2. Check webhook URL in VAPI dashboard
3. Verify VAPI credentials in `.env`
4. Check backend logs for webhook errors

### Database errors
```bash
# Delete and recreate database
cd backend
del bills.db
# Restart backend (will recreate tables)
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

## 📝 Development Workflow

### Adding New Bills
1. Use dashboard → Add Bill button
2. Or use API: http://localhost:8000/docs → POST /api/bills/

### Viewing Call Logs
1. Dashboard → Call Logs tab
2. Or API: http://localhost:8000/docs → GET /api/calls/

### Testing VAPI Integration
1. Create bill with your phone number
2. Click Call button
3. Answer the call
4. Test the conversation flow
5. Check call logs and transcripts

### Monitoring
- Backend logs in terminal
- VAPI dashboard for call details
- Twilio console for SMS delivery

---

## 🎯 Next Steps After Running

1. ✅ Test with 2-3 sample bills
2. ✅ Review call recordings in VAPI dashboard
3. ✅ Check SMS delivery in Twilio console
4. ✅ Adjust AI prompts if needed
5. ✅ Monitor call success rates
6. ✅ Optimize based on results

---

## 🚀 Production Deployment (Later)

When ready for production:
1. Deploy backend to Heroku/AWS/DigitalOcean
2. Deploy frontend to Netlify/Vercel
3. Use PostgreSQL instead of SQLite
4. Update VAPI webhook to production URL
5. Remove ngrok dependency

---

**You're all set! 🎉**

Start with Step 1 and follow sequentially. Each step should take 2-5 minutes.
