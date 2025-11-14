# 📊 Trading Analytics System

A professional, full-stack trading analytics platform that syncs with Google Sheets, provides AI-powered insights, and displays beautiful interactive dashboards.

## ✨ Features

- 🔄 **Real-time Google Sheets Sync** - Automatically fetch trading data from multiple Google Sheets
- 🤖 **AI-Powered Chat** - Ask questions in natural language using OpenAI & LangChain
- 📈 **Interactive Dashboards** - Beautiful charts showing trends, sentiment, and performance
- 🔍 **Advanced Filtering** - Filter stocks by trend, strength, volatility, sentiment, and ADX
- 💼 **Professional UI** - Clean, modern interface perfect for business presentations
- 🚀 **Fast & Simple** - Easy to set up, clean code, fully documented

## 🏗️ Architecture

```
Frontend (React + Vite + Tailwind CSS)
         ↕️ REST API
Backend (Python + FastAPI + LangChain)
         ↕️ Google Sheets API
    Google Sheets (Your n8n Data)
```

## 📋 Prerequisites

- **Python 3.8+** installed
- **Node.js 18+** and npm installed
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Google Cloud Project** with Sheets API enabled
- **Google Service Account** credentials JSON file

## 🚀 Quick Start

### 1️⃣ Backend Setup

#### Step 1: Install Python Dependencies

```cmd
cd backend
pip install -r requirements.txt
```

#### Step 2: Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Sheets API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

4. Create Service Account:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Fill in name and click "Create"
   - Skip optional steps and click "Done"

5. Download Credentials:
   - Click on the service account you created
   - Go to "Keys" tab
   - Click "Add Key" → "Create New Key"
   - Select "JSON" and click "Create"
   - Save the downloaded file as `credentials.json` in the `backend` folder

6. Share your Google Sheet with the service account email (found in credentials.json)

#### Step 3: Configure Environment Variables

Create a `.env` file in the `backend` folder:

```cmd
copy .env.example .env
```

Edit `.env` and add your credentials:

```env
# Your OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Your Google Sheet IDs (comma-separated for multiple sheets)
# Get the ID from the URL: https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
GOOGLE_SHEET_IDS=your_sheet_id_here

# Path to your credentials file
GOOGLE_CREDENTIALS_FILE=credentials.json

# Server settings (default values are fine)
PORT=8000
HOST=0.0.0.0
FRONTEND_URL=http://localhost:5173
```

#### Step 4: Start the Backend Server

```cmd
python main.py
```

You should see:
```
✅ Successfully authenticated with Google Sheets
✅ AI Chat service initialized
✨ Server ready!
🚀 Starting server on 0.0.0.0:8000
```

### 2️⃣ Frontend Setup

Open a **new terminal** window:

#### Step 1: Install Dependencies

```cmd
cd frontend
npm install
```

#### Step 2: Configure Environment

Create `.env` file:

```cmd
copy .env.example .env
```

The default configuration should work:

```env
VITE_API_URL=http://localhost:8000
```

#### Step 3: Start the Frontend

```cmd
npm run dev
```

The app will open at: **http://localhost:5173**

## 📖 Usage Guide

### Initial Setup

1. **Start both servers** (backend and frontend)
2. **Click "Sync Data"** button in the top-right corner
3. Wait for data to sync from your Google Sheet
4. Explore the dashboard! 🎉

### Dashboard Tab

- View **market overview** with key metrics
- See **trend distribution** pie chart
- Analyze **top performers** by ADX
- Get **AI-generated insights** about the market

### Stocks Tab

- **Filter stocks** by multiple criteria:
  - Trend (uptrend/downtrend)
  - Trend strength (strong/developing/weak)
  - Volatility (high/moderate/low)
  - Minimum sentiment score
  - Minimum ADX value
- View detailed **stock cards** with all metrics
- See sentiment analysis and rationale

### AI Chat Tab

- Ask questions in natural language:
  - "Show me strong uptrend stocks"
  - "What's the average sentiment?"
  - "List high volatility stocks"
  - "Which stocks have sentiment above 0.5?"
- Get instant AI-powered responses
- View relevant stock data automatically

## 🔧 Configuration

### Multiple Google Sheets

To work with multiple sheets, add all sheet IDs to `.env`:

```env
GOOGLE_SHEET_IDS=sheet_id_1,sheet_id_2,sheet_id_3
```

The system will automatically combine data from all sheets.

### Changing the OpenAI Model

Edit `backend/services/ai_chat.py`:

```python
self.llm = ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-4",  # Change to "gpt-4", "gpt-3.5-turbo", etc.
    temperature=0.3
)
```

## 🎨 Customization

### Colors & Branding

Edit `frontend/tailwind.config.js` to change the color scheme:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Change these values to your brand colors
        500: '#0ea5e9',
        600: '#0284c7',
        // ...
      },
    },
  },
}
```

### Chart Styles

Charts are in `frontend/src/components/Dashboard.jsx` using Recharts library.

## 📁 Project Structure

```
Trading System/
├── backend/
│   ├── main.py                 # FastAPI server & API routes
│   ├── models.py               # Data models (Pydantic)
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (create this)
│   ├── credentials.json        # Google credentials (add this)
│   └── services/
│       ├── sheets_sync.py      # Google Sheets integration
│       ├── ai_chat.py          # LangChain + OpenAI chat
│       └── analytics.py        # Data processing & analytics
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main application component
│   │   ├── main.jsx            # React entry point
│   │   ├── index.css           # Global styles (Tailwind)
│   │   ├── components/
│   │   │   ├── Dashboard.jsx   # Analytics dashboard
│   │   │   ├── ChatInterface.jsx # AI chat component
│   │   │   ├── Filters.jsx     # Filtering controls
│   │   │   └── StockCard.jsx   # Individual stock display
│   │   └── services/
│   │       └── api.js          # API service (axios)
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md                   # This file
```

## 🐛 Troubleshooting

### Backend Issues

**"Authentication failed"**
- Make sure `credentials.json` is in the `backend` folder
- Verify you've enabled Google Sheets API in Google Cloud Console
- Check that the service account email has access to your sheet

**"OpenAI API key not found"**
- Ensure you've set `OPENAI_API_KEY` in `.env`
- Verify the API key is valid at https://platform.openai.com/

**"No data available"**
- Click the "Sync Data" button to fetch data from Google Sheets
- Check that `GOOGLE_SHEET_IDS` is set correctly in `.env`
- Verify the sheet format matches the expected columns

### Frontend Issues

**"Failed to fetch"**
- Make sure the backend server is running (python main.py)
- Check that `VITE_API_URL` in frontend `.env` points to the correct backend URL
- Look for CORS errors in browser console

**Charts not displaying**
- Ensure data has been synced successfully
- Check browser console for any errors

### Common Errors

**Port already in use**
```cmd
# Backend (change PORT in .env)
PORT=8001

# Frontend (change port in vite.config.js)
server: { port: 5174 }
```

**Module not found**
```cmd
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## 🚢 Deployment

### Backend (Railway/Render/Heroku)

1. Create a new project
2. Connect your GitHub repository
3. Set environment variables in the dashboard
4. Add `credentials.json` as a secret file
5. Deploy!

### Frontend (Vercel/Netlify)

1. Build the frontend:
   ```cmd
   cd frontend
   npm run build
   ```

2. Deploy the `dist` folder to Vercel/Netlify
3. Set environment variable: `VITE_API_URL=https://your-backend-url.com`

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/sync` - Sync data from Google Sheets
- `GET /api/stocks` - Get stocks with filters
- `GET /api/analytics` - Get analytics summary
- `POST /api/chat` - Chat with AI
- `GET /api/insights` - Get quick insights

## 🤝 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the code comments (everything is well-documented)
3. Inspect browser console and backend logs for errors

## 📝 Notes for Your UK Client

- ✅ **Professional Design** - Clean, modern UI suitable for business presentations
- ✅ **Easy to Use** - Intuitive interface, no technical knowledge required
- ✅ **Scalable** - Supports multiple Google Sheets, thousands of stocks
- ✅ **AI-Powered** - Natural language queries make data analysis effortless
- ✅ **Real-time** - Data syncs on-demand, always up-to-date
- ✅ **Secure** - No data stored permanently, all processing in real-time

## 🎉 You're All Set!

Start the servers and begin analyzing your trading data with AI-powered insights!

```cmd
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

Then visit: **http://localhost:5173** 🚀
