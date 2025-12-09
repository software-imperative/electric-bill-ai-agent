# Adani Group - AI Voice Agent for Bill Collection

## 🎯 Objective
Automated bill collection system using AI voice calls with SMS payment links to reduce manual workforce and accelerate payment collection.

## 🌟 Features
- **AI Voice Calls**: Automated calls to consumers with pending bills
- **Bill Confirmation**: Verifies bill amount and due date with customer
- **SMS Payment Links**: Sends instant payment links during call
- **Payment Guidance**: Guides users through payment process
- **Payment Tracking**: Monitors payment completion in real-time
- **Auto Escalation**: Sends reminders for unpaid bills

## 🏗️ System Architecture

```
┌─────────────────┐
│   Customer      │
│   (Phone)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   VAPI.ai       │◄────►│   Twilio     │
│  (Voice AI)     │      │   (SMS/Voice)│
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend (Python)        │
│  ┌─────────────────────────────────┐   │
│  │  Webhook Handlers               │   │
│  │  - Call Events                  │   │
│  │  - Function Calling             │   │
│  │  - Payment Webhooks             │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  Business Logic                 │   │
│  │  - Bill Management              │   │
│  │  - Payment Processing           │   │
│  │  - SMS Sending                  │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  Database (SQLite/PostgreSQL)   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│    Frontend Dashboard (HTML/CSS/JS)     │
│  - Bill Management                      │
│  - Call Logs & Analytics                │
│  - Payment Tracking                     │
│  - Real-time Updates                    │
└─────────────────────────────────────────┘
```

## 📁 Project Structure

```
Electric bill AI Agent/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── config.py               # Configuration settings
│   │   ├── database.py             # Database connection
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── bill.py             # Bill model
│   │   │   ├── call_log.py         # Call log model
│   │   │   └── payment.py          # Payment model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── bill.py             # Bill schemas
│   │   │   ├── call.py             # Call schemas
│   │   │   └── payment.py          # Payment schemas
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── vapi_webhooks.py    # VAPI webhook endpoints
│   │   │   ├── bills.py            # Bill management APIs
│   │   │   ├── calls.py            # Call management APIs
│   │   │   └── payments.py         # Payment APIs
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── vapi_service.py     # VAPI integration
│   │   │   ├── twilio_service.py   # Twilio SMS integration
│   │   │   ├── bill_service.py     # Bill business logic
│   │   │   └── payment_service.py  # Payment processing
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py          # Utility functions
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html                  # Main dashboard
│   ├── assets/
│   │   ├── css/
│   │   │   ├── main.css            # Main styles
│   │   │   └── components.css      # Component styles
│   │   └── js/
│   │       ├── app.js              # Main application logic
│   │       ├── api.js              # API client
│   │       ├── dashboard.js        # Dashboard functionality
│   │       └── utils.js            # Utility functions
│   └── components/
│       ├── bills.html              # Bill management component
│       ├── calls.html              # Call logs component
│       └── payments.html           # Payment tracking component
├── vapi_config/
│   ├── assistant_config.json       # VAPI assistant configuration
│   ├── system_prompt.txt           # System prompt for AI
│   ├── first_message.txt           # First message template
│   └── functions.json              # Function calling definitions
├── docs/
│   ├── SETUP.md                    # Setup instructions
│   ├── VAPI_GUIDE.md              # VAPI configuration guide
│   ├── TWILIO_GUIDE.md            # Twilio setup guide
│   └── API_DOCS.md                # API documentation
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- VAPI.ai account
- Twilio account
- Node.js (for frontend development tools, optional)

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Open frontend/index.html in a browser**
   - For development, use a local server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   - Access at: http://localhost:3000

### VAPI Configuration

See [VAPI_GUIDE.md](docs/VAPI_GUIDE.md) for detailed setup instructions.

### Twilio Configuration

See [TWILIO_GUIDE.md](docs/TWILIO_GUIDE.md) for detailed setup instructions.

## 📊 Demo Flow

1. **Bill Upload**: Admin uploads pending bills to the system
2. **AI Call Initiation**: System triggers VAPI to call customer
3. **Bill Confirmation**: AI confirms bill details with customer
4. **SMS Payment Link**: Twilio sends payment link via SMS
5. **Payment Guidance**: AI guides customer through payment
6. **Payment Tracking**: System monitors payment completion
7. **Confirmation**: AI thanks customer upon payment
8. **Escalation**: Auto-reminder if payment not completed

## 🔧 Technology Stack

- **Voice AI**: VAPI.ai
- **SMS/Voice**: Twilio
- **Backend**: Python, FastAPI
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: HTML, CSS, JavaScript
- **API Documentation**: Swagger/OpenAPI

## 📝 Environment Variables

```env
# VAPI Configuration
VAPI_API_KEY=your_vapi_api_key
VAPI_PHONE_NUMBER_ID=your_vapi_phone_number_id
VAPI_ASSISTANT_ID=your_vapi_assistant_id

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Application Configuration
DATABASE_URL=sqlite:///./bills.db
SECRET_KEY=your_secret_key
API_BASE_URL=http://localhost:8000

# Payment Gateway (Optional)
PAYMENT_GATEWAY_URL=your_payment_gateway_url
PAYMENT_GATEWAY_KEY=your_payment_gateway_key
```

## 📚 Documentation

- [Setup Guide](docs/SETUP.md)
- [VAPI Configuration](docs/VAPI_GUIDE.md)
- [Twilio Setup](docs/TWILIO_GUIDE.md)
- [API Documentation](docs/API_DOCS.md)

## 🎯 Outcome

- ✅ Faster bill collections
- ✅ Reduced manual workforce
- ✅ Zero delay in payment processing
- ✅ Automated follow-ups and reminders
- ✅ Real-time payment tracking

## 🚀 Free Hosting Deployment

This project can be deployed online for free using:

- **Backend**: [Render.com](https://render.com) (Free tier available)
- **Frontend**: [Netlify](https://netlify.com) or [Vercel](https://vercel.com) (Free tier available)

### Quick Deploy

1. **Backend**: See [DEPLOYMENT.md](./DEPLOYMENT.md) for Render.com setup
2. **Frontend**: See [DEPLOYMENT.md](./DEPLOYMENT.md) for Netlify/Vercel setup
3. **Quick Start**: See [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) for 5-minute setup

All deployment configuration files are included:
- `render.yaml` - Render.com configuration
- `netlify.toml` - Netlify configuration
- `vercel.json` - Vercel configuration
- `Procfile` - Process file for Render.com

---

## 📄 License

MIT License
