# 🎯 Quick Start Guide - For Your UK Client

## What This System Does

This is a **professional trading analytics platform** that:
- ✅ Connects to your Google Sheets (where n8n stores trading data)
- ✅ Shows beautiful charts and analytics automatically
- ✅ Lets you ask questions in plain English using AI
- ✅ Filters and analyzes stocks instantly
- ✅ Works with multiple Google Sheets simultaneously

## 🚀 Super Quick Setup (5 Minutes)

### Step 1: Get Your Google Credentials

1. Go to: https://console.cloud.google.com/
2. Create a new project (or use existing)
3. Click "Enable APIs & Services"
4. Search "Google Sheets API" and enable it
5. Go to "Credentials" → "Create Credentials" → "Service Account"
6. Download the JSON file and save it as `credentials.json` in the `backend` folder

**Important:** Share your Google Sheet with the email from the credentials file (looks like: `something@your-project.iam.gserviceaccount.com`)

### Step 2: Get Your OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Create a new API key
3. Copy it (you'll need it in the next step)

### Step 3: Configure the System

1. Double-click `setup.bat` - this installs everything automatically
2. Open `backend/.env` in Notepad
3. Add your API keys:

```
OPENAI_API_KEY=sk-your-key-here
GOOGLE_SHEET_IDS=your-sheet-id-here
```

**To find your Sheet ID:**
- Open your Google Sheet
- Look at the URL: `https://docs.google.com/spreadsheets/d/COPY_THIS_PART/edit`
- Copy the long string between `/d/` and `/edit`

### Step 4: Start the System

1. Double-click `start.bat`
2. Two windows will open (backend and frontend)
3. Wait 10 seconds
4. Your browser will open at: http://localhost:5173

## 🎨 Using the System

### Dashboard Tab
- Overview of all your trading data
- Charts showing trends, sentiment, performance
- AI-generated insights

### Stocks Tab
- View all stocks in a clean card layout
- Filter by trend, strength, volatility, sentiment
- See detailed metrics for each stock

### AI Chat Tab
- Type questions in plain English:
  - "Show me stocks with strong uptrend"
  - "What's the average sentiment?"
  - "Which stocks have high volatility?"
- Get instant answers with relevant data

## 📊 Key Features for Presentations

1. **Professional Look** - Clean, modern design suitable for clients
2. **Real-time Data** - Click "Sync Data" button to refresh from Google Sheets
3. **Interactive Charts** - Hover over charts for detailed information
4. **AI-Powered** - Natural language queries impress clients
5. **Multiple Sheets** - Can handle data from multiple Google Sheets

## 🔄 Daily Workflow

1. Start the system: Double-click `start.bat`
2. Click "Sync Data" button (top-right)
3. Analyze your data using dashboard or filters
4. Ask AI questions about specific stocks
5. When done, close the terminal windows

## 🆘 If Something Goes Wrong

**"Authentication failed"**
- Make sure `credentials.json` is in the `backend` folder
- Check that you shared the sheet with the service account email

**"No data available"**
- Click the "Sync Data" button
- Check your `.env` file has the correct Sheet ID

**"Connection error"**
- Make sure both terminal windows (backend/frontend) are still open
- Restart by double-clicking `start.bat` again

## 💼 For Your UK Business Needs

This system is designed to:
- ✅ Look professional in client meetings
- ✅ Handle large amounts of trading data
- ✅ Provide instant insights without technical knowledge
- ✅ Scale as your business grows (multiple sheets, more stocks)
- ✅ Work offline (after initial sync)

## 📱 Accessing from Other Devices

**Same Network:**
- Backend: `http://YOUR_COMPUTER_IP:8000`
- Frontend: `http://YOUR_COMPUTER_IP:5173`

**Public Access:**
- Deploy to cloud (instructions in main README.md)
- Recommended: Vercel (frontend) + Railway (backend)

## 🎓 Tips for Best Results

1. **Keep Sheet Format Consistent** - The system expects these columns:
   - Symbol, Trend, Trend_strength, Volatility, ADX, sentimentScore, etc.

2. **Sync Regularly** - Click "Sync Data" whenever your n8n updates the sheet

3. **Use Filters** - Narrow down to specific stocks quickly

4. **Try AI Chat** - The AI can find patterns you might miss

5. **Show Clients** - Dashboard tab is perfect for presentations

## 🚀 You're Ready!

The system is now set up and ready to use. Just double-click `start.bat` whenever you need to analyze your trading data!

---

**Need Help?** Check the main README.md file for detailed technical documentation.
