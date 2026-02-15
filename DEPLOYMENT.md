# AI Financial Coach - Complete Deployment Guide

## 🚀 Quick Start

### Backend Setup
```bash
# 1. Navigate to project
cd Finance_AI

# 2. Activate environment
conda activate Finance_env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export OPENROUTER_API_KEY='your-key-here'

# 5. Start backend
uvicorn backend.main:app --reload --port 8000
```

### Frontend Setup
```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start dev server
npm run dev

# Visit: http://localhost:5173
```

---

## 📦 System Requirements

### Backend
- **Python:** 3.11+
- **Platform:** macOS, Linux, Windows
- **Memory:** 512MB minimum
- **Dependencies:** See `requirements.txt`

### Frontend
- **Node.js:** 18+
- **npm:** 9+
- **Browser:** Modern (Chrome, Firefox, Safari, Edge)

---

## 🔑 Environment Variables

### Backend (`backend/.env`)
```env
OPENROUTER_API_KEY=sk-your-key-here
PORT=8000
LOG_LEVEL=INFO
```

### Frontend (`frontend/.env`)
```env
VITE_API_URL=http://localhost:8000
```

---

## 🧪 Testing

### Run Integration Tests
```bash
# Set API key
export OPENROUTER_API_KEY='your-key-here'

# Run all tests
./run_tests.sh
```

### Expected Results
- ✅ 3/3 tests pass
- ⏱️ Complete in ~30-40 seconds
- 📊 All components validated

---

## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │  React + TypeScript + Tailwind
│ (Port 5173) │  File upload, Dashboard, Charts
└──────┬──────┘
       │ HTTP
       ↓
┌─────────────┐
│   Backend   │  FastAPI + Python
│ (Port 8000) │  REST API, CORS, Error handling
└──────┬──────┘
       │
       ├─→ OCR Engine (PaddleOCR)
       ├─→ Transaction Categorizer (Rule-based)
       ├─→ Metrics Calculator (Deterministic)
       └─→ LangGraph Multi-Agent System
           ├─→ Debt Analyzer Agent
           ├─→ Savings Strategy Agent
           ├─→ Budget Optimizer Agent
           └─→ Risk Scorer Agent
```

---

## 📊 API Endpoints

### Health Check
```bash
GET /health
Response: {"status": "healthy"}
```

### Analyze Statement
```bash
POST /api/analyze
Content-Type: multipart/form-data
Body: file=statement.pdf

Response: {
  "analysis_id": "uuid",
  "summary": {...},
  "transactions": [...],
  "analysis": {
    "debt": {...},
    "savings": {...},
    "budget": {...},
    "risk": {...}
  }
}
```

---

## 🎨 Frontend Pages

### Home (`/`)
- Gradient hero section
- File upload with drag & drop
- Feature cards
- Animated transitions

### Analysis Dashboard (`/analysis/:id`)
- Financial summary card
- 4 AI analysis cards:
  - 💳 Debt Analysis
  - 💰 Savings Strategy
  - 📊 Budget Optimizer
  - ⚠️ Risk Score
- Export functionality

---

## 🔧 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn backend.main:app --port 8001
```

**Import errors:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

**OCR not working:**
```bash
# Reinstall PaddleOCR
pip install --force-reinstall paddleocr paddlepaddle
```

### Frontend Issues

**Styles not loading:**
```bash
# Reinstall Tailwind
cd frontend
npm install -D @tailwindcss/postcss
npm run dev
```

**Build errors:**
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

**CORS errors:**
- Check `backend/api/middleware/cors.py`
- Ensure frontend URL in allowed origins
- Restart backend server

---

## 📈 Performance Optimization

### Backend
- Use `uvicorn --workers 4` for production
- Enable caching for repeated analyses
- Consider GPU for OCR (if available)

### Frontend
- Build for production: `npm run build`
- Use CDN for static assets
- Enable lazy loading for routes

---

## 🚢 Production Deployment

### Backend Options

#### Option 1: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

#### Option 2: Render
```bash
# Create render.yaml
web:
  - type: web
    name: finance-ai-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

#### Option 3: AWS EC2
```bash
# SSH to instance
# Install dependencies
# Run with systemd or supervisor
```

### Frontend Options

#### Option 1: Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel deploy --prod
```

#### Option 2: Netlify
```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

---

## 🔐 Security Checklist

- [ ] API keys in environment variables (not code)
- [ ] CORS properly configured
- [ ] Input validation on all endpoints
- [ ] Rate limiting enabled
- [ ] HTTPS in production
- [ ] Sensitive data not logged
- [ ] Dependencies up to date

---

## 📚 Documentation

- **Backend API:** `/docs` (Swagger UI)
- **Backend ReDoc:** `/redoc`
- **Testing Guide:** `tests/README.md`
- **Frontend README:** `frontend/README.md`

---

## 🎯 Success Metrics

### Functional
- ✅ Upload PDF → Get analysis
- ✅ All 4 AI agents respond
- ✅ Dashboard displays correctly
- ✅ Error handling works

### Performance
- ⏱️ Analysis < 35 seconds
- 📊 99% uptime
- 🚀 Page load < 2 seconds
- 💰 API cost < $0.10/analysis

---

## 🆘 Support

### Common Issues

**"Module not found" errors:**
- Check virtual environment is activated
- Reinstall dependencies

**"Connection refused" errors:**
- Ensure backend is running
- Check port numbers match
- Verify firewall settings

**"API key invalid" errors:**
- Check OpenRouter account
- Verify key is set correctly
- Ensure key has credits

---

## 🎉 You're Ready!

1. ✅ Backend running on port 8000
2. ✅ Frontend running on port 5173
3. ✅ Tests passing
4. ✅ Documentation complete

**Upload a bank statement and enjoy AI-powered financial insights!** 🚀

---

## 📞 Next Steps

**Production Checklist:**
- [ ] Deploy backend to Railway/Render
- [ ] Deploy frontend to Vercel/Netlify
- [ ] Set production environment variables
- [ ] Configure custom domain
- [ ] Enable monitoring (Sentry, LogRocket)
- [ ] Set up CI/CD pipeline
- [ ] Create backup strategy

**Future Enhancements:**
- [ ] Database integration (MongoDB)
- [ ] User authentication
- [ ] Analysis history
- [ ] PDF export
- [ ] Mobile app
- [ ] Multi-language support
