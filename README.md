# 📊 Trading Analytics Dashboard

A professional trading analytics platform that syncs with Google Sheets, provides AI-powered insights, and displays beautiful interactive dashboards.

> **Perfect for**: Demo presentations, client showcases, n8n automation integration

## ✨ Features

- 🔄 **Real-time Google Sheets Sync** - Fetch trading data automatically
- 🤖 **AI Chat Assistant** - Ask questions in natural language (OpenAI + LangChain)
- 📈 **Interactive Dashboards** - Beautiful charts with trends, sentiment, and performance
- 🎯 **Advanced Filtering** - Filter by trend, strength, volatility, sentiment, ADX
- 🎨 **Professional UI** - Clean interface built with React + Tailwind CSS
- ☁️ **Cloud-Ready** - Deploy to Google Cloud Run in minutes

## 🏗️ Architecture

```
Frontend (React + Vite + Tailwind)
         ↕️ REST API
Backend (Python FastAPI + LangChain)
         ↕️ Google Sheets API
    Google Sheets (n8n writes here)
```

**Extensible Design**: 
- Add n8n webhooks without code changes
- Modify data structure easily
- Swap data sources (Sheets → Database)
- Add new analytics calculations

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.11+ and Node.js 18+
- OpenAI API Key: https://platform.openai.com/api-keys
- Google Service Account with Sheets API enabled
- Google Sheet shared with service account

### 1. Clone & Setup

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies  
cd ../frontend
npm install
```

### 2. Get API Keys

**OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy it (starts with `sk-`)

**Google Service Account:**
1. Go to https://console.cloud.google.com/
2. Create project → Enable "Google Sheets API"
3. Create Service Account → Download JSON credentials
4. Save as `backend/credentials.json`
5. Copy service account email from JSON file
6. Share your Google Sheet with this email (Viewer access)

### 3. Configure

Create `backend/.env`:

```env
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_SHEET_IDS=your_sheet_id_from_url
GOOGLE_SHEET_GID=1186874097  # Optional: specific worksheet GID
GOOGLE_CREDENTIALS_FILE=credentials.json
PORT=8000
FRONTEND_URL=http://localhost:5173
```

### 4. Run

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

Open **http://localhost:5173** 🎉

---

## 📖 Usage

### Dashboard Tab
- View analytics summary
- See trend distribution charts
- Check top performers by ADX
- Read AI-generated insights

### Stocks Tab
- Browse all stocks from Google Sheets
- Filter by trend, strength, volatility
- Filter by sentiment score and ADX
- View detailed stock cards

### AI Chat Tab
- Ask: "Which stocks have strong uptrends?"
- Ask: "Show me high volatility stocks"
- Ask: "What's the average sentiment?"
- Natural language interface powered by OpenAI

---

## 🔧 Configuration

### Multiple Google Sheets

```env
GOOGLE_SHEET_IDS=sheet_id_1,sheet_id_2,sheet_id_3
```

### Specific Worksheet (by GID)

Get GID from URL: `...#gid=1186874097`

```env
GOOGLE_SHEET_GID=1186874097
```

### Change AI Model

Edit `backend/services/ai_chat.py`:

```python
self.llm = ChatOpenAI(
    model="gpt-4o-mini",  # or "gpt-4", "gpt-4o"
    temperature=0.3
)
```

---

## 🚀 Cloud Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete Google Cloud Run deployment guide.

**Quick deploy:**
```bash
gcloud run deploy trading-analytics-dashboard \
  --source . \
  --region europe-west2 \
  --allow-unauthenticated
```

---

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app & endpoints
│   ├── models.py            # Data models (Pydantic)
│   ├── requirements.txt     # Python dependencies
│   ├── credentials.json     # Google credentials (gitignored)
│   └── services/
│       ├── sheets_sync.py   # Google Sheets integration
│       ├── analytics.py     # Data analysis & filtering
│       └── ai_chat.py       # LangChain + OpenAI chat
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main app component
│   │   ├── components/      # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── StockCard.jsx
│   │   │   ├── Filters.jsx
│   │   │   └── ChatInterface.jsx
│   │   └── services/
│   │       └── api.js       # API client
│   ├── package.json
│   └── vite.config.js
│
├── Dockerfile               # Multi-stage Docker build
├── cloudbuild.yaml         # Auto-deploy on git push
└── .dockerignore
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/sync` | POST | Sync data from Google Sheets |
| `/api/stocks` | GET | Get all stocks (with filters) |
| `/api/analytics` | GET | Get analytics summary |
| `/api/chat` | POST | Chat with AI about data |
| `/api/insights` | GET | Get AI-generated insights |
| `/api/sync-status` | GET | Check sync status |

**Full API docs**: http://localhost:8000/docs (auto-generated)

---

## 🛠️ Extending the System

### Adding New Data Fields

1. Update Google Sheet columns
2. Add field to `backend/models.py`:
```python
class StockData(BaseModel):
    rsi: Optional[float] = None  # Add this
```
3. Frontend automatically displays new fields

### Adding New Analytics

Create new method in `backend/services/analytics.py`:
```python
@staticmethod
def calculate_risk_score(data: List[Dict]) -> Dict:
    # Your logic here
    pass
```

### n8n Integration

**Option 1**: n8n writes to Google Sheets (no code changes!)

**Option 2**: Add webhook endpoint:
```python
@app.post("/api/webhook/n8n")
async def receive_n8n_data(data: dict):
    global stock_data_cache
    stock_data_cache[data['sheet_id']] = data['stocks']
    return {"status": "success"}
```

---

## 🐛 Troubleshooting

**"Authentication failed"**
- Check service account has Sheet access
- Verify credentials.json is in backend folder

**"No data available"**
- Click "Sync Data" button first
- Check Google Sheet ID in .env
- Verify Sheet is shared with service account

**"Connection refused"**
- Backend running? Check terminal
- Correct ports? (Backend:8000, Frontend:5173)

**"Module not found"**
```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

---

## 📊 Data Format

Expected Google Sheet columns:
```
Symbol, Timeframe, EMA50, EMA200, ATR, Price, atrPercentage, 
ADX, Trend, Trend_strength, Volatility, qualifiedFilter, 
Date, Stock, sentimentScore, Rational
```

**Column names are flexible** - the system handles variations (case-insensitive).

---

## 🎯 Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- LangChain - AI orchestration
- OpenAI GPT-4o-mini - Natural language processing
- gspread - Google Sheets API
- Pandas - Data analysis

**Frontend:**
- React 18 - UI library
- Vite - Build tool & dev server
- Tailwind CSS - Styling
- Recharts - Data visualization
- Axios - API client

**Deployment:**
- Docker - Containerization
- Cloud Run - Serverless hosting
- Cloud Build - CI/CD pipeline

---

## 📝 License

MIT License - feel free to modify and use for your projects.

---

## 🆘 Need Help?

1. Check `DEPLOYMENT.md` for cloud deployment
2. View API docs: http://localhost:8000/docs
3. Check browser console (F12) for frontend errors
4. Check terminal for backend errors

---

**Built with ❤️ for trading analytics and AI-powered insights**
