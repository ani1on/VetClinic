<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Favorits</h1>
        <p class="section-copy">
          Stored products, services and doctors. Route name is kept as requested: `/favorits`.
        </p>
      </div>
    </div>

    <section class="favorites-grid">
      <article v-for="item in favorites" :key="item.title" class="tile">
        <div class="meta-row">
          <h2 class="card-title">{{ item.title }}</h2>
          <span class="chip">{{ item.type }}</span>
        </div>
        <p class="muted">{{ item.note }}</p>
        <div class="hero-actions">
          <button class="button-secondary" type="button">Open</button>
          <button class="button" type="button">Remove</button>
        </div>
      </article>
    </section>
  </section>
</template>

<script>
import { favorites } from "../data/mock";

export default {
  name: "FavoritesView",
  data() {
    return {
      favorites,
    };
  },
};
</script>
