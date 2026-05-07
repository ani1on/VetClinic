import apiClient from './api';

export default {
  getDashboard() {
    return apiClient.get('/admin/dashboard');
  }
};