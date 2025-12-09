# Setup Guide - Adani Bill Collection AI Agent

Complete setup instructions for the AI Voice Agent system.

## 📋 Prerequisites

- Python 3.9 or higher
- VAPI.ai account
- Twilio account
- Text editor or IDE
- Terminal/Command Prompt

## 🚀 Quick Start

### 1. Clone or Download the Project

Navigate to your project directory:
```bash
cd "d:\Voice Agent\Electric bill AI Agent"
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Environment Variables

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` file with your credentials:

```env
# VAPI Configuration
VAPI_API_KEY=your_vapi_api_key
VAPI_PHONE_NUMBER_ID=your_phone_number_id
VAPI_ASSISTANT_ID=your_assistant_id

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+91XXXXXXXXXX

# Database (SQLite for development)
DATABASE_URL=sqlite:///./bills.db

# Application
SECRET_KEY=generate_random_secret_key_here
API_BASE_URL=http://localhost:8000
DEBUG=True
```

**Generate Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### Initialize Database

```bash
# The database will be created automatically when you run the app
# Tables will be created on first startup
```

#### Run the Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### 3. Frontend Setup

#### Option A: Simple HTTP Server (Recommended for Development)

```bash
cd frontend
python -m http.server 3000
```

Access the dashboard at: `http://localhost:3000`

#### Option B: Live Server (VS Code Extension)

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### 4. VAPI Configuration

Follow the detailed guide: [VAPI_GUIDE.md](VAPI_GUIDE.md)

**Quick Steps:**
1. Create VAPI account
2. Get API key
3. Purchase phone number
4. Create assistant using `vapi_config/assistant_config.json`
5. Configure webhooks to point to your backend
6. Add credentials to `.env`

### 5. Twilio Configuration

Follow the detailed guide: [TWILIO_GUIDE.md](TWILIO_GUIDE.md)

**Quick Steps:**
1. Create Twilio account
2. Get Account SID and Auth Token
3. Purchase phone number (or use trial number)
4. Verify test numbers (if using trial)
5. Add credentials to `.env`

## 🧪 Testing the System

### 1. Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Create a test bill
curl -X POST http://localhost:8000/api/bills/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Test Customer",
    "customer_phone": "+919876543210",
    "consumer_number": "TEST001",
    "bill_number": "BILL001",
    "bill_amount": 1500.00,
    "due_date": "2024-12-31T00:00:00Z"
  }'
```

### 2. Test Frontend

1. Open `http://localhost:3000` in browser
2. Click "Add New Bill"
3. Fill in the form
4. Submit and verify bill appears in table

### 3. Test VAPI Integration

1. Create a bill in the dashboard
2. Click "Call" button
3. Verify call is initiated
4. Check call logs

### 4. Test SMS Sending

The SMS will be sent automatically during the call when the AI calls the `send_payment_link` function.

## 📦 Production Deployment

### Backend Deployment (Example: Heroku)

1. **Create Heroku App**
```bash
heroku create adani-bill-collection-api
```

2. **Set Environment Variables**
```bash
heroku config:set VAPI_API_KEY=your_key
heroku config:set TWILIO_ACCOUNT_SID=your_sid
# ... set all other variables
```

3. **Deploy**
```bash
git push heroku main
```

4. **Update VAPI Webhook URL**
```
https://adani-bill-collection-api.herokuapp.com/api/webhooks/vapi/events
```

### Frontend Deployment (Example: Netlify)

1. **Build for Production** (if needed)
2. **Deploy to Netlify**
   - Drag and drop `frontend` folder
   - Or connect Git repository

3. **Update API URL**
   - Edit `frontend/assets/js/api.js`
   - Change `API_BASE_URL` to your production backend URL

### Database Migration (Production)

For production, use PostgreSQL instead of SQLite:

1. **Install PostgreSQL**
2. **Update DATABASE_URL**:
```env
DATABASE_URL=postgresql://user:password@localhost/adani_bills
```

3. **Install psycopg2**:
```bash
pip install psycopg2-binary
```

## 🔧 Configuration Options

### SMS Templates

Edit in `.env`:
```env
SMS_PAYMENT_LINK_TEMPLATE=Dear {name}, your bill of Rs.{amount} is due on {due_date}. Pay now: {payment_link}
```

### Call Settings

```env
MAX_CALL_DURATION=300          # 5 minutes
CALL_RETRY_ATTEMPTS=3          # Retry 3 times
REMINDER_INTERVAL_HOURS=24     # Remind after 24 hours
```

### VAPI Assistant Settings

Edit `vapi_config/assistant_config.json`:
- Change voice provider and voice ID
- Adjust temperature for AI responses
- Modify max duration and timeout

## 📊 Monitoring

### Backend Logs

```bash
# View logs
tail -f backend.log

# Or if running with uvicorn
# Logs appear in terminal
```

### VAPI Dashboard

- Monitor calls in VAPI dashboard
- Review call recordings
- Analyze transcripts

### Twilio Console

- Check SMS delivery status
- Monitor costs
- View error logs

## 🐛 Troubleshooting

### Backend Not Starting

```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for port conflicts
netstat -ano | findstr :8000
```

### Frontend Not Loading

```bash
# Check if backend is running
curl http://localhost:8000/health

# Clear browser cache
# Try incognito mode
```

### VAPI Calls Not Working

1. Check VAPI credentials in `.env`
2. Verify webhook URL is accessible
3. Check VAPI dashboard for errors
4. Ensure phone number is active

### SMS Not Sending

1. Check Twilio credentials
2. Verify phone number format (+91XXXXXXXXXX)
3. Check Twilio account balance
4. Review Twilio error logs

### Database Errors

```bash
# Delete database and recreate
rm backend/bills.db

# Restart backend (will recreate tables)
uvicorn app.main:app --reload
```

## 📚 Additional Resources

- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [VAPI Documentation](https://docs.vapi.ai)
- [Twilio Documentation](https://www.twilio.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

## 🔐 Security Checklist

- [ ] Never commit `.env` file
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS in production
- [ ] Set up CORS properly
- [ ] Rotate API keys regularly
- [ ] Monitor for unusual activity
- [ ] Implement rate limiting
- [ ] Backup database regularly

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review API documentation
3. Check VAPI/Twilio status pages
4. Review application logs

## 🎉 Next Steps

After setup:
1. ✅ Test with sample bills
2. ✅ Monitor call quality
3. ✅ Adjust AI prompts as needed
4. ✅ Scale up gradually
5. ✅ Implement monitoring and alerts
6. ✅ Train team on dashboard usage
