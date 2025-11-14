# 📋 Quick Reference Card

## 🚀 Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] OpenAI API key obtained
- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] Service account created
- [ ] credentials.json downloaded
- [ ] Google Sheet shared with service account
- [ ] Run setup.bat
- [ ] Edit backend/.env with API keys
- [ ] Edit backend/.env with Sheet ID
- [ ] Run start.bat

## 🎯 Quick Commands

### Setup (First Time)
```cmd
setup.bat
```

### Start System
```cmd
start.bat
```

### Manual Start - Backend
```cmd
cd backend
python main.py
```

### Manual Start - Frontend
```cmd
cd frontend
npm run dev
```

### Install Backend Dependencies
```cmd
cd backend
pip install -r requirements.txt
```

### Install Frontend Dependencies
```cmd
cd frontend
npm install
```

## 🔑 Key Files to Edit

### Backend Configuration
**File**: `backend/.env`
```env
OPENAI_API_KEY=sk-your-key-here
GOOGLE_SHEET_IDS=your-sheet-id-here
```

### Frontend Configuration
**File**: `frontend/.env`
```env
VITE_API_URL=http://localhost:8000
```

### Google Credentials
**File**: `backend/credentials.json`
- Download from Google Cloud Console
- Place in backend folder
- Never commit to git!

## 📍 Important URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎨 Key Components

### Backend Services
- `sheets_sync.py` - Google Sheets connection
- `ai_chat.py` - AI chat functionality
- `analytics.py` - Data processing

### Frontend Components
- `Dashboard.jsx` - Analytics view
- `ChatInterface.jsx` - AI chat
- `Filters.jsx` - Filter controls
- `StockCard.jsx` - Stock display

## 💡 Common Tasks

### Add New Google Sheet
1. Get Sheet ID from URL
2. Add to `GOOGLE_SHEET_IDS` in .env (comma-separated)
3. Share sheet with service account email
4. Restart backend
5. Click "Sync Data"

### Change Colors
**File**: `frontend/tailwind.config.js`
```javascript
colors: {
  primary: {
    500: '#YOUR_COLOR',
    600: '#YOUR_DARKER_COLOR',
  }
}
```

### Change AI Model
**File**: `backend/services/ai_chat.py`
```python
model="gpt-4"  # or "gpt-3.5-turbo"
```

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "Port already in use" | Change PORT in .env |
| "Module not found" | Run pip install / npm install |
| "Authentication failed" | Check credentials.json location |
| "No data available" | Click "Sync Data" button |
| "CORS error" | Check FRONTEND_URL in backend .env |
| Backend won't start | Check Python version (3.8+) |
| Frontend won't start | Check Node version (18+) |

## 📊 Data Format Expected

Your Google Sheet should have these columns:
- Symbol
- Timeframe
- EMA50
- EMA200
- ATR
- Price
- ATRPercentage (or atrPercentage)
- ADX (or ADX with space)
- Trend
- Trend_strength (or trendStrength)
- Volatility
- sentimentScore (or sentiment_score)
- rational (or rationale)
- date
- stock

*Case-insensitive, spaces/underscores handled automatically*

## 🎯 Features Quick Access

### Sync Data
**Location**: Top-right button
**What it does**: Fetches latest data from Google Sheets

### Filters
**Location**: Stocks tab
**Available filters**:
- Trend (uptrend/downtrend)
- Strength (strong/weak/developing)
- Volatility (high/moderate/low)
- Min Sentiment (-1 to 1)
- Min ADX (0-100)

### AI Chat
**Location**: AI Chat tab
**Example queries**:
- "Show me strong uptrend stocks"
- "What's the average sentiment?"
- "List high volatility stocks"
- "Which stocks have sentiment above 0.5?"

## 📱 Keyboard Shortcuts

### Chat Interface
- **Enter** - Send message
- **Shift+Enter** - New line

### General
- **Ctrl+R** - Refresh browser
- **F12** - Open developer tools (for debugging)

## 🔐 Security Reminders

- ✅ Never commit .env files
- ✅ Never commit credentials.json
- ✅ Keep API keys secret
- ✅ Use .gitignore (already included)
- ✅ Rotate API keys periodically

## 📞 Support Resources

### Documentation Files
- `README.md` - Full technical guide
- `CLIENT_GUIDE.md` - Simple user guide
- `SYSTEM_OVERVIEW.md` - Architecture details
- `UI_PREVIEW.md` - UI design reference

### Online Resources
- OpenAI API Docs: https://platform.openai.com/docs
- Google Sheets API: https://developers.google.com/sheets
- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev/

## ✅ Daily Workflow

1. **Start**: Double-click `start.bat`
2. **Wait**: 10 seconds for servers to start
3. **Open**: Browser opens automatically
4. **Sync**: Click "Sync Data" button
5. **Analyze**: Use dashboard, filters, or AI chat
6. **Close**: Close terminal windows when done

## 🚀 Deployment Checklist

### Backend (Railway/Render)
- [ ] Create new project
- [ ] Connect GitHub repo
- [ ] Set environment variables
- [ ] Upload credentials.json as secret
- [ ] Deploy

### Frontend (Vercel/Netlify)
- [ ] Build: `npm run build`
- [ ] Connect to hosting
- [ ] Set VITE_API_URL to backend URL
- [ ] Deploy dist folder

---

**Keep this reference handy for quick access to common tasks! 📌**
