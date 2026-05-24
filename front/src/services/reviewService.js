import apiClient from './api';

export default {
  getReviews(params) {
    return apiClient.get('/reviews/', { params });
  },
  createReview(data) {
    return apiClient.post('/reviews/', data);
  },
  moderateReview(id, status) {
    return apiClient.patch(`/reviews/${id}/moderate`, { status });
  },
   deleteReview(id) {
    return apiClient.delete(`/reviews/${id}`);
  },

};