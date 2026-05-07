import apiClient from './api';

export default {
  createOrder() {
    return apiClient.post('/orders/');
  },
  getMyOrders() {
    return apiClient.get('/orders/');
  },
  getOrder(id) {
    return apiClient.get(`/orders/${id}`);
  },
  updateOrderStatus(id, status) {
    return apiClient.patch(`/orders/${id}/status`, { status });
  }
};