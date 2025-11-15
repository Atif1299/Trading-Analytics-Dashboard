"""
Analytics Service
Simple data processing and calculations
"""
import pandas as pd
from typing import Dict, List
import numpy as np


class AnalyticsService:
    """Process and analyze trading data - keep it simple!"""
    
    @staticmethod
    def calculate_summary(data: List[Dict]) -> Dict:
        """
        Calculate overall market summary
        Returns key metrics in a simple dictionary
        """
        if not data:
            return {
                "total_stocks": 0,
                "uptrend_count": 0,
                "downtrend_count": 0,
                "avg_sentiment": 0,
                "strong_trends": 0,
                "high_volatility_count": 0,
                "top_performers": []
            }
        
        df = pd.DataFrame(data)
        
        # Debug: Print actual column names
        print(f"📊 DEBUG: Available columns: {list(df.columns)}")
        print(f"📊 DEBUG: First row sample: {df.iloc[0].to_dict() if len(df) > 0 else 'No data'}")
        
        # Count trends - handle different column name variations
        trend_col = 'Trend' if 'Trend' in df.columns else 'trend' if 'trend' in df.columns else None
        if trend_col:
            uptrend = len(df[df[trend_col].astype(str).str.lower() == 'uptrend'])
            downtrend = len(df[df[trend_col].astype(str).str.lower() == 'downtrend'])
        else:
            uptrend = 0
            downtrend = 0

        # Calculate average sentiment (handle missing values)
        sentiment_col = 'sentimentScore' if 'sentimentScore' in df.columns else 'sentiment_score' if 'sentiment_score' in df.columns else None
        if sentiment_col:
            avg_sentiment = pd.to_numeric(df[sentiment_col], errors='coerce').mean()
            if pd.isna(avg_sentiment):
                avg_sentiment = 0
        else:
            avg_sentiment = 0
        
        # Count strong trends
        strength_col = 'Trend_strength' if 'Trend_strength' in df.columns else 'trend_strength' if 'trend_strength' in df.columns else None
        if strength_col:
            strong_trends = len(df[df[strength_col].astype(str).str.lower() == 'strong'])
        else:
            strong_trends = 0
        
        # Count high volatility
        volatility_col = 'Volatility' if 'Volatility' in df.columns else 'volatility' if 'volatility' in df.columns else None
        if volatility_col:
            high_volatility = len(df[df[volatility_col].astype(str).str.lower() == 'high'])
        else:
            high_volatility = 0
        
        # Get top performers (high ADX + positive sentiment)
        top_performers = AnalyticsService._get_top_performers(df)
        
        return {
            "total_stocks": len(df),
            "uptrend_count": uptrend,
            "downtrend_count": downtrend,
            "avg_sentiment": round(float(avg_sentiment), 2),
            "strong_trends": strong_trends,
            "high_volatility_count": high_volatility,
            "top_performers": top_performers
        }
    
    @staticmethod
    def _get_top_performers(df: pd.DataFrame, top_n: int = 5) -> List[Dict]:
        """Find top performing stocks based on ADX and sentiment"""
        try:
            # Make a copy to avoid warnings
            analysis_df = df.copy()
            
            # Get ADX column (handle different naming)
            adx_col = 'ADX' if 'ADX' in analysis_df.columns else 'ADX ' if 'ADX ' in analysis_df.columns else 'adx'
            
            # Convert ADX to numeric
            if adx_col in analysis_df.columns:
                analysis_df['adx_numeric'] = pd.to_numeric(
                    analysis_df[adx_col].astype(str).str.strip(), 
                    errors='coerce'
                )
            else:
                analysis_df['adx_numeric'] = 0
            
            # Get sentiment score
            sentiment_col = 'sentimentScore' if 'sentimentScore' in analysis_df.columns else 'sentiment_score'
            if sentiment_col in analysis_df.columns:
                analysis_df['sentiment_numeric'] = pd.to_numeric(
                    analysis_df[sentiment_col], 
                    errors='coerce'
                )
            else:
                analysis_df['sentiment_numeric'] = 0
            
            # Fill NaN values
            analysis_df['adx_numeric'] = analysis_df['adx_numeric'].fillna(0)
            analysis_df['sentiment_numeric'] = analysis_df['sentiment_numeric'].fillna(0)
            
            # Calculate performance score (weighted)
            analysis_df['performance_score'] = (
                analysis_df['adx_numeric'] * 0.6 + 
                analysis_df['sentiment_numeric'] * 20  # Scale sentiment to 0-20
            )
            
            # Sort and get top performers
            top = analysis_df.nlargest(top_n, 'performance_score')
            
            # Return clean list
            symbol_col = 'Symbol' if 'Symbol' in top.columns else 'symbol'
            trend_col = 'Trend' if 'Trend' in top.columns else 'trend'
            
            result = []
            for _, row in top.iterrows():
                result.append({
                    "symbol": row.get(symbol_col, 'N/A'),
                    "adx": round(float(row['adx_numeric']), 2),
                    "sentiment": round(float(row['sentiment_numeric']), 2),
                    "trend": row.get(trend_col, 'N/A'),
                    "score": round(float(row['performance_score']), 2)
                })
            
            return result
            
        except Exception as e:
            print(f"⚠️ Error calculating top performers: {str(e)}")
            return []
    
    @staticmethod
    def filter_stocks(data: List[Dict], filters: Dict) -> List[Dict]:
        """
        Filter stocks based on criteria
        
        Supported filters:
        - trend: 'uptrend' or 'downtrend'
        - trend_strength: 'strong', 'weak', 'developing'
        - volatility: 'high', 'moderate', 'low'
        - min_sentiment: minimum sentiment score
        - max_sentiment: maximum sentiment score
        - min_adx: minimum ADX value
        """
        if not data:
            return []
        
        df = pd.DataFrame(data)
        result = df.copy()
        
        # Apply trend filter
        if 'trend' in filters and filters['trend']:
            trend_col = 'Trend' if 'Trend' in result.columns else 'trend' if 'trend' in result.columns else None
            if trend_col:
                result = result[result[trend_col].astype(str).str.lower() == filters['trend'].lower()]
        
        # Apply trend strength filter
        if 'trend_strength' in filters and filters['trend_strength']:
            strength_col = 'Trend_strength' if 'Trend_strength' in result.columns else 'trend_strength' if 'trend_strength' in result.columns else None
            if strength_col:
                result = result[result[strength_col].astype(str).str.lower() == filters['trend_strength'].lower()]
        
        # Apply volatility filter
        if 'volatility' in filters and filters['volatility']:
            vol_col = 'Volatility' if 'Volatility' in result.columns else 'volatility' if 'volatility' in result.columns else None
            if vol_col:
                result = result[result[vol_col].astype(str).str.lower() == filters['volatility'].lower()]
        
        # Apply sentiment filters
        sentiment_col = 'sentimentScore' if 'sentimentScore' in result.columns else 'sentiment_score'
        if sentiment_col in result.columns:
            result[sentiment_col] = pd.to_numeric(result[sentiment_col], errors='coerce')
            
            if 'min_sentiment' in filters:
                result = result[result[sentiment_col] >= filters['min_sentiment']]
            
            if 'max_sentiment' in filters:
                result = result[result[sentiment_col] <= filters['max_sentiment']]
        
        # Apply ADX filter
        adx_col = 'ADX' if 'ADX' in result.columns else 'ADX ' if 'ADX ' in result.columns else 'adx'
        if 'min_adx' in filters and adx_col in result.columns:
            result[adx_col] = pd.to_numeric(result[adx_col], errors='coerce')
            result = result[result[adx_col] >= filters['min_adx']]
        
        # Convert to dict and clean NaN/Infinity values
        records = result.to_dict('records')
        return AnalyticsService._clean_data_for_json(records)
    
    @staticmethod
    def _clean_data_for_json(data: List[Dict]) -> List[Dict]:
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
