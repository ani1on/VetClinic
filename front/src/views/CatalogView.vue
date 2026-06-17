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
}
.toast { position: fixed; top: 20px; right: 20px; z-index: 1000; padding: 12px 20px; border-radius: 12px; background: #323232; color: white; font-weight: 500; box-shadow: 0 4px 12px rgba(0,0,0,0.15); animation: fadeIn 0.3s ease; }
.toast.success { background: #2b7e3a; }
.toast.error { background: #c62828; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
.error-text { color: #e53e3e; margin: 0.5rem 0; }
.filters { display: flex; gap: 12px; align-items: center; }
.search-input { padding: 8px 12px; border-radius: 12px; border: 1px solid var(--line); }
.load-more-wrapper { display: flex; justify-content: center; margin-top: 20px; }
</style>