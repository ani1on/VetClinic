<template>
  <section class="page">
    <div class="hero-card">
      <div>
        <span class="badge">FastPig clinic platform</span>
        <h1 class="hero-title">Healthy pets, calm owners, one digital clinic.</h1>
        <p class="hero-subtitle">
          FastPig combines appointment booking, veterinary catalog, favorites and
          pet profiles in one warm and easy web experience.
        </p>
        <div class="hero-actions">
          <router-link class="button" to="/appointment">Book appointment</router-link>
          <router-link class="button-secondary" to="/catalog">Open catalog</router-link>
        </div>
      </div>

      <div class="hero-aside">
        <div class="panel">
          <p class="mini-title">Today in clinic</p>
          <p class="muted">8 surgeries, 19 online confirmations and 34 repeated orders.</p>
        </div>
        <div class="panel soft success">
          <p class="mini-title">Fast route</p>
          <p class="muted">Client can book visit in three steps and instantly see the doctor.</p>
        </div>
        <div class="panel soft">
          <p class="mini-title">Main scenario</p>
          <p class="muted">Auth -> choose service -> book appointment -> manage profile.</p>
        </div>
      </div>
    </div>

    <section class="stats-grid">
      <article v-for="item in stats" :key="item.value" class="stat-card">
        <p class="stat-value">{{ item.value }}</p>
        <p class="stat-label">{{ item.label }}</p>
      </article>
    </section>

    <section class="page">
      <div class="section-heading">
        <div>
          <h2 class="section-title">Popular directions</h2>
          <p class="section-copy">
            The home feed highlights what owners do most often: choose service,
            buy daily products and keep all pet data close.
          </p>
        </div>
      </div>

      <div class="tile-grid">
        <article v-for="service in services" :key="service.title" class="tile">
          <div class="meta-row">
            <span class="chip">{{ service.tag }}</span>
            <strong>{{ service.price }}</strong>
          </div>
          <h3 class="card-title">{{ service.title }}</h3>
          <p class="muted">{{ service.description }}</p>
        </article>
      </div>
    </section>

    <section class="split-grid">
      <article class="panel">
        <div class="section-heading">
          <div>
            <h2 class="section-title">Latest updates</h2>
            <p class="section-copy">A home page can later be filled from your backend news feed.</p>
          </div>
        </div>
        <div class="list-column">
          <article class="feed-card">
            <div class="meta-row">
              <strong>New doctor shift</strong>
              <span class="chip">Urgent care</span>
            </div>
            <p class="muted">Dr. Elena is available on weekends for emergency patients.</p>
          </article>
          <article class="feed-card">
            <div class="meta-row">
              <strong>Season vaccination campaign</strong>
              <span class="chip">May promo</span>
            </div>
            <p class="muted">Bundle visits and vaccines with auto-filled patient cards.</p>
          </article>
        </div>
      </article>

      <article class="panel">
        <p class="mini-title">Quick links</p>
        <div class="hero-actions">
          <router-link class="button-secondary" to="/profile">Pet cards</router-link>
          <router-link class="button-secondary" to="/favorits">Favorites</router-link>
          <router-link class="button-secondary" to="/about">About clinic</router-link>
        </div>
      </article>
    </section>
  </section>
</template>

<script>
import { homeStats, services } from "../data/mock";

export default {
  name: "HomeView",
  data() {
    return {
      stats: homeStats,
      services,
    };
  },
};
</script>
