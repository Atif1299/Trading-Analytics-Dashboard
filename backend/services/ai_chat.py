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
            
            # Step 1: Use LLM to extract filter parameters from user query
            filter_params = self._llm_extract_filters(user_message, df)
            
            # Step 2: Apply filters to get relevant stocks
            relevant_stocks = self._apply_smart_filters(df, filter_params)
            
            # Step 3: Create context with filtered data for AI response
            data_summary = self._create_data_summary(df)
            filtered_summary = ""
            if relevant_stocks:
                filtered_summary = f"\n\nFiltered Results: {len(relevant_stocks)} stocks matching criteria"
            
            # Build the prompt
            system_prompt = f"""You are a helpful trading analyst assistant. 
            
You have access to the following stock trading data:

{data_summary}{filtered_summary}

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
    
    def _llm_extract_filters(self, query: str, df: pd.DataFrame) -> Dict:
        """
        Use LLM to intelligently extract filter parameters from natural language query
        """
        try:
            # Get available columns
            columns_info = ", ".join(df.columns.tolist())
            
            extraction_prompt = f"""Analyze this trading query and extract filter parameters.

Available data columns: {columns_info}

User Query: "{query}"

Extract the following if mentioned:
1. trend: "uptrend" or "downtrend"
2. trend_strength: "strong", "developing", or "weak"
3. volatility: "high", "moderate", or "low"
4. sentiment: "positive", "negative", or "neutral"
5. sort_by: what to sort by ("volatility", "sentiment", "adx", "none")
6. limit: how many results (default 10)

Return ONLY a JSON object with these keys. Use null for unspecified values.
Example: {{"trend": "uptrend", "volatility": "high", "sort_by": "adx", "limit": 10}}"""

            messages = [
                SystemMessage(content="You are a parameter extraction assistant. Return only valid JSON."),
                HumanMessage(content=extraction_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse JSON response
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                filters = json.loads(json_match.group())
                print(f"📊 LLM extracted filters: {filters}")
                return filters
            
            return {}
            
        except Exception as e:
            print(f"⚠️ Error extracting filters with LLM: {str(e)}")
            return {}
    
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
