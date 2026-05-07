import apiClient from './api';

export default {
  getCart() {
    return apiClient.get('/cart/');
  },
  addItem(productId, quantity) {
    return apiClient.post('/cart/items', { product_id: productId, quantity });
  },
  updateItem(itemId, quantity) {
    return apiClient.put(`/cart/items/${itemId}`, { quantity });
  },
  removeItem(itemId) {
    return apiClient.delete(`/cart/items/${itemId}`);
  }
};