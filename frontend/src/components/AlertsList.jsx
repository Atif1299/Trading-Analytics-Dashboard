/**
 * AlertsList Component
 * Displays real-time alerts from TradingView/n8n
 */
import React, { useState, useEffect } from 'react';
import { Bell, ExternalLink, Clock, Activity } from 'lucide-react';
import apiService from '../services/api';

const AlertsList = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAlerts = async () => {
    try {
      const data = await apiService.getAlerts();
      // Sort by date descending (newest first) - with robust parsing
      const sortedAlerts = (data.alerts || []).sort((a, b) => {
        const dateA = new Date(a.Alert_Time || 0);
        const dateB = new Date(b.Alert_Time || 0);
        return dateB - dateA; // Newest first
      });
      setAlerts(sortedAlerts);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch alerts:', err);
      setError('Failed to load alerts');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    // Poll for new alerts every 30 seconds
    const interval = setInterval(fetchAlerts, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading && alerts.length === 0) {
    return (
      <div className="card animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="space-y-3">
          <div className="h-12 bg-gray-100 rounded"></div>
          <div className="h-12 bg-gray-100 rounded"></div>
          <div className="h-12 bg-gray-100 rounded"></div>
        </div>
      </div>
    );
  }

  if (error && alerts.length === 0) {
    return null; // Hide if error and no data
  }

  if (alerts.length === 0) {
    return (
      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <Bell className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-bold">Recent Alerts</h3>
        </div>
        <div className="text-center py-8 text-gray-500">
          <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p>No alerts yet</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Bell className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-bold">Recent Alerts</h3>
          <span className="badge badge-blue">{alerts.length}</span>
        </div>
        <button 
          onClick={fetchAlerts}
          className="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          Refresh
        </button>
      </div>

      <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
        {alerts.map((alert, index) => (
          <div 
            key={index}
            className="p-3 bg-gray-50 rounded-lg border border-gray-100 hover:border-primary-200 transition-colors"
          >
            <div className="flex justify-between items-start mb-1">
              <div className="flex items-center gap-2">
                <span className="font-bold text-gray-900">{alert.Symbol}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  alert.Indicator?.includes('spike') ? 'bg-purple-100 text-purple-700' :
                  alert.Indicator?.includes('ATH') ? 'bg-green-100 text-green-700' :
                  'bg-blue-100 text-blue-700'
                }`}>
                  {alert.Indicator}
                </span>
              </div>
              <span className="text-xs text-gray-500 flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {new Date(alert.Alert_Time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
            
            <div className="flex justify-between items-end">
              <div className="text-sm text-gray-600">
                <span className="mr-3">Price: <span className="font-medium text-gray-900">${alert.Price}</span></span>
                {alert.Volumn && (
                  <span>Vol: <span className="font-medium text-gray-900">{(alert.Volumn / 1000).toFixed(1)}K</span></span>
                )}
              </div>
              <span className="text-xs text-gray-400">{alert.Timeframe}m</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertsList;
