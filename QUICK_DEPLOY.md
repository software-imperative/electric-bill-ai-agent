# ⚡ Quick Deploy Guide

## 🚀 Fastest Way to Deploy (5 minutes)

### Option 1: Render.com + Netlify (Recommended)

#### Backend (Render.com) - 3 minutes
1. Go to [render.com](https://render.com) → Sign up (free)
2. Click "New +" → "Web Service"
3. Connect GitHub → Select your repo
4. Settings:
   - **Build**: `pip install -r backend/requirements.txt`
   - **Start**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
5. Add PostgreSQL database (New + → PostgreSQL → Free)
6. Add environment variables (see DEPLOYMENT.md)
7. Deploy! ✅

#### Frontend (Netlify) - 2 minutes
1. Go to [netlify.com](https://netlify.com) → Sign up (free)
2. "Add new site" → "Import from Git"
3. Select your repo
4. Settings:
   - **Publish directory**: `frontend`
   - **Build command**: (leave empty)
5. Add environment variable:
   - `API_BASE_URL` = `https://your-render-app.onrender.com`
6. Deploy! ✅

### Option 2: Railway.app (All-in-One)

1. Go to [railway.app](https://railway.app) → Sign up (free)
2. "New Project" → "Deploy from GitHub"
3. Select your repo
4. Add PostgreSQL service
5. Set environment variables
6. Deploy! ✅

---

## 📝 Required Environment Variables

Copy these to your hosting platform:

```
VAPI_API_KEY=your_key
VAPI_PHONE_NUMBER_ID=your_id
VAPI_ASSISTANT_ID=your_id
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_number
SECRET_KEY=generate_random_string
API_BASE_URL=https://your-backend-url
FRONTEND_URL=https://your-frontend-url
DEBUG=false
```

---

## ✅ After Deployment

1. Test backend: `https://your-backend.onrender.com/health`
2. Test frontend: `https://your-frontend.netlify.app`
3. Update VAPI webhooks to point to your backend URL
4. Done! 🎉

---

For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

