"""
AI Chat Service using LangChain & OpenAI
Optimized with structured output and caching
"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import json
from typing import Dict, List, Optional
import pandas as pd
from functools import lru_cache
import hashlib


class FilterParams(BaseModel):
    """Structured filter parameters extracted from query"""
    trend: Optional[str] = Field(None, description="uptrend or downtrend")
    trend_strength: Optional[str] = Field(None, description="strong, developing, or weak")
    volatility: Optional[str] = Field(None, description="high, moderate, or low")
    sentiment: Optional[str] = Field(None, description="positive, negative, or neutral")
    sort_by: str = Field("adx", description="Column to sort by: volatility, sentiment, or adx")
    limit: int = Field(10, description="Number of results to return")


class AIChatService:
    """Handle natural language queries about trading data - optimized version"""
    
    def __init__(self, openai_api_key: str):
        """Initialize with OpenAI API key"""
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4o-mini",  # Fast and cost-effective
            temperature=0.3  # More focused responses
        )
        # Create parser for structured output
        self.filter_parser = PydanticOutputParser(pydantic_object=FilterParams)
    
    def query(self, user_message: str, stock_data: List[Dict]) -> Dict:
        """
        Process user's natural language query about stocks
        NOW OPTIMIZED: Single LLM call with structured output
        
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
            
            # Convert data to DataFrame
            df = pd.DataFrame(stock_data)
            
            # Check cache first (avoid LLM call if possible)
            cache_key = self._get_cache_key(user_message, len(df))
            cached_result = self._get_cached_response(cache_key)
            if cached_result:
                print("✅ Cache hit - returning cached response")
                # Still apply filters to fresh data
                relevant_stocks = self._apply_smart_filters(df, cached_result['filters'])
                if relevant_stocks:
                    relevant_stocks = self._clean_data_for_json(relevant_stocks)
                return {
                    "response": cached_result['response'],
                    "data": relevant_stocks
                }
            
            # Create data summary for context
            data_summary = self._create_data_summary(df)
            
            # OPTIMIZED: Single LLM call with structured output
            filter_params, ai_response = self._query_with_structured_output(
                user_message, 
                data_summary, 
                len(df)
            )
            
            # Apply filters to get relevant stocks
            relevant_stocks = None
            if filter_params:
                relevant_stocks = self._apply_smart_filters(df, filter_params)
            else:
                # If no filters specified, return top 10 by ADX (default)
                relevant_stocks = self._get_default_stocks(df)
            
            # Clean data for JSON
            if relevant_stocks:
                relevant_stocks = self._clean_data_for_json(relevant_stocks)
            
            # Cache the result (filters + response text)
            self._cache_response(cache_key, {
                'filters': filter_params,
                'response': ai_response
            })
            
            return {
                "response": ai_response,
                "data": relevant_stocks
            }
            
        except Exception as e:
            print(f"❌ Error in AI chat: {str(e)}")
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "data": None
            }
    
    def _get_cache_key(self, query: str, data_size: int) -> str:
        """Generate cache key from query and data size"""
        content = f"{query.lower().strip()}_{data_size}"
        return hashlib.md5(content.encode()).hexdigest()
    
    @lru_cache(maxsize=100)
    def _get_cached_response(self, cache_key: str) -> Optional[Dict]:
        """Get cached response (in-memory cache)"""
        # LRU cache automatically handles storage
        return None  # First call always returns None, then caches
    
    def _cache_response(self, cache_key: str, result: Dict):
        """Cache the response"""
        # Store in the function's cache by calling it
        self._get_cached_response.__wrapped__(cache_key, result)
    
    def _query_with_structured_output(self, query: str, data_summary: str, total_stocks: int) -> tuple:
        """
        OPTIMIZED: Single LLM call that returns both filters and response
        Uses structured output to extract parameters
        """
        try:
            # Build comprehensive prompt that returns structured data
            prompt = f"""You are a trading analyst assistant. Analyze the query and provide:
1. Filter parameters (if query asks for specific stocks)
2. A helpful response to the user

Available data: {total_stocks} stocks
{data_summary}

User Query: "{query}"

IMPORTANT: If the user asks for specific stocks (e.g., "top 10 by volatility", "stocks with positive sentiment"), 
extract the appropriate filter parameters. Otherwise, just answer their question.

Filter Parameters to extract:
- trend: "uptrend" or "downtrend" (if mentioned)
- trend_strength: "strong", "developing", or "weak" (if mentioned)
- volatility: "high", "moderate", or "low" (if mentioned)
- sentiment: "positive", "negative", or "neutral" (if mentioned)
- sort_by: "volatility", "sentiment", or "adx" (what to sort by)
- limit: number of stocks requested (default 10)

Respond with JSON in this format:
{{
    "filters": {{
        "trend": null or "uptrend"/"downtrend",
        "volatility": null or "high"/"moderate"/"low",
        "sentiment": null or "positive"/"negative",
        "sort_by": "adx" or "volatility" or "sentiment",
        "limit": 10
    }},
    "response": "Your helpful answer to the user"
}}"""

            messages = [
                SystemMessage(content="You extract filters and provide helpful responses. Always return valid JSON."),
                HumanMessage(content=prompt)
            ]
            
            # Call LLM once
            result = self.llm.invoke(messages)
            
            # Parse JSON response
            import re
            json_match = re.search(r'\{.*\}', result.content, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                filters = parsed.get('filters', {})
                response_text = parsed.get('response', result.content)
                
                # Clean up filters (remove null values)
                clean_filters = {k: v for k, v in filters.items() if v is not None}
                
                print(f"📊 Extracted filters: {clean_filters}")
                return clean_filters, response_text
            
            # Fallback if JSON parsing fails
            return {}, result.content
            
        except Exception as e:
            print(f"⚠️ Error in structured query: {str(e)}")
            # Fallback to simple response
            return {}, f"I understand your question. {str(e)}"
    
    def _apply_smart_filters(self, df: pd.DataFrame, filter_params: Dict) -> List[Dict]:
        """
        Apply extracted filter parameters to dataframe
        """
        try:
            if not filter_params:
                return None
            
            filtered_df = df.copy()
            
            # Apply trend filter
            if filter_params.get('trend'):
                trend_col = self._find_column(filtered_df, ['trend'])
                if trend_col:
                    filtered_df = filtered_df[
                        filtered_df[trend_col].astype(str).str.lower().str.contains(
                            filter_params['trend'].lower(), na=False
                        )
                    ]
            
            # Apply trend strength filter
            if filter_params.get('trend_strength'):
                strength_col = self._find_column(filtered_df, ['trend_strength', 'trendstrength'])
                if strength_col:
                    filtered_df = filtered_df[
                        filtered_df[strength_col].astype(str).str.lower().str.contains(
                            filter_params['trend_strength'].lower(), na=False
                        )
                    ]
            
            # Apply volatility filter
            if filter_params.get('volatility'):
                vol_col = self._find_column(filtered_df, ['volatility'])
                if vol_col:
                    filtered_df = filtered_df[
                        filtered_df[vol_col].astype(str).str.lower().str.contains(
                            filter_params['volatility'].lower(), na=False
                        )
                    ]
            
            # Apply sentiment filter
            if filter_params.get('sentiment'):
                sentiment_col = self._find_column(filtered_df, ['sentimentscore', 'sentiment_score', 'sentiment'])
                if sentiment_col:
                    filtered_df[sentiment_col] = pd.to_numeric(filtered_df[sentiment_col], errors='coerce')
                    if filter_params['sentiment'].lower() == 'positive':
                        filtered_df = filtered_df[filtered_df[sentiment_col] > 0]
                    elif filter_params['sentiment'].lower() == 'negative':
                        filtered_df = filtered_df[filtered_df[sentiment_col] < 0]
            
            # Sort by requested column
            sort_by = filter_params.get('sort_by', 'adx')
            if sort_by and sort_by != 'none':
                sort_col = None
                if sort_by == 'volatility':
                    # For volatility, map text to numeric for sorting
                    vol_col = self._find_column(filtered_df, ['volatility'])
                    if vol_col:
                        vol_map = {'high': 3, 'moderate': 2, 'low': 1}
                        filtered_df['vol_numeric'] = filtered_df[vol_col].astype(str).str.lower().map(vol_map)
                        sort_col = 'vol_numeric'
                elif sort_by == 'sentiment':
                    sort_col = self._find_column(filtered_df, ['sentimentscore', 'sentiment_score'])
                    if sort_col:
                        filtered_df[sort_col] = pd.to_numeric(filtered_df[sort_col], errors='coerce')
                elif sort_by == 'adx':
                    sort_col = self._find_column(filtered_df, ['adx', 'adx '])
                    if sort_col:
                        filtered_df[sort_col] = pd.to_numeric(filtered_df[sort_col], errors='coerce')
                
                if sort_col:
                    filtered_df = filtered_df.nlargest(filter_params.get('limit', 10), sort_col)
            
            # Apply limit
            limit = filter_params.get('limit', 10)
            filtered_df = filtered_df.head(limit)
            
            if not filtered_df.empty:
                return filtered_df.to_dict('records')
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error applying smart filters: {str(e)}")
            return None
    
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

    def _get_default_stocks(self, df: pd.DataFrame, limit: int = 10) -> List[Dict]:
        """
        Return default stocks when no specific filters are requested
        Sorts by ADX (trend strength) to show most active stocks
        """
        try:
            adx_col = self._find_column(df, ['adx', 'adx '])
            if adx_col:
                df[adx_col] = pd.to_numeric(df[adx_col], errors='coerce')
                result_df = df.nlargest(limit, adx_col)
                return result_df.to_dict('records')
            else:
                # Fallback to first N stocks if ADX column not found
                return df.head(limit).to_dict('records')
        except Exception as e:
            print(f"⚠️ Error getting default stocks: {str(e)}")
            return df.head(limit).to_dict('records')
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> str:
        """Helper to find column by possible name variations"""
        for col in df.columns:
            col_clean = col.lower().replace('_', '').replace(' ', '')
            for name in possible_names:
                if col_clean == name.lower().replace('_', '').replace(' ', ''):
                    return col
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
