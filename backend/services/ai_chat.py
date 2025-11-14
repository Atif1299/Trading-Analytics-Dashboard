"""
AI Chat Service using LangChain & OpenAI
Simple natural language interface for trading data
"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import json
from typing import Dict, List
import pandas as pd


class AIChatService:
    """Handle natural language queries about trading data"""
    
    def __init__(self, openai_api_key: str):
        """Initialize with OpenAI API key"""
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4o-mini",  # Fast and cost-effective
            temperature=0.3  # More focused responses
        )
    
    def query(self, user_message: str, stock_data: List[Dict]) -> Dict:
        """
        Process user's natural language query about stocks
        
        Args:
            user_message: User's question
            stock_data: Current stock data from Google Sheets
        
        Returns:
            Dictionary with 'response' and optionally 'data'
        """
        try:
            # Handle empty data
            if not stock_data or len(stock_data) == 0:
                return {
                    "response": "I don't have any data to analyze. Please sync the data first.",
                    "data": None
                }
            
            # Convert data to a readable format for the LLM
            df = pd.DataFrame(stock_data)
            
            # Create a summary of available data
            data_summary = self._create_data_summary(df)
            
            # Build the prompt
            system_prompt = f"""You are a helpful trading analyst assistant. 
            
You have access to the following stock trading data:

{data_summary}

Total stocks: {len(df)}

Answer the user's question based on this data. Be conversational and helpful.
If they ask for specific stocks or filters, provide clear information.
If you mention specific numbers or stats, be accurate based on the data.

Keep responses concise and professional."""

            # Create messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            # Get AI response
            response = self.llm.invoke(messages)
            
            # Try to extract relevant stocks if query is about specific criteria
            relevant_stocks = self._extract_relevant_stocks(user_message, df)
            
            # Clean the data to ensure JSON compatibility
            if relevant_stocks:
                relevant_stocks = self._clean_data_for_json(relevant_stocks)
            
            return {
                "response": response.content,
                "data": relevant_stocks
            }
            
        except Exception as e:
            print(f"❌ Error in AI chat: {str(e)}")
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "data": None
            }
    
    def _clean_data_for_json(self, data: List[Dict]) -> List[Dict]:
        """Clean data to ensure JSON compatibility (remove NaN, Infinity)"""
        import math
        
        cleaned_data = []
        for record in data:
            cleaned_record = {}
            for key, value in record.items():
                # Handle float values that aren't JSON compliant
                if isinstance(value, float):
                    if math.isnan(value) or math.isinf(value):
                        cleaned_record[key] = None
                    else:
                        cleaned_record[key] = value
                else:
                    cleaned_record[key] = value
            cleaned_data.append(cleaned_record)
        
        return cleaned_data
    
    def _create_data_summary(self, df: pd.DataFrame) -> str:
        """Create a concise summary of the data for the AI"""
        try:
            summary_parts = []
            
            # Trend distribution
            if 'Trend' in df.columns or 'trend' in df.columns:
                trend_col = 'Trend' if 'Trend' in df.columns else 'trend'
                trend_counts = df[trend_col].value_counts().to_dict()
                summary_parts.append(f"Trends: {trend_counts}")
            
            # Sentiment stats
            sentiment_col = 'sentimentScore' if 'sentimentScore' in df.columns else 'sentiment_score'
            if sentiment_col in df.columns:
                df[sentiment_col] = pd.to_numeric(df[sentiment_col], errors='coerce')
                avg_sentiment = df[sentiment_col].mean()
                if not pd.isna(avg_sentiment):
                    summary_parts.append(f"Avg Sentiment: {avg_sentiment:.2f}")
            
            # Sample symbols
            symbol_col = 'Symbol' if 'Symbol' in df.columns else 'symbol'
            if symbol_col in df.columns:
                symbols = df[symbol_col].head(10).tolist()
                summary_parts.append(f"Sample symbols: {', '.join(map(str, symbols))}")
            
            # Volatility distribution
            if 'Volatility' in df.columns or 'volatility' in df.columns:
                vol_col = 'Volatility' if 'Volatility' in df.columns else 'volatility'
                vol_counts = df[vol_col].value_counts().to_dict()
                summary_parts.append(f"Volatility: {vol_counts}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            print(f"⚠️ Error creating data summary: {str(e)}")
            return "Data summary unavailable"
    
    def _extract_relevant_stocks(self, query: str, df: pd.DataFrame) -> List[Dict]:
        """
        Try to extract stocks relevant to the query
        Simple keyword matching approach
        """
        try:
            query_lower = query.lower()
            
            # Keywords that suggest filtering
            filter_keywords = {
                'uptrend': ('Trend', 'uptrend'),
                'downtrend': ('Trend', 'downtrend'),
                'strong': ('Trend_strength', 'Strong'),
                'high volatility': ('Volatility', 'High'),
                'positive sentiment': ('sentimentScore', lambda x: x > 0),
            }
            
            # Check if query matches any filter keywords
            for keyword, (column, value) in filter_keywords.items():
                if keyword in query_lower:
                    # Find the actual column name (handle case variations)
                    col_name = None
                    for col in df.columns:
                        if col.lower() == column.lower():
                            col_name = col
                            break
                    
                    if col_name:
                        if callable(value):
                            # Handle lambda functions
                            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                            filtered = df[df[col_name].apply(value)]
                        else:
                            # Simple string matching
                            filtered = df[df[col_name].astype(str).str.contains(value, case=False, na=False)]
                        
                        if not filtered.empty:
                            return filtered.head(10).to_dict('records')
            
            # If no specific filter, return top stocks
            if any(word in query_lower for word in ['top', 'best', 'strongest']):
                adx_col = None
                for col in df.columns:
                    if col.lower().replace(' ', '') == 'adx':
                        adx_col = col
                        break
                
                if adx_col:
                    df[adx_col] = pd.to_numeric(df[adx_col], errors='coerce')
                    top_stocks = df.nlargest(5, adx_col)
                    return top_stocks.to_dict('records')
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error extracting relevant stocks: {str(e)}")
            return None
    
    def get_quick_insights(self, stock_data: List[Dict]) -> str:
        """Generate quick insights about the market"""
        try:
            if not stock_data or len(stock_data) == 0:
                return "No data available"
            
            df = pd.DataFrame(stock_data)
            insights = []
            
            # Trend insight
            trend_col = None
            for col in df.columns:
                if col.lower() == 'trend':
                    trend_col = col
                    break
            
            if trend_col:
                uptrend_pct = (df[trend_col].astype(str).str.lower() == 'uptrend').sum() / len(df) * 100
                insights.append(f"📈 {uptrend_pct:.0f}% of stocks are in uptrend")
            
            # Strong trends
            strength_col = None
            for col in df.columns:
                if col.lower() in ['trend_strength', 'trendstrength']:
                    strength_col = col
                    break
            
            if strength_col:
                strong_pct = (df[strength_col].astype(str).str.lower() == 'strong').sum() / len(df) * 100
                insights.append(f"💪 {strong_pct:.0f}% show strong trend strength")
            
            # Sentiment
            sentiment_col = None
            for col in df.columns:
                if col.lower() in ['sentimentscore', 'sentiment_score']:
                    sentiment_col = col
                    break
            
            if sentiment_col:
                df[sentiment_col] = pd.to_numeric(df[sentiment_col], errors='coerce')
                avg_sent = df[sentiment_col].mean()
                if not pd.isna(avg_sent):
                    if avg_sent > 0:
                        insights.append(f"😊 Average sentiment is positive ({avg_sent:.2f})")
                    elif avg_sent < 0:
                        insights.append(f"😟 Average sentiment is negative ({avg_sent:.2f})")
            
            return " | ".join(insights) if insights else "No insights available"
            
        except Exception as e:
            print(f"⚠️ Error generating insights: {str(e)}")
            return "Insights unavailable"
