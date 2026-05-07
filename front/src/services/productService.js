import apiClient from './api';

export default {
  getProducts(params) {
    return apiClient.get('/products/', { params });
  },
  getProduct(id) {
    return apiClient.get(`/products/${id}`);
  },
  createProduct(data) {
    return apiClient.post('/products/', data);
  },
  updateProduct(id, data) {
    return apiClient.put(`/products/${id}`, data);
  },
  updateStock(id, data) {
    return apiClient.patch(`/products/${id}/stock`, data);
  },
  deleteProduct(id) {
    return apiClient.delete(`/products/${id}`);
  }
};