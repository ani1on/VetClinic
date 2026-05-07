<template>
  <section class="page">
    <!-- hero … без изменений -->
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

    <!-- Услуги с сервера -->
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

      <div v-if="isServicesLoading" class="muted">Loading services…</div>
      <p v-if="servicesError" class="error-text">{{ servicesError }}</p>

      <div v-if="services.length" class="tile-grid">
        <article v-for="service in services" :key="service.id" class="tile">
          <div class="meta-row">
            <span class="chip">{{ service.category || 'Service' }}</span>
            <strong>{{ service.price }} BYN</strong>
          </div>
          <h3 class="card-title">{{ service.name }}</h3>
          <p class="muted">{{ service.description }}</p>
        </article>
      </div>
    </section>

    <!-- Новости -->
    <section class="split-grid">
      <article class="panel">
        <div class="section-heading">
          <div>
            <h2 class="section-title">Latest updates</h2>
            <p class="section-copy">Fresh news from the clinic.</p>
          </div>
        </div>
        <div v-if="isNewsLoading" class="muted">Loading news…</div>
        <p v-if="newsError" class="error-text">{{ newsError }}</p>
        <div v-if="news.length" class="list-column">
          <article v-for="item in news" :key="item.id" class="feed-card">
            <div class="meta-row">
              <strong>{{ item.title }}</strong>
              <span class="chip">{{ item.created_at?.slice(0,10) }}</span>
            </div>
            <p class="muted">{{ item.content }}</p>
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
import serviceService from '@/services/serviceService';
import newsService from '@/services/newsService';

export default {
  name: "HomeView",
  data() {
    return {
      stats: [
        { value: "24/7", label: "Emergency support for urgent cases and night consultations." },
        { value: "12", label: "Doctors, diagnosticians and pet-care specialists in one team." },
        { value: "4.9", label: "Average client rating based on service quality and attention." },
        { value: "15m", label: "Average response time for online appointment confirmations." },
      ],
      services: [],
      isServicesLoading: false,
      servicesError: null,
      news: [],
      isNewsLoading: false,
      newsError: null,
    };
  },
  async created() {
    await this.fetchServices();
    await this.fetchNews();
  },
  methods: {
    async fetchServices() {
      this.isServicesLoading = true;
      try {
        const resp = await serviceService.getServices();
        this.services = resp.data;
      } catch (e) {
        this.servicesError = 'Failed to load services';
      } finally {
        this.isServicesLoading = false;
      }
    },
    async fetchNews() {
      this.isNewsLoading = true;
      try {
        const resp = await newsService.getNews();
        this.news = resp.data.news;
      } catch (e) {
        this.newsError = 'Failed to load news';
      } finally {
        this.isNewsLoading = false;
      }
    },
  },
};
</script>
<style scoped>
/* стили уже глобальные, можно оставить пустым или добавить специфичные */
.error-text { color: #e53e3e; margin-top: 0.5rem; }
</style>