import apiClient from './api';

export default {
  getAll(params) {
    return apiClient.get('/doctors/', { params });
  },
  getDoctor(id) {
    return apiClient.get(`/doctors/${id}`);
  },
  getSlots(doctorId, date) {
    return apiClient.get(`/doctors/${doctorId}/slots`, { params: { date } });
  },
  createDoctor(data) {
    return apiClient.post('/doctors/', data);
  },
  updateDoctor(id, data) {
    return apiClient.put(`/doctors/${id}`, data);
  },
  deleteDoctor(id) {
    return apiClient.delete(`/doctors/${id}`);
  },
};