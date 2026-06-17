<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Избранное</h1>
        <p class="section-copy">Сохранённые товары, услуги и врачи.</p>
      </div>
    </div>

    <div v-if="isLoading" class="muted">Загрузка избранного…</div>
    <p v-if="error" class="error-text">{{ error }}</p>

    <section v-if="favorites.length" class="favorites-grid">
      <article v-for="item in favorites" :key="item.id" class="tile">
        <img v-if="getEntityImage(item)" :src="getEntityImage(item)" :alt="getEntityName(item)" class="card-image" />
        <div class="meta-row">
          <h2 class="card-title">{{ getEntityName(item) }}</h2>
          <span class="chip">{{ translateEntityType(item.entity_type) }}</span>
        </div>
        <p class="muted">Сохранено: {{ new Date(item.created_at).toLocaleDateString() }}</p>

        <!-- Детали -->
        <div v-if="expandedId === item.id" class="entity-details">
          <p v-if="getEntityDetail(item).description" class="muted">
            {{ getEntityDetail(item).description }}
          </p>
          <div class="detail-props" v-if="getEntityDetail(item).price != null">
            <span class="label">Цена:</span>
            <span>{{ getEntityDetail(item).price }} BYN</span>
          </div>
          <div class="detail-props" v-if="getEntityDetail(item).category">
            <span class="label">Категория:</span>
            <span>{{ getEntityDetail(item).category }}</span>
          </div>
          <div class="detail-props" v-if="getEntityDetail(item).specialization">
            <span class="label">Специализация:</span>
            <span>{{ getEntityDetail(item).specialization }}</span>
          </div>
          <div class="detail-props" v-if="getEntityDetail(item).duration_minutes">
            <span class="label">Длительность:</span>
            <span>{{ getEntityDetail(item).duration_minutes }} мин</span>
          </div>
        </div>

        <div class="hero-actions">
          <button
            class="button-secondary"
            type="button"
            @click="toggleDetails(item.id)"
          >
            {{ expandedId === item.id ? 'Закрыть' : 'Открыть' }}
          </button>
          <button class="button" type="button" @click="removeFavorite(item.id)">
            Удалить
          </button>
        </div>
      </article>
    </section>

    <p v-else-if="!isLoading" class="muted">Пока нет избранного.</p>
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
    // Улучшенный парсинг ошибок с обработкой сетевых ошибок и 5xx
    parseApiError(error) {
      if (!error.response) {
        return 'Не удалось соединиться с сервером. Проверьте подключение к интернету.';
      }
      const status = error.response.status;
      if (status >= 500 && status <= 503) {
        return 'Сервер временно недоступен. Попробуйте позже.';
      }
      const data = error.response.data;
      if (data) {
        if (Array.isArray(data) && data[0]?.loc) {
          const messages = data.map(err => {
            const field = err.loc[err.loc.length - 1];
            return `Поле "${field}": ${err.msg}`;
          });
          return messages.join('; ');
        }
        if (data.detail) {
          if (typeof data.detail === 'string') return data.detail;
          if (Array.isArray(data.detail)) return data.detail.map(d => d.msg).join('; ');
        }
        if (data.message) return data.message;
      }
      return 'Произошла ошибка. Попробуйте обновить страницу.';
    },

    translateEntityType(type) {
      const map = {
        product: 'Товар',
        service: 'Услуга',
        doctor: 'Врач'
      };
      return map[type] || type;
    },

    async fetchFavorites() {
      this.isLoading = true;
      this.error = null;
      try {
        const resp = await favoriteService.getFavorites();
        this.favorites = resp.data;
      } catch (e) {
        this.error = this.parseApiError(e);
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
        this.allProducts = productsResp.data.products || productsResp.data || [];
        this.allServices = Array.isArray(servicesResp.data) ? servicesResp.data : [];
        this.allDoctors = Array.isArray(doctorsResp.data) ? doctorsResp.data : [];
      } catch (e) {
        console.warn('Не удалось загрузить справочные данные для избранного', e);
      }
    },

    getEntityName(item) {
      const info = this.getEntityInfo(item);
      return info ? info.name : `${this.translateEntityType(item.entity_type)} #${item.entity_id}`;
    },

    getEntityImage(item) {
      const info = this.getEntityInfo(item);
      return info ? (info.image_url || info.photo_url) : null;
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
          is_available: p.is_available,
          image_url: p.image_url
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
          is_active: d.is_active,
          photo_url: d.photo_url
        } : null;
      }
      return null;
    },

    toggleDetails(id) {
      this.expandedId = this.expandedId === id ? null : id;
    },

    async removeFavorite(id) {
      this.error = null;
      try {
        await favoriteService.removeFavorite(id);
        this.favorites = this.favorites.filter(f => f.id !== id);
        if (this.expandedId === id) this.expandedId = null;
      } catch (e) {
        this.error = this.parseApiError(e);
      }
    }
  }
};
</script>

<style scoped>
.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 16px;
}
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