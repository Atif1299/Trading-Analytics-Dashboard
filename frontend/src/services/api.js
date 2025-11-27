/**
 * API Service - Simple API calls to backend
 * Clean and easy to understand
 */
import axios from 'axios';

// In production (Cloud Run), use relative URL since frontend and backend are on same domain
// In development, use localhost:8000
const API_URL = import.meta.env.VITE_API_URL || 
  (window.location.hostname === 'localhost' ? 'http://localhost:8000' : '');

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Methods
export const apiService = {
  // Sync data from Google Sheets
  syncData: async (sheetId = null) => {
    const response = await api.post('/api/sync', null, {
      params: sheetId ? { sheet_id: sheetId } : {}
    });
    return response.data;
  },

  // Get all stocks with optional filters
  getStocks: async (filters = {}) => {
    const response = await api.get('/api/stocks', { params: filters });
    return response.data;
  },

  // Get analytics summary
  getAnalytics: async (sheetId = null) => {
    const response = await api.get('/api/analytics', {
      params: sheetId ? { sheet_id: sheetId } : {}
    });
    return response.data;
  },

  // Chat with AI
  chat: async (message, sheetId = null) => {
    const response = await api.post('/api/chat', {
      message,
      sheet_id: sheetId
    });
    return response.data;
  },

  // Get quick insights
  getInsights: async (sheetId = null) => {
    const response = await api.get('/api/insights', {
      params: sheetId ? { sheet_id: sheetId } : {}
    });
    return response.data;
  },

  // Get sync status
  getSyncStatus: async () => {
    const response = await api.get('/api/sync-status');
    return response.data;
  },

  // Get available sheets
  getSheets: async () => {
    const response = await api.get('/api/sheets');
    return response.data;
  },

  // Get TradingView alerts
  getAlerts: async () => {
    const response = await api.get('/api/alerts');
    return response.data;
  }
};

export default apiService;
