/**
 * Stock Card Component
 * Clean display of individual stock information
 */
import React from 'react';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';

const StockCard = ({ stock }) => {
  const isUptrend = stock.Trend?.toLowerCase() === 'uptrend' || stock.trend?.toLowerCase() === 'uptrend';
  const symbol = stock.Symbol || stock.symbol || 'N/A';
  const price = stock.Price || stock.price;
  const trend = stock.Trend || stock.trend || 'N/A';
  const trendStrength = stock.Trend_strength || stock.trend_strength || stock.trendStrength || 'N/A';
  const volatility = stock.Volatility || stock.volatility || 'N/A';
  const adx = stock.ADX || stock['ADX '] || stock.adx;
  const sentiment = stock.sentimentScore || stock.sentiment_score;

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
        
        {sentiment !== undefined && sentiment !== null && sentiment !== '' && (
          <div className={`badge ${parseFloat(sentiment) > 0 ? 'badge-green' : parseFloat(sentiment) < 0 ? 'badge-red' : 'badge-blue'}`}>
            Sentiment: {parseFloat(sentiment).toFixed(2)}
          </div>
        )}
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
          <p className="text-xs text-gray-600 line-clamp-2">
            {stock.rational}
          </p>
        </div>
      )}
    </div>
  );
};

export default StockCard;
