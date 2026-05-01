<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Catalog</h1>
        <p class="section-copy">
          Product catalog for clinic shop. Cards can later be loaded from your backend with filters,
          prices, favorite state and stock status.
        </p>
      </div>
      <div class="chip-row">
        <span class="chip">Feed</span>
        <span class="chip">Supplements</span>
        <span class="chip">Accessories</span>
      </div>
    </div>

    <section class="catalog-grid">
      <article v-for="product in products" :key="product.id" class="tile">
        <div class="meta-row">
          <span class="chip">{{ product.category }}</span>
          <strong>{{ product.price }}</strong>
        </div>
        <h2 class="card-title">{{ product.title }}</h2>
        <p class="muted">{{ product.description }}</p>
        <div class="price-row">
          <span class="muted">{{ product.stock }}</span>
          <div class="inline-actions">
            <button class="button-secondary" type="button">Favorite</button>
            <button class="button" type="button">Add to cart</button>
          </div>
        </div>
      </article>
    </section>
  </section>
</template>

<script>
import { products } from "../data/mock";

export default {
  name: "CatalogView",
  data() {
    return {
      products,
    };
  },
};
</script>
