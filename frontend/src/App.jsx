/**
 * Main App Component
 * Simple, clean, and professional trading analytics interface
 */
import React, { useState, useEffect } from 'react';
import { BarChart3, MessageSquare, Filter as FilterIcon, RefreshCw, Database } from 'lucide-react';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import Filters from './components/Filters';
import StockCard from './components/StockCard';
import apiService from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [analytics, setAnalytics] = useState(null);
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [syncStatus, setSyncStatus] = useState(null);
  const [filters, setFilters] = useState({
    trend: '',
    trend_strength: '',
    volatility: '',
    min_sentiment: null,
    min_adx: null
  });

  // Fetch initial data on mount
  useEffect(() => {
    checkSyncStatus();
  }, []);

  const checkSyncStatus = async () => {
    try {
      const status = await apiService.getSyncStatus();
      setSyncStatus(status);
      
      if (status.total_records > 0) {
        fetchAnalytics();
        fetchStocks();
      }
    } catch (error) {
      console.error('Failed to check sync status:', error);
    }
  };

  const handleSync = async () => {
    setLoading(true);
    try {
      const result = await apiService.syncData();
      setSyncStatus(result);
      
      // Fetch fresh data after sync
      await fetchAnalytics();
      await fetchStocks();
      
      alert('✅ Data synced successfully!');
    } catch (error) {
      console.error('Sync failed:', error);
      alert('❌ Sync failed. Please check your backend configuration.');
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const data = await apiService.getAnalytics();
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStocks = async (appliedFilters = {}) => {
    setLoading(true);
    try {
      // Clean filters (remove empty values)
      const cleanFilters = {};
      Object.keys(appliedFilters).forEach(key => {
        if (appliedFilters[key] !== '' && appliedFilters[key] !== null) {
          cleanFilters[key] = appliedFilters[key];
        }
      });

      const data = await apiService.getStocks(cleanFilters);
      setStocks(data.stocks || []);
    } catch (error) {
      console.error('Failed to fetch stocks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyFilters = () => {
    fetchStocks(filters);
  };

  const handleResetFilters = () => {
    const resetFilters = {
      trend: '',
      trend_strength: '',
      volatility: '',
      min_sentiment: null,
      min_adx: null
    };
    setFilters(resetFilters);
    fetchStocks(resetFilters);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header - Made Sticky */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary-600 rounded-lg">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Trading Analytics</h1>
                <p className="text-sm text-gray-500">Professional Market Analysis System</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {/* Sync Status */}
              {syncStatus && (
                <div className="text-sm text-gray-600">
                  <span className="font-medium">{syncStatus.total_records}</span> records
                  {syncStatus.last_sync && (
                    <span className="ml-2 text-gray-400">
                      • Last sync: {new Date(syncStatus.last_sync).toLocaleTimeString()}
                    </span>
                  )}
                </div>
              )}

              {/* Sync Button */}
              <button
                onClick={handleSync}
                disabled={loading}
                className="btn-primary flex items-center gap-2"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                Sync Data
              </button>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="flex gap-2 mt-4">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'dashboard'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              Dashboard
            </button>

            <button
              onClick={() => setActiveTab('stocks')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'stocks'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Database className="w-4 h-4" />
              Stocks
            </button>

            <button
              onClick={() => setActiveTab('chat')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'chat'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              AI Chat
            </button>
          </div>
        </div>
      </header>

      {/* Main Content - Added padding top to prevent content going behind sticky header */}
      <main className="max-w-7xl mx-auto px-4 py-8 pt-4">
        {activeTab === 'dashboard' && (
          <Dashboard analytics={analytics} loading={loading} />
        )}

        {activeTab === 'stocks' && (
          <div className="space-y-6">
            {/* Filters */}
            <Filters
              filters={filters}
              setFilters={setFilters}
              onApply={handleApplyFilters}
              onReset={handleResetFilters}
            />

            {/* Stock Count */}
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">
                {stocks.length} Stock{stocks.length !== 1 ? 's' : ''} Found
              </h2>
            </div>

            {/* Stock Grid */}
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
              </div>
            ) : stocks.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {stocks.map((stock, index) => (
                  <StockCard key={index} stock={stock} />
                ))}
              </div>
            ) : (
              <div className="card text-center py-12">
                <FilterIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No stocks found. Try adjusting your filters or sync data first.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'chat' && (
          <ChatInterface />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-gray-500">
          <p>Trading Analytics System • Built with React + FastAPI + LangChain</p>
          <p className="mt-1">Professional trading analysis for smarter decisions</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
