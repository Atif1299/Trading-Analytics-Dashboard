# 🚀 GETTING STARTED - Read This First!

## 👋 Welcome!

You now have a **complete trading analytics system** with:
- ✅ Python backend (FastAPI + AI)
- ✅ React frontend (beautiful UI)
- ✅ Google Sheets integration
- ✅ AI chat assistant
- ✅ Complete documentation

## ⚡ Quick Start (5 Minutes)

### Step 1: Get Your API Keys

#### OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. **Copy the key** (starts with `sk-`)
5. Save it somewhere safe!

#### Google Service Account
1. Go to: https://console.cloud.google.com/
2. Create a new project (or use existing)
3. Click "☰" menu → "APIs & Services" → "Library"
4. Search "Google Sheets API" → Click → "Enable"
5. Go back to "APIs & Services" → "Credentials"
6. Click "Create Credentials" → "Service Account"
7. Give it a name → Click "Create"
8. Skip optional steps → Click "Done"
9. Click on the service account you just created
10. Go to "Keys" tab → "Add Key" → "Create New Key"
11. Select "JSON" → Click "Create"
12. **File downloads automatically** (this is `credentials.json`)
13. **Copy the email** from the JSON file (looks like: `something@project.iam.gserviceaccount.com`)

#### Share Your Google Sheet
1. Open your Google Sheet with trading data
2. Click "Share" button
3. Paste the service account email
4. Give it "Viewer" access
5. Click "Send"

#### Get Your Sheet ID
1. Look at your Google Sheet URL
2. Copy the part between `/d/` and `/edit`
3. Example: `https://docs.google.com/spreadsheets/d/COPY_THIS_PART/edit`

### Step 2: Setup the System

#### Option A: Automatic (Recommended)
```cmd
1. Double-click: setup.bat
2. Wait for installation to complete
```

#### Option B: Manual
```cmd
# Backend
cd backend
pip install -r requirements.txt
copy .env.example .env

# Frontend  
cd frontend
npm install
copy .env.example .env
```

### Step 3: Configure

#### Edit Backend Config
1. Open `backend/.env` in Notepad
2. Replace with your values:

```env
OPENAI_API_KEY=sk-your-actual-key-here
GOOGLE_SHEET_IDS=your-actual-sheet-id-here
GOOGLE_CREDENTIALS_FILE=credentials.json
```

3. Save the file

#### Add Google Credentials
1. Move the downloaded `credentials.json` file
2. Place it in the `backend` folder
3. Make sure it's named exactly `credentials.json`

### Step 4: Start!

#### Option A: Automatic (Recommended)
```cmd
Double-click: start.bat
```

#### Option B: Manual
```cmd
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Step 5: Use It!

1. Browser opens automatically at: http://localhost:5173
2. Click the **"Sync Data"** button (top-right)
3. Wait 5 seconds for data to load
4. Explore!
   - **Dashboard tab**: See analytics & charts
   - **Stocks tab**: Filter and browse stocks
   - **AI Chat tab**: Ask questions!

## 🎯 First Things to Try

### In Dashboard Tab
- Look at the market insights banner (AI-generated!)
- Check the trend distribution pie chart
- See top performers in the bar chart

### In Stocks Tab
- Click filters to narrow down stocks
- Try filtering by "Uptrend" and "Strong"
- View individual stock cards with all metrics

### In AI Chat Tab
- Type: "Show me strong uptrend stocks"
- Try: "What's the average sentiment?"
- Ask: "Which stocks have high volatility?"

## ❓ Common First-Time Issues

### "Module not found" Error
**Solution**: Run setup again
```cmd
setup.bat
```

### "Authentication failed"
**Solution**: Check 3 things:
1. Is `credentials.json` in the `backend` folder?
2. Did you enable Google Sheets API?
3. Did you share the sheet with the service account email?

### "No data available"
**Solution**: Click the "Sync Data" button!

### "Connection refused"
**Solution**: Make sure backend is running
```cmd
cd backend
python main.py
```

### "Port already in use"
**Solution**: Close other apps using ports 8000 or 5173
Or change ports in:
- Backend: `backend/.env` → `PORT=8001`
- Frontend: `frontend/vite.config.js` → `port: 5174`

## 📚 Next Steps

### Learn More
- Read `CLIENT_GUIDE.md` for detailed usage
- Check `QUICK_REFERENCE.md` for commands
- See `UI_PREVIEW.md` for design overview

### Customize
- Change colors: `frontend/tailwind.config.js`
- Modify charts: `frontend/src/components/Dashboard.jsx`
- Adjust AI: `backend/services/ai_chat.py`

### Deploy (Make it Public)
- See `README.md` deployment section
- Backend: Railway, Render, or Heroku
- Frontend: Vercel or Netlify

## 🆘 Need Help?

### Check These Files
1. `README.md` - Complete technical guide
2. `CLIENT_GUIDE.md` - User-friendly guide
3. `QUICK_REFERENCE.md` - Quick commands
4. `SYSTEM_OVERVIEW.md` - Architecture details

### Look at the Code
- Backend is in: `backend/`
- Frontend is in: `frontend/src/`
- Everything is well-commented!

### Check Browser Console
- Press F12 in browser
- Look for error messages
- Copy them to search online

### Check Backend Logs
- Look at the terminal running `python main.py`
- Error messages will show there

## ✅ Checklist Before You Start

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] OpenAI API key obtained
- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] Service account created
- [ ] `credentials.json` downloaded
- [ ] Google Sheet shared with service account
- [ ] Sheet ID copied
- [ ] `setup.bat` completed
- [ ] `backend/.env` configured
- [ ] `credentials.json` in backend folder
- [ ] `start.bat` launched
- [ ] Browser opened to localhost:5173
- [ ] "Sync Data" button clicked
- [ ] Data loaded successfully!

## 🎉 You're Ready!

Everything is set up and ready to use. Your trading analytics system is:

✅ **Professional** - Perfect for UK business presentations
✅ **AI-Powered** - Natural language queries
✅ **Real-time** - Syncs with Google Sheets
✅ **Beautiful** - Modern, clean UI
✅ **Simple** - Easy to use and maintain

**Start analyzing your trading data now! 📊🚀**

---

### Quick Access

**Start System**: `start.bat`
**Frontend**: http://localhost:5173
**Backend API**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

**Questions?** Check the documentation files!
