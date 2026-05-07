<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Favorites</h1>
        <p class="section-copy">Your saved products, services and doctors.</p>
      </div>
    </div>

    <div v-if="isLoading" class="muted">Loading favorites…</div>
    <p v-if="error" class="error-text">{{ error }}</p>

    <section v-if="favorites.length" class="favorites-grid">
      <article v-for="item in favorites" :key="item.id" class="tile">
        <div class="meta-row">
          <h2 class="card-title">{{ item.entity_type }} #{{ item.entity_id }}</h2>
          <span class="chip">{{ item.entity_type }}</span>
        </div>
        <p class="muted">Saved on {{ new Date(item.created_at).toLocaleDateString() }}</p>
        <div class="hero-actions">
          <button class="button-secondary" type="button">Open</button>
          <button class="button" type="button" @click="removeFavorite(item.id)">Remove</button>
        </div>
      </article>
    </section>
    <p v-else-if="!isLoading" class="muted">No favorites yet.</p>
  </section>
</template>

<script>
import favoriteService from '@/services/favoriteService';

export default {
  name: "FavoritesView",
  data() {
    return {
      favorites: [],
      isLoading: false,
      error: null,
    };
  },
  async created() {
    await this.fetchFavorites();
  },
  methods: {
    async fetchFavorites() {
      this.isLoading = true;
      try {
        const resp = await favoriteService.getFavorites();
        this.favorites = resp.data;
      } catch (e) {
        this.error = 'Failed to load favorites';
      } finally {
        this.isLoading = false;
      }
    },
    async removeFavorite(id) {
      try {
        await favoriteService.removeFavorite(id);
        this.favorites = this.favorites.filter(f => f.id !== id);
      } catch (e) {
        alert('Could not remove');
      }
    }
  }
};
</script>
<style scoped>
.error-text { color: #e53e3e; }
</style>