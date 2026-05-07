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
          <h2 class="card-title">{{ getEntityName(item) }}</h2>
          <span class="chip">{{ item.entity_type }}</span>
        </div>
        <p class="muted">Saved on {{ new Date(item.created_at).toLocaleDateString() }}</p>

        <!-- Детали (раскрываются по Open) -->
        <div v-if="expandedId === item.id" class="entity-details">
          <p v-if="getEntityDetail(item).description" class="muted">
            {{ getEntityDetail(item).description }}
          </p>
          <div class="detail-props" v-if="getEntityDetail(item).price != null">
            <span class="label">Price:</span>
            <span>{{ getEntityDetail(item).price }} BYN</span>
          </div>
          <div class="detail-props" v-if="getEntityDetail(item).category">
            <span class="label">Category:</span>
            <span>{{ getEntityDetail(item).category }}</span>
          </div>
          <div class="detail-props" v-if="getEntityDetail(item).specialization">
            <span class="label">Specialization:</span>
            <span>{{ getEntityDetail(item).specialization }}</span>
          </div>
          <div class="detail-props" v-if="getEntityDetail(item).duration_minutes">
            <span class="label">Duration:</span>
            <span>{{ getEntityDetail(item).duration_minutes }} min</span>
          </div>
        </div>

        <div class="hero-actions">
          <button
            class="button-secondary"
            type="button"
            @click="toggleDetails(item.id)"
          >
            {{ expandedId === item.id ? 'Close' : 'Open' }}
          </button>
          <button class="button" type="button" @click="removeFavorite(item.id)">
            Remove
          </button>
        </div>
      </article>
    </section>

    <p v-else-if="!isLoading" class="muted">No favorites yet.</p>
  </section>
</template>

<script>
import favoriteService from '@/services/favoriteService';
import productService from '@/services/productService';
import serviceService from '@/services/serviceService';
import doctorService from '@/services/doctorService';

export default {
  name: "FavoritesView",
  data() {
    return {
      favorites: [],
      isLoading: false,
      error: null,
      // справочники
      allProducts: [],
      allServices: [],
      allDoctors: [],
      expandedId: null,
    };
  },
  async created() {
    await Promise.all([this.fetchFavorites(), this.loadReferenceData()]);
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

    async loadReferenceData() {
      try {
        const [productsResp, servicesResp, doctorsResp] = await Promise.all([
          productService.getProducts(),
          serviceService.getServices(),
          doctorService.getAll()
        ]);

        // catalog возвращает { total, products }
        this.allProducts = productsResp.data.products || productsResp.data || [];
        // services возвращает массив
        this.allServices = Array.isArray(servicesResp.data) ? servicesResp.data : [];
        // doctors тоже массив
        this.allDoctors = Array.isArray(doctorsResp.data) ? doctorsResp.data : [];
      } catch (e) {
        console.warn('Failed to load reference data for favorites', e);
      }
    },

    getEntityName(item) {
      const info = this.getEntityInfo(item);
      return info ? info.name : `${item.entity_type} #${item.entity_id}`;
    },

    getEntityDetail(item) {
      return this.getEntityInfo(item) || {};
    },

    getEntityInfo(item) {
      const type = item.entity_type;
      const id = item.entity_id;

      if (type === 'product') {
        const p = this.allProducts.find(p => p.id === id);
        return p ? {
          name: p.name,
          description: p.description,
          price: p.price,
          category: p.category,
          is_available: p.is_available
        } : null;
      }
      else if (type === 'service') {
        const s = this.allServices.find(s => s.id === id);
        return s ? {
          name: s.name,
          description: s.description,
          price: s.price,
          duration_minutes: s.duration_minutes,
          category: s.category,
          is_active: s.is_active
        } : null;
      }
      else if (type === 'doctor') {
        const d = this.allDoctors.find(d => d.id === id);
        return d ? {
          name: d.full_name,
          description: d.description,
          specialization: d.specialization,
          is_active: d.is_active
        } : null;
      }
      return null;
    },

    toggleDetails(id) {
      this.expandedId = this.expandedId === id ? null : id;
    },

    async removeFavorite(id) {
      try {
        await favoriteService.removeFavorite(id);
        this.favorites = this.favorites.filter(f => f.id !== id);
        if (this.expandedId === id) this.expandedId = null;
      } catch (e) {
        alert('Could not remove');
      }
    }
  }
};
</script>

<style scoped>
.error-text { color: #e53e3e; }

.entity-details {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--line);
}

.detail-props {
  display: flex;
  gap: 8px;
  margin-top: 6px;
  font-size: 0.95rem;
}

.detail-props .label {
  color: var(--muted);
  font-weight: 600;
}
</style>