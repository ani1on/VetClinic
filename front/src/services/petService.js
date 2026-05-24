import apiClient from './api';

export default {
  createPet(data) {
    return apiClient.post('/pets/', data);
  },
  getMyPets() {
    return apiClient.get('/pets/');
  },
  getPet(petId) {
    return apiClient.get(`/pets/${petId}`);
  },
  updatePet(petId, data) {
    return apiClient.put(`/pets/${petId}`, data);
  },
  deletePet(petId) {
    return apiClient.delete(`/pets/${petId}`);
  },
  getPetHistory(petId) {
    return apiClient.get(`/pets/${petId}/history`);
  },
  getAllPets() {
  return apiClient.get('/pets/all'); 
}
};