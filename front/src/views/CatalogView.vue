<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Catalog</h1>
        <p class="section-copy">Product catalog for clinic shop. Loaded from server.</p>
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
      <input v-model="filters.search" placeholder="Search…" @input="debounceSearch" class="search-input" />
      <label><input type="checkbox" v-model="filters.in_stock" @change="fetchProducts" /> In stock only</label>
    </div>

    <div v-if="isLoading" class="muted">Loading products…</div>
    <p v-if="error" class="error-text">{{ error }}</p>

    <!-- Сетка товаров — показываем только displayedProducts -->
    <section v-if="displayedProducts.length" class="catalog-grid">
      <article v-for="product in displayedProducts" :key="product.id" class="tile">
        <div class="meta-row">
          <span class="chip">{{ product.category }}</span>
          <strong>{{ product.price }} BYN</strong>
        </div>
        <h2 class="card-title">{{ product.name }}</h2>
        <p class="muted">{{ product.description }}</p>
        <div class="price-row">
          <span class="muted">{{ product.stock_quantity > 0 ? 'In stock' : 'Out of stock' }}</span>
          <div class="inline-actions">
            <button class="button-secondary" type="button" @click="addToFavorites(product.id)">Favorite</button>
            <button
              class="button"
              type="button"
              @click="addToCart(product.id)"
              :disabled="product.stock_quantity <= 0"
            >
              Add to cart
            </button>
          </div>
        </div>
      </article>
    </section>

    <!-- Кнопка «Загрузить ещё» появляется, если есть скрытые товары -->
    <div v-if="hasMore" class="load-more-wrapper">
      <button class="button-secondary" @click="loadMore" :disabled="loadingMore">
        {{ loadingMore ? 'Loading…' : 'Load more' }}
      </button>
    </div>

    <p v-if="!isLoading && !allProducts.length" class="muted">No products found.</p>
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
      allProducts: [],          // все загруженные товары с сервера
      displayedProducts: [],    // те, что сейчас показаны
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
      categories: ['Feed', 'Vitamins', 'Care', 'Accessories'],
      searchTimer: null,
      visibleCount: 0,          // сколько товаров уже отображено
      initialLoad: 6,           // первая порция
      loadBatch: 2,             // последующие порции
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
    async fetchProducts() {
      this.isLoading = true;
      this.error = null;
      try {
        const params = { ...this.filters };
        if (!params.in_stock) delete params.in_stock;
        const resp = await productService.getProducts(params);
        this.allProducts = resp.data.products || resp.data;
        // сбрасываем счётчик
        this.visibleCount = 0;
        this.displayedProducts = [];
        // показываем первую порцию
        this.showNext(this.initialLoad);
      } catch (e) {
        this.error = 'Failed to load products';
        this.allProducts = [];
      } finally {
        this.isLoading = false;
      }
    },
    // добавляет к отображаемым товарам указанное количество из allProducts
    showNext(count) {
      const next = this.allProducts.slice(this.visibleCount, this.visibleCount + count);
      this.displayedProducts.push(...next);
      this.visibleCount += next.length;
    },
    loadMore() {
      this.loadingMore = true;
      // небольшая задержка для имитации сетевого запроса (можно убрать)
      setTimeout(() => {
        this.showNext(this.loadBatch);
        this.loadingMore = false;
      }, 300);
    },
    setCategory(cat) {
      if (this.filters.category === cat) {
        this.filters.category = '';
      } else {
        this.filters.category = cat;
      }
      this.fetchProducts();
    },
    debounceSearch() {
      clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        this.fetchProducts();
      }, 400);
    },
    async addToCart(productId) {
      try {
        await cartService.addItem(productId, 1);
        alert('Added to cart');
      } catch (e) {
        alert('Could not add to cart');
      }
    },
    async addToFavorites(productId) {
      try {
        await favoriteService.addFavorite('product', productId);
        alert('Added to favorites');
      } catch (e) {
        alert('Could not add to favorites');
      }
    }
  }
};
</script>

<style scoped>
.error-text { color: #e53e3e; margin: 0.5rem 0; }
.filters {
  display: flex;
  gap: 12px;
  align-items: center;
}
.search-input {
  padding: 8px 12px;
  border-radius: 12px;
  border: 1px solid var(--line);
}
.load-more-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>