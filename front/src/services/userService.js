import apiClient from './api';

export default {
  getProfile() {
    return apiClient.get('/users/profile');
  },
  updateProfile(data) {
    return apiClient.put('/users/profile', data);
  },
  getUser(userId) {
    return apiClient.get(`/users/${userId}`);
  },
  listUsers(params) {
    return apiClient.get('/users/', { params });
  },
  updateUserRole(userId, data) {
  return apiClient.patch(`/users/${userId}/role`, data);
},
deleteUser(userId) {
  return apiClient.delete(`/users/${userId}`);
}
};