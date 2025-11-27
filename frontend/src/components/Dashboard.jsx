/**
 * Dashboard Component
 * Main analytics overview with beautiful charts
 */
import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { TrendingUp, TrendingDown, Activity, AlertCircle, Zap } from 'lucide-react';
import apiService from '../services/api';

import AlertsList from './AlertsList';

const Dashboard = ({ analytics, loading }) => {
  const [insights, setInsights] = useState('');

  useEffect(() => {
    // Fetch AI insights
    const fetchInsights = async () => {
      try {
        const data = await apiService.getInsights();
        setInsights(data.insights);
      } catch (error) {
        console.error('Failed to fetch insights:', error);
      }
    };

    if (analytics) {
      fetchInsights();
    }
  }, [analytics]);

  if (loading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="card">
        <div className="text-center py-12">
          <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No data available. Please sync your Google Sheets first.</p>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const trendData = [
    { name: 'Uptrend', value: analytics.uptrend_count, color: '#10b981' },
    { name: 'Downtrend', value: analytics.downtrend_count, color: '#ef4444' },
  ];

  const topPerformersData = analytics.top_performers?.slice(0, 5).map(stock => ({
    name: stock.symbol,
    score: stock.score,
    adx: stock.adx
  })) || [];

  return (
    <div className="space-y-6">
      {/* Insights Banner */}
      {insights && (
        <div className="bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-lg p-4 shadow-lg">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5" />
            <h3 className="font-bold">Market Insights</h3>
          </div>
          <p className="text-sm opacity-90">{insights}</p>
        </div>
      )}

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Stocks */}
        <div className="card bg-gradient-to-br from-blue-50 to-blue-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Stocks</p>
              <p className="text-3xl font-bold text-gray-900">{analytics.total_stocks}</p>
            </div>
            <Activity className="w-10 h-10 text-blue-600 opacity-50" />
          </div>
        </div>

        {/* Uptrend */}
        <div className="card bg-gradient-to-br from-green-50 to-green-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Uptrend</p>
              <p className="text-3xl font-bold text-green-700">{analytics.uptrend_count}</p>
              <p className="text-xs text-gray-600">
                {((analytics.uptrend_count / analytics.total_stocks) * 100).toFixed(1)}%
              </p>
            </div>
            <TrendingUp className="w-10 h-10 text-green-600 opacity-50" />
          </div>
        </div>

        {/* Downtrend */}
        <div className="card bg-gradient-to-br from-red-50 to-red-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Downtrend</p>
              <p className="text-3xl font-bold text-red-700">{analytics.downtrend_count}</p>
              <p className="text-xs text-gray-600">
                {((analytics.downtrend_count / analytics.total_stocks) * 100).toFixed(1)}%
              </p>
            </div>
            <TrendingDown className="w-10 h-10 text-red-600 opacity-50" />
          </div>
        </div>

        {/* Avg Sentiment */}
        <div className={`card bg-gradient-to-br ${
          analytics.avg_sentiment > 0 ? 'from-emerald-50 to-emerald-100' : 'from-orange-50 to-orange-100'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Avg Sentiment</p>
              <p className={`text-3xl font-bold ${
                analytics.avg_sentiment > 0 ? 'text-emerald-700' : 'text-orange-700'
              }`}>
                {analytics.avg_sentiment.toFixed(2)}
              </p>
              <p className="text-xs text-gray-600">
                {analytics.avg_sentiment > 0 ? 'Positive' : analytics.avg_sentiment < 0 ? 'Negative' : 'Neutral'}
              </p>
            </div>
            <div className={`text-4xl ${analytics.avg_sentiment > 0 ? 'text-emerald-600' : 'text-orange-600'} opacity-50`}>
              {analytics.avg_sentiment > 0 ? '😊' : analytics.avg_sentiment < 0 ? '😟' : '😐'}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid: Charts + Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Charts (Takes 2/3 width) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Trend Distribution Pie Chart */}
          <div className="card">
            <h3 className="text-lg font-bold mb-4">Trend Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={trendData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {trendData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Top Performers Bar Chart */}
          <div className="card">
            <h3 className="text-lg font-bold mb-4">Top Performers (by ADX)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topPerformersData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="adx" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right Column: Alerts (Takes 1/3 width) */}
        <div className="lg:col-span-1">
          <AlertsList />
        </div>
      </div>

      {/* Additional Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card text-center">
          <p className="text-sm text-gray-600 mb-2">Strong Trends</p>
          <p className="text-2xl font-bold text-primary-600">{analytics.strong_trends}</p>
          <p className="text-xs text-gray-500 mt-1">
            {((analytics.strong_trends / analytics.total_stocks) * 100).toFixed(1)}% of total
          </p>
        </div>

        <div className="card text-center">
          <p className="text-sm text-gray-600 mb-2">High Volatility</p>
          <p className="text-2xl font-bold text-orange-600">{analytics.high_volatility_count}</p>
          <p className="text-xs text-gray-500 mt-1">
            {((analytics.high_volatility_count / analytics.total_stocks) * 100).toFixed(1)}% of total
          </p>
        </div>

        <div className="card text-center">
          <p className="text-sm text-gray-600 mb-2">Top Performers</p>
          <p className="text-2xl font-bold text-green-600">{analytics.top_performers?.length || 0}</p>
          <p className="text-xs text-gray-500 mt-1">
            Based on ADX & sentiment
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
