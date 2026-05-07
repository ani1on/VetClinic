import apiClient from './api';

export default {
  getProfile() {
    return apiClient.get('/users/profile');
  },
  updateProfile(data) {
    return apiClient.put('/users/profile', data);
  },
  // админские методы (если нужно)
  getUser(userId) {
    return apiClient.get(`/users/${userId}`);
  },
  listUsers(params) {
    return apiClient.get('/users/', { params });
  }
};