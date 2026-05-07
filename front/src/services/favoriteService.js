import apiClient from './api';

export default {
  getFavorites() {
    return apiClient.get('/favorites/');
  },
  addFavorite(entityType, entityId) {
    return apiClient.post('/favorites/', { entity_type: entityType, entity_id: entityId });
  },
  removeFavorite(favId) {
    return apiClient.delete(`/favorites/${favId}`);
  }
};