"""
Simple data models for the trading system
Clean and easy to understand
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class StockData(BaseModel):
    """Individual stock information from Google Sheets"""
    symbol: str
    timeframe: str
    ema50: Optional[float] = None
    ema200: Optional[float] = None
    atr: Optional[float] = None
    price: Optional[float] = None
    atr_percentage: Optional[float] = Field(None, alias="atrPercentage")
    adx: Optional[float] = None
    trend: Optional[str] = None
    trend_strength: Optional[str] = Field(None, alias="trendStrength")
    volatility: Optional[str] = None
    qualified_filter: Optional[str] = Field(None, alias="qualifiedFilter")
    date: Optional[str] = None
    stock: Optional[str] = None
    sentiment_score: Optional[float] = Field(None, alias="sentimentScore")
    rational: Optional[str] = None

    class Config:
        populate_by_name = True


class ChatRequest(BaseModel):
    """User's chat message"""
    message: str
    sheet_id: Optional[str] = None  # Which sheet to query


class ChatResponse(BaseModel):
    """AI's response"""
    response: str
    data: Optional[List[dict]] = None  # Filtered stock data if applicable


class AnalyticsSummary(BaseModel):
    """Overall market analytics"""
    total_stocks: int
    uptrend_count: int
    downtrend_count: int
    avg_sentiment: float
    strong_trends: int
    high_volatility_count: int
    top_performers: List[dict]
    
    
class SyncStatus(BaseModel):
    """Google Sheets sync status"""
    last_sync: Optional[datetime] = None
    total_records: int
    status: str  # 'success', 'error', 'syncing'
    message: Optional[str] = None


class Alert(BaseModel):
    """TradingView Alert from Google Sheets"""
    symbol: str = Field(..., alias="Symbol")
    exchange: Optional[str] = Field(None, alias="Exchange")
    indicator: str = Field(..., alias="Indicator")
    price: Optional[float] = Field(None, alias="Price")
    volume: Optional[float] = Field(None, alias="Volumn")  # Note: Handling 'Volumn' typo from sheet
    timeframe: Optional[str] = Field(None, alias="Timeframe")
    alert_time: str = Field(..., alias="Alert_Time")
    status: Optional[str] = Field(None, alias="Status")

    class Config:
        populate_by_name = True

