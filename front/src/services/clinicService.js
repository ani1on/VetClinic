import apiClient from './api';

export default {
  getAbout() {
    return apiClient.get('/clinic/about');
  },
  updateAbout(data) {
    return apiClient.put('/clinic/admin/clinic/about', data);
  }
};