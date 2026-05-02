import apiClient from './api';

export default {
  register(data) {
    return apiClient.post('/auth/register', data);
  },
  login(data) {
    return apiClient.post('/auth/login', data);
  },
  refreshToken(refreshToken) {
    return apiClient.post('/auth/refresh', { refresh_token: refreshToken });
  },
  logout(refreshToken) {
    return apiClient.post('/auth/logout', { refresh_token: refreshToken });
  },
  forgotPassword(email) {
    return apiClient.post('/auth/forgot-password', { email });
  },
  resetPassword(token, newPassword) {
    return apiClient.post('/auth/reset-password', { token, new_password: newPassword });
  },
  getProfile() {
    return apiClient.get('/auth/me');
  },
};