import apiClient from './api';

export default {
  createAppointment(data) {
    return apiClient.post('/appointments/', data);
  },
  getMyAppointments() {
    return apiClient.get('/appointments/');
  },
  getAppointment(id) {
    return apiClient.get(`/appointments/${id}`);
  },
  updateAppointment(id, data) {
    return apiClient.put(`/appointments/${id}`, data);
  },
  updateStatus(id, status) {
    return apiClient.patch(`/appointments/${id}/status`, { status });
  },
  cancelAppointment(id) {
    return apiClient.delete(`/appointments/${id}`);
  },
  // admin
  getAllAppointments() {
    return apiClient.get('/appointments/admin/all');
  }
};