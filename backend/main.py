"""
FastAPI Backend - Simple and Clean
Trading Analytics System API
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
from typing import Optional, List
from datetime import datetime
from pathlib import Path

# Import our services
from services.sheets_sync import GoogleSheetsSync, to_dataframe
from services.analytics import AnalyticsService
from services.ai_chat import AIChatService
from models import ChatRequest, ChatResponse, AnalyticsSummary, SyncStatus

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="Trading Analytics API",
    description="Simple API for analyzing trading data from Google Sheets",
    version="1.0.0"
)

# Configure CORS (allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
sheets_sync = None
ai_chat = None
analytics = AnalyticsService()

# In-memory cache for stock data
stock_data_cache = {}
last_sync_time = None


@app.on_event("startup")
async def startup_event():
    """Initialize services when server starts"""
    global sheets_sync, ai_chat
    
    print("🚀 Starting Trading Analytics API...")
    
    # Initialize Google Sheets
    # Check for Cloud Run env variable first, then local file
    creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    
    if creds_json:
        # Cloud Run: env variable contains JSON
        sheets_sync = GoogleSheetsSync(credentials_file=None)
        print("✅ Google Sheets service initialized (using GOOGLE_CREDENTIALS_JSON)")
    elif os.path.exists(credentials_file):
        # Local: use credentials file
        sheets_sync = GoogleSheetsSync(credentials_file)
        print("✅ Google Sheets service initialized (using credentials file)")
    else:
        print("⚠️ Google credentials not found. Set GOOGLE_CREDENTIALS_JSON env var or add credentials.json")
    
    # Initialize AI Chat
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        ai_chat = AIChatService(openai_key)
        print("✅ AI Chat service initialized")
    else:
        print("⚠️ OpenAI API key not found. Chat features will be limited.")
    
    print("✨ Server ready!")


# Mount static files (for production/Cloud Run)
# This serves the React frontend build
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")
    print("✅ Serving frontend static files")


@app.get("/")
async def root():
    """Health check endpoint or serve frontend"""
    # If static frontend exists, serve it
    index_file = Path(__file__).parent / "static" / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    
    # Otherwise return API info (for development)
    return {
        "status": "running",
        "message": "Trading Analytics API is live! 🚀",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/sheets")
async def list_sheets():
    """Get list of configured Google Sheets"""
    sheet_ids = os.getenv("GOOGLE_SHEET_IDS", "").split(",")
    sheet_ids = [sid.strip() for sid in sheet_ids if sid.strip()]
    
    sheets_info = []
    for sheet_id in sheet_ids:
        if sheets_sync:
            info = sheets_sync.get_sheet_info(sheet_id)
            sheets_info.append({
                "id": sheet_id,
                **info
            })
        else:
            sheets_info.append({"id": sheet_id, "title": "Unknown"})
    
    return {"sheets": sheets_info}


@app.post("/api/sync")
async def sync_data(sheet_id: Optional[str] = None):
    """
    Sync data from Google Sheets
    If sheet_id is provided, sync that specific sheet
    Otherwise, sync all configured sheets
    """
    global stock_data_cache, last_sync_time
    
    if not sheets_sync:
        raise HTTPException(status_code=500, detail="Google Sheets service not initialized")
    
    try:
        # Get worksheet GID if specified
        worksheet_gid = os.getenv("GOOGLE_SHEET_GID", None)
        
        if sheet_id:
            # Sync specific sheet
            data = sheets_sync.fetch_sheet_data(sheet_id, worksheet_gid=worksheet_gid)
            stock_data_cache[sheet_id] = data
        else:
            # Sync all sheets
            sheet_ids = os.getenv("GOOGLE_SHEET_IDS", "").split(",")
            sheet_ids = [sid.strip() for sid in sheet_ids if sid.strip()]
            
            for sid in sheet_ids:
                data = sheets_sync.fetch_sheet_data(sid, worksheet_gid=worksheet_gid)
                stock_data_cache[sid] = data
        
        last_sync_time = datetime.now()
        total_records = sum(len(data) for data in stock_data_cache.values())
        
        return SyncStatus(
            last_sync=last_sync_time,
            total_records=total_records,
            status="success",
            message=f"Successfully synced {total_records} records"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@app.get("/api/stocks")
async def get_stocks(
    sheet_id: Optional[str] = None,
    trend: Optional[str] = Query(None, description="Filter by trend (uptrend/downtrend)"),
    trend_strength: Optional[str] = Query(None, description="Filter by strength"),
    volatility: Optional[str] = Query(None, description="Filter by volatility"),
    min_sentiment: Optional[float] = Query(None, description="Minimum sentiment score"),
    min_adx: Optional[float] = Query(None, description="Minimum ADX value")
):
    """
    Get stock data with optional filters
    """
    # Get data (from specific sheet or combine all)
    if sheet_id and sheet_id in stock_data_cache:
        data = stock_data_cache[sheet_id]
    elif stock_data_cache:
        # Combine all sheets
        data = []
        for sheet_data in stock_data_cache.values():
            data.extend(sheet_data)
    else:
        return {"stocks": [], "message": "No data available. Please sync first."}
    
    # Apply filters if provided
    filters = {}
    if trend:
        filters['trend'] = trend
    if trend_strength:
        filters['trend_strength'] = trend_strength
    if volatility:
        filters['volatility'] = volatility
    if min_sentiment is not None:
        filters['min_sentiment'] = min_sentiment
    if min_adx is not None:
        filters['min_adx'] = min_adx
    
    if filters:
        data = analytics.filter_stocks(data, filters)
    
    return {
        "stocks": data,
        "total": len(data),
        "filters_applied": filters
    }


@app.get("/api/analytics")
async def get_analytics(sheet_id: Optional[str] = None):
    """Get analytics summary of the trading data"""
    
    # Get data
    if sheet_id and sheet_id in stock_data_cache:
        data = stock_data_cache[sheet_id]
    elif stock_data_cache:
        data = []
        for sheet_data in stock_data_cache.values():
            data.extend(sheet_data)
    else:
        raise HTTPException(status_code=404, detail="No data available. Please sync first.")
    
    # Calculate analytics
    summary = analytics.calculate_summary(data)
    
    return summary


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Chat with AI about the trading data
    Ask questions in natural language
    """
    if not ai_chat:
        raise HTTPException(status_code=500, detail="AI Chat service not available. Please configure OpenAI API key.")
    
    # Get data
    if request.sheet_id and request.sheet_id in stock_data_cache:
        data = stock_data_cache[request.sheet_id]
    elif stock_data_cache:
        data = []
        for sheet_data in stock_data_cache.values():
            data.extend(sheet_data)
    else:
        return ChatResponse(
            response="I don't have any data to analyze yet. Please sync the Google Sheets first.",
            data=None
        )
    
    # Process with AI
    result = ai_chat.query(request.message, data)
    
    return ChatResponse(
        response=result['response'],
        data=result.get('data')
    )


@app.get("/api/insights")
async def get_insights(sheet_id: Optional[str] = None):
    """Get quick AI-generated insights about the market"""
    if not ai_chat:
        return {"insights": "AI insights not available"}
    
    # Get data
    if sheet_id and sheet_id in stock_data_cache:
        data = stock_data_cache[sheet_id]
    elif stock_data_cache:
        data = []
        for sheet_data in stock_data_cache.values():
            data.extend(sheet_data)
    else:
        return {"insights": "No data available"}
    
    insights = ai_chat.get_quick_insights(data)
    
    return {"insights": insights}


@app.get("/api/sync-status")
async def get_sync_status():
    """Get current sync status"""
    total_records = sum(len(data) for data in stock_data_cache.values())
    
    return SyncStatus(
        last_sync=last_sync_time,
        total_records=total_records,
        status="success" if stock_data_cache else "no_data",
        message=f"{total_records} records in cache" if stock_data_cache else "No data synced yet"
    )


@app.get("/api/alerts")
async def get_alerts():
    """Get TradingView alerts from Google Sheets"""
    if not sheets_sync:
        raise HTTPException(status_code=500, detail="Sheets service not initialized")
    
    try:
        # Get the first sheet ID from env
        sheet_ids = os.getenv("GOOGLE_SHEET_IDS", "").split(",")
        if not sheet_ids or not sheet_ids[0]:
            raise HTTPException(status_code=500, detail="No Google Sheet ID configured")
            
        main_sheet_id = sheet_ids[0].strip()
        
        # Fetch from TradingView_Alerts sheet
        # We don't cache alerts as they might be updated frequently by n8n
        alerts_data = sheets_sync.fetch_sheet_data(
            main_sheet_id,
            worksheet_name="TradingView_Alerts"
        )
        
        return {"alerts": alerts_data, "total": len(alerts_data)}
        
    except Exception as e:
        print(f"❌ Error fetching alerts: {str(e)}")
        # Return empty list instead of erroring out if sheet doesn't exist yet
        return {"alerts": [], "total": 0, "message": "Could not fetch alerts. Ensure 'TradingView_Alerts' sheet exists."}



# Run the server
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True  # Auto-reload on code changes (disable in production)
    )
