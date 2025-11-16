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
        Extract stocks relevant to the query using expanded keyword matching
        """
        try:
            query_lower = query.lower()
            filtered_df = df.copy()
            filter_applied = False
            
            # Expanded keyword mapping for better matching
            filter_keywords = {
                # Uptrend synonyms
                ('uptrend', 'bullish', 'rising', 'up trend', 'going up', 'increasing'): ('Trend', 'uptrend'),
                # Downtrend synonyms
                ('downtrend', 'bearish', 'falling', 'down trend', 'going down', 'decreasing'): ('Trend', 'downtrend'),
                # Strong trend synonyms
                ('strong', 'powerful', 'strongest', 'high strength'): ('Trend_strength', 'strong'),
                # High volatility synonyms
                ('high volatility', 'volatile', 'high vol', 'unstable'): ('Volatility', 'high'),
                # Moderate volatility
                ('moderate volatility', 'medium volatility', 'moderate vol'): ('Volatility', 'moderate'),
                # Low volatility
                ('low volatility', 'stable', 'low vol'): ('Volatility', 'low'),
                # Positive sentiment
                ('positive sentiment', 'good sentiment', 'bullish sentiment', 'optimistic'): ('sentimentScore', lambda x: x > 0),
                # Negative sentiment
                ('negative sentiment', 'bad sentiment', 'bearish sentiment', 'pessimistic'): ('sentimentScore', lambda x: x < 0),
            }
            
            # Apply filters based on keyword matches
            for keywords, (column, value) in filter_keywords.items():
                if any(keyword in query_lower for keyword in keywords):
                    # Find the actual column name (handle case variations)
                    col_name = None
                    for col in filtered_df.columns:
                        if col.lower().replace('_', '').replace(' ', '') == column.lower().replace('_', '').replace(' ', ''):
                            col_name = col
                            break
                    
                    if col_name:
                        if callable(value):
                            # Handle lambda functions for numeric comparisons
                            filtered_df[col_name] = pd.to_numeric(filtered_df[col_name], errors='coerce')
                            filtered_df = filtered_df[filtered_df[col_name].apply(value)]
                        else:
                            # String matching (case insensitive)
                            filtered_df = filtered_df[filtered_df[col_name].astype(str).str.lower().str.contains(value.lower(), na=False)]
                        filter_applied = True
            
            # Handle ADX-related queries
            if any(word in query_lower for word in ['high adx', 'strong adx', 'adx above', 'adx >', 'adx greater']):
                adx_col = self._find_column(filtered_df, ['adx', 'adx '])
                if adx_col:
                    filtered_df[adx_col] = pd.to_numeric(filtered_df[adx_col], errors='coerce')
                    # Filter ADX > 25 for "high ADX"
                    filtered_df = filtered_df[filtered_df[adx_col] > 25]
                    filter_applied = True
            
            # Handle "top", "best", "strongest" queries
            if any(word in query_lower for word in ['top', 'best', 'strongest', 'highest', 'leading']):
                adx_col = self._find_column(filtered_df, ['adx', 'adx '])
                if adx_col:
                    filtered_df[adx_col] = pd.to_numeric(filtered_df[adx_col], errors='coerce')
                    filtered_df = filtered_df.nlargest(10, adx_col)
                    filter_applied = True
            
            # Handle "show", "list", "get", "find" queries - return sample stocks
            if any(word in query_lower for word in ['show', 'list', 'get', 'find', 'which', 'what']) and not filter_applied:
                # If no specific filter but user is asking for stocks, return top 10 by ADX
                adx_col = self._find_column(filtered_df, ['adx', 'adx '])
                if adx_col:
                    filtered_df[adx_col] = pd.to_numeric(filtered_df[adx_col], errors='coerce')
                    filtered_df = filtered_df.nlargest(10, adx_col)
                    filter_applied = True
                else:
                    # Just return first 10 if no ADX
                    filtered_df = filtered_df.head(10)
                    filter_applied = True
            
            # Return filtered results
            if filter_applied and not filtered_df.empty:
                return filtered_df.head(20).to_dict('records')  # Max 20 stocks
            
            # If filter was applied but no results, return None (let AI explain)
            if filter_applied and filtered_df.empty:
                return None
            
            # If no filter and generic query, return None (AI will just answer)
            return None
            
        except Exception as e:
            print(f"⚠️ Error extracting relevant stocks: {str(e)}")
            return None
    
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
