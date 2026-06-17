import apiClient from './api';

export default {
  getDashboard() {
    return apiClient.get('/admin/dashboard');
  },
  getUTMStats() {
    return apiClient.get('/admin/utm-stats');
  },
};