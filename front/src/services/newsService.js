import apiClient from './api';

export default {
  getNews(params) {
    return apiClient.get('/news/', { params });
  },
  createNews(data) {
    return apiClient.post('/news/', data);
  },
  updateNews(id, data) {
    return apiClient.put(`/news/${id}`, data);
  },
  deleteNews(id) {
    return apiClient.delete(`/news/${id}`);
  }
};