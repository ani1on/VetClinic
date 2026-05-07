// src/services/serviceService.js
import apiClient from './api';

export default {
  getServices(params) { return apiClient.get('/services/', { params }); },
  getService(id)      { return apiClient.get(`/services/${id}`); },
  createService(data) { return apiClient.post('/services/', data); },
  updateService(id, data) { return apiClient.put(`/services/${id}`, data); },
  deleteService(id)   { return apiClient.delete(`/services/${id}`); },
};