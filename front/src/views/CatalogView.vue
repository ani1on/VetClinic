<template>
  <section class="page">
    <div v-if="toastMessage" class="toast" :class="toastType">{{ toastMessage }}</div>

    <div class="section-heading">
      <div>
        <h1 class="section-title">Каталог</h1>
        <p class="section-copy">Каталог товаров магазина клиники.</p>
      </div>
      <div class="chip-row">
        <span
          v-for="cat in categories"
          :key="cat"
          class="chip"
          :class="{ active: filters.category === cat }"
          @click="setCategory(cat)"
        >{{ cat }}</span>
      </div>
    </div>

    <div class="filters row">
      <input v-model="filters.search" placeholder="Поиск…" @input="debounceSearch" class="search-input" />
      <label><input type="checkbox" v-model="filters.in_stock" @change="fetchProducts" /> Только в наличии</label>
    </div>

    <div v-if="isLoading" class="muted">Загрузка товаров…</div>
    <p v-if="error" class="error-text">{{ error }}</p>

    <section v-if="displayedProducts.length" class="catalog-grid">
      <article v-for="product in displayedProducts" :key="product.id" class="tile">
        <img v-if="product.image_url" :src="product.image_url" :alt="product.name" class="card-image" />
        <div class="meta-row">
          <span class="chip">{{ product.category }}</span>
          <strong>{{ product.price }} BYN</strong>
        </div>
        <h2 class="card-title">{{ product.name }}</h2>
        <p class="muted">{{ product.description }}</p>
        <div class="price-row">
          <span class="muted">{{ product.stock_quantity > 0 ? 'В наличии' : 'Нет в наличии' }}</span>
          <div class="inline-actions">
            <button class="button-secondary" type="button" @click="addToFavorites(product.id)">В избранное</button>
            <button class="button" type="button" @click="addToCart(product.id)" :disabled="product.stock_quantity <= 0">
              В корзину
            </button>
          </div>
        </div>
      </article>
    </section>

    <div v-if="hasMore" class="load-more-wrapper">
      <button class="button-secondary" @click="loadMore" :disabled="loadingMore">
        {{ loadingMore ? 'Загрузка…' : 'Загрузить ещё' }}
      </button>
    </div>

    <p v-if="!isLoading && !allProducts.length" class="muted">Товары не найдены.</p>
  </section>
</template>

<script>
import productService from '@/services/productService';
import cartService from '@/services/cartService';
import favoriteService from '@/services/favoriteService';

export default {
  name: "CatalogView",
  data() {
    return {
      toastMessage: '',
      toastType: '',
      allProducts: [],
      displayedProducts: [],
      isLoading: false,
      loadingMore: false,
      error: null,
      filters: {
        category: '',
        search: '',
        min_price: null,
        max_price: null,
        in_stock: false
      },
      categories: ['Корм', 'Витамины', 'Уход', 'Аксессуары'],
      searchTimer: null,
      visibleCount: 0,
      initialLoad: 6,
      loadBatch: 2,
    };
  },
  computed: {
    hasMore() {
      return this.visibleCount < this.allProducts.length;
    }
  },
  async created() {
    await this.fetchProducts();
  },
  methods: {
    showToast(text, type = 'success') {
      this.toastMessage = text;
      this.toastType = type;
      setTimeout(() => { this.toastMessage = ''; }, 3000);
    },

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
          return data.map(err => `Поле "${err.loc[err.loc.length-1]}": ${err.msg}`).join('; ');
        }
        if (data.detail) {
          if (typeof data.detail === 'string') return data.detail;
          if (Array.isArray(data.detail)) return data.detail.map(d => d.msg).join('; ');
        }
        if (data.message) return data.message;
      }
      return 'Произошла ошибка. Попробуйте обновить страницу.';
    },

    async fetchProducts() {
      this.isLoading = true;
      this.error = null;
      try {
        const params = { ...this.filters };
        if (!params.in_stock) delete params.in_stock;
        const resp = await productService.getProducts(params);
        this.allProducts = resp.data.products || resp.data;
        this.visibleCount = 0;
        this.displayedProducts = [];
        this.showNext(this.initialLoad);
      } catch (e) {
        this.error = this.parseApiError(e);
        this.allProducts = [];
      } finally {
        this.isLoading = false;
      }
    },

    showNext(count) {
      const next = this.allProducts.slice(this.visibleCount, this.visibleCount + count);
      this.displayedProducts.push(...next);
      this.visibleCount += next.length;
    },

    loadMore() {
      this.loadingMore = true;
      setTimeout(() => {
        this.showNext(this.loadBatch);
        this.loadingMore = false;
      }, 300);
    },

    setCategory(cat) {
      this.filters.category = this.filters.category === cat ? '' : cat;
      this.fetchProducts();
    },

    debounceSearch() {
      clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => this.fetchProducts(), 400);
    },

    async addToCart(productId) {
      try {
        await cartService.addItem(productId, 1);
        this.showToast('Товар добавлен в корзину', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },

    async addToFavorites(productId) {
      try {
        await favoriteService.addFavorite('product', productId);
        this.showToast('Товар добавлен в избранное', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
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
  transition: transform 0.3s ease;
}
.tile:hover .card-image {
  transform: scale(1.03);
}
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  padding: 14px 22px;
  border-radius: 14px;
  background: #323232;
  color: white;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  animation: toastIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.toast.success { background: linear-gradient(135deg, #2b7e3a, #3aa17e); }
.toast.error { background: linear-gradient(135deg, #c62828, #e53e3e); }
@keyframes toastIn {
  from { opacity: 0; transform: translateX(20px) scale(0.95); }
  to { opacity: 1; transform: translateX(0) scale(1); }
}
.error-text {
  color: #e53e3e;
  margin: 0.5rem 0;
  padding: 10px 14px;
  background: rgba(229, 62, 62, 0.08);
  border-radius: 12px;
  border-left: 3px solid #e53e3e;
}
.filters { display: flex; gap: 12px; align-items: center; }
.search-input {
  padding: 10px 16px;
  border-radius: 999px;
  border: 2px solid var(--line);
  transition: all 0.2s ease;
  flex: 1;
  max-width: 300px;
}
.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(255, 122, 89, 0.12);
}
.load-more-wrapper { display: flex; justify-content: center; margin-top: 20px; }

.catalog-grid .tile {
  animation: fadeInUp 0.4s ease backwards;
}
.catalog-grid .tile:nth-child(1) { animation-delay: 0.05s; }
.catalog-grid .tile:nth-child(2) { animation-delay: 0.1s; }
.catalog-grid .tile:nth-child(3) { animation-delay: 0.15s; }
.catalog-grid .tile:nth-child(4) { animation-delay: 0.2s; }
.catalog-grid .tile:nth-child(5) { animation-delay: 0.25s; }
.catalog-grid .tile:nth-child(6) { animation-delay: 0.3s; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>