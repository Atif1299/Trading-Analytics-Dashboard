/**
 * Stock Card Component
 * Clean display of individual stock information
 */
import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Activity, ChevronDown, ChevronUp } from 'lucide-react';

const StockCard = ({ stock }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const isUptrend = stock.Trend?.toLowerCase() === 'uptrend' || stock.trend?.toLowerCase() === 'uptrend';
  const symbol = stock.Symbol || stock.symbol || 'N/A';
  const price = stock.Price || stock.price;
  const trend = stock.Trend || stock.trend || 'N/A';
  const trendStrength = stock.Trend_strength || stock.trend_strength || stock.trendStrength || 'N/A';
  const volatility = stock.Volatility || stock.volatility || 'N/A';
  const adx = stock.ADX || stock['ADX '] || stock.adx;
  const sentiment = stock.sentimentScore || stock.sentiment_score;
  const sentimentText = stock.sentiment;  // New: text sentiment (bullish/bearish/neutral)

  return (
    <div className="card hover:scale-[1.02] transition-transform">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg ${isUptrend ? 'bg-green-100' : 'bg-red-100'}`}>
            {isUptrend ? (
              <TrendingUp className="w-5 h-5 text-green-600" />
            ) : (
              <TrendingDown className="w-5 h-5 text-red-600" />
            )}
          </div>
          <div>
            <h3 className="text-lg font-bold">{symbol}</h3>
            {price && <p className="text-sm text-gray-500">${parseFloat(price).toFixed(2)}</p>}
          </div>
        </div>
        
        <div className="flex gap-2">
          {/* Sentiment Text Badge (bullish/bearish/neutral) */}
          {sentimentText && (
            <div className={`badge ${
              sentimentText.toLowerCase() === 'bullish' ? 'badge-green' :
              sentimentText.toLowerCase() === 'bearish' ? 'badge-red' :
              'badge-blue'
            }`}>
              {sentimentText.charAt(0).toUpperCase() + sentimentText.slice(1)}
            </div>
          )}
          
          {/* Sentiment Score Badge (numeric) */}
          {sentiment !== undefined && sentiment !== null && sentiment !== '' && (
            <div className={`badge ${parseFloat(sentiment) > 0 ? 'badge-green' : parseFloat(sentiment) < 0 ? 'badge-red' : 'badge-blue'}`}>
              Score: {parseFloat(sentiment).toFixed(2)}
            </div>
          )}
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-gray-50 p-3 rounded-lg">
          <p className="text-xs text-gray-500 mb-1">Trend</p>
          <p className={`font-semibold ${isUptrend ? 'text-green-600' : 'text-red-600'}`}>
            {trend}
          </p>
        </div>

        <div className="bg-gray-50 p-3 rounded-lg">
          <p className="text-xs text-gray-500 mb-1">Strength</p>
          <p className="font-semibold text-gray-900">
            {trendStrength}
          </p>
        </div>

        {adx && (
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-xs text-gray-500 mb-1">ADX</p>
            <p className="font-semibold text-gray-900">
              {parseFloat(adx).toFixed(2)}
            </p>
          </div>
        )}

        <div className="bg-gray-50 p-3 rounded-lg">
          <p className="text-xs text-gray-500 mb-1">Volatility</p>
          <p className={`font-semibold ${
            volatility.toLowerCase() === 'high' ? 'text-orange-600' : 
            volatility.toLowerCase() === 'low' ? 'text-blue-600' : 
            'text-gray-900'
          }`}>
            {volatility}
          </p>
        </div>
      </div>

      {/* Rational (if available) */}
      {stock.rational && stock.rational.trim() !== '' && (
        <div className="mt-3 pt-3 border-t">
          <div className="flex items-start justify-between gap-2">
            <p className={`text-xs text-gray-600 flex-1 ${!isExpanded ? 'line-clamp-2' : ''}`}>
              {stock.rational}
            </p>
            {stock.rational.length > 100 && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="text-primary-600 hover:text-primary-700 flex-shrink-0"
                aria-label={isExpanded ? 'Show less' : 'Show more'}
              >
                {isExpanded ? (
                  <ChevronUp className="w-4 h-4" />
                ) : (
                  <ChevronDown className="w-4 h-4" />
                )}
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default StockCard;
