/**
 * Filters Component
 * Simple and clean filtering controls
 */
import React from 'react';
import { Filter, X } from 'lucide-react';

const Filters = ({ filters, setFilters, onApply, onReset }) => {
  const handleChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const activeFiltersCount = Object.values(filters).filter(v => v !== '' && v !== null).length;

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-bold">Filters</h3>
          {activeFiltersCount > 0 && (
            <span className="badge badge-blue">{activeFiltersCount} active</span>
          )}
        </div>
        {activeFiltersCount > 0 && (
          <button
            onClick={onReset}
            className="text-sm text-gray-600 hover:text-gray-900 flex items-center gap-1"
          >
            <X className="w-4 h-4" />
            Reset
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Trend Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Trend
          </label>
          <select
            value={filters.trend || ''}
            onChange={(e) => handleChange('trend', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All</option>
            <option value="uptrend">Uptrend</option>
            <option value="downtrend">Downtrend</option>
          </select>
        </div>

        {/* Trend Strength Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Trend Strength
          </label>
          <select
            value={filters.trend_strength || ''}
            onChange={(e) => handleChange('trend_strength', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All</option>
            <option value="strong">Strong</option>
            <option value="developing">Developing</option>
            <option value="weak">Weak</option>
          </select>
        </div>

        {/* Volatility Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Volatility
          </label>
          <select
            value={filters.volatility || ''}
            onChange={(e) => handleChange('volatility', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All</option>
            <option value="high">High</option>
            <option value="moderate">Moderate</option>
            <option value="low">Low</option>
          </select>
        </div>

        {/* Sentiment Filter (Text: neutral, bearish, bullish) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Sentiment
          </label>
          <select
            value={filters.sentiment || ''}
            onChange={(e) => handleChange('sentiment', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All</option>
            <option value="bullish">Bullish</option>
            <option value="neutral">Neutral</option>
            <option value="bearish">Bearish</option>
          </select>
        </div>

        {/* Min Sentiment */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Min Sentiment Score
          </label>
          <input
            type="number"
            step="0.1"
            min="-1"
            max="1"
            value={filters.min_sentiment || ''}
            onChange={(e) => handleChange('min_sentiment', e.target.value ? parseFloat(e.target.value) : null)}
            placeholder="e.g., 0.3"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        {/* Min ADX */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Min ADX
          </label>
          <input
            type="number"
            step="1"
            min="0"
            value={filters.min_adx || ''}
            onChange={(e) => handleChange('min_adx', e.target.value ? parseFloat(e.target.value) : null)}
            placeholder="e.g., 25"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
      </div>

      <div className="mt-4 flex gap-3">
        <button onClick={onApply} className="btn-primary flex-1">
          Apply Filters
        </button>
      </div>
    </div>
  );
};

export default Filters;
