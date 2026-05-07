<template>
  <section class="page">
    <div class="hero-card">
      <div>
        <span class="badge">About clinic</span>
        <h1 class="hero-title">FastPig is a modern veterinary space with a human tone.</h1>
        <p class="hero-subtitle">
          This page displays contacts, doctors, working hours and more from the backend.
        </p>
      </div>

      <article v-if="clinic" class="panel soft">
        <p class="mini-title">Contacts block</p>
        <p class="muted">{{ clinic.address || 'Address not set' }}</p>
        <p class="muted">{{ clinic.phone || 'No phone' }}</p>
        <p class="muted">{{ clinic.email || 'No email' }}</p>
      </article>
      <article v-else-if="isLoading" class="panel soft">
        <p>Loading clinic info…</p>
      </article>
      <p v-if="error" class="error-text">{{ error }}</p>
    </div>

    <section class="about-grid">
      <article v-for="fact in facts" :key="fact.title" class="tile">
        <h2 class="card-title">{{ fact.title }}</h2>
        <p class="muted">{{ fact.description }}</p>
      </article>
    </section>

    <!-- Блок с социальными сетями -->
    <section class="social-section">
      <h2 class="section-title">Follow us</h2>
      <div class="social-links">
        <a href="https://www.instagram.com/ani1onn" class="social-link instagram">
          <span class="social-icon">📷</span> Instagram
        </a>
        <a href="https://web.telegram.org/ani1on" class="social-link telegram">
          <span class="social-icon">📨</span> Telegram
        </a>
        <a href="https://vk.com/v_vrrrrrrrrrrrrrrrrtoi" class="social-link vk">
          <span class="social-icon">🔵</span> VK
        </a>
      </div>
    </section>
  </section>
</template>

<script>
import clinicService from '@/services/clinicService';

export default {
  name: "AboutView",
  data() {
    return {
      clinic: null,
      isLoading: false,
      error: null,
      facts: [
        { title: "Digital patient card", description: "Every visit stays in one cabinet." },
        { title: "Separate zones", description: "Quiet areas for large and small pets." },
        { title: "Own shop", description: "Clinic catalog with feed, care and doctor kits." },
        { title: "FastPig hotline", description: "Help with urgent routing and questions." },
      ],
    };
  },
  async created() {
    await this.fetchClinicInfo();
  },
  methods: {
    async fetchClinicInfo() {
      this.isLoading = true;
      try {
        const resp = await clinicService.getAbout();
        this.clinic = resp.data;
      } catch (e) {
        this.error = 'Could not load clinic data';
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.error-text { color: #e53e3e; }

/* Стили для блока соцсетей */
.social-section {
  margin-top: 32px;
  text-align: center;
}
.social-links {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 12px;
}
.social-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 12px 18px;
  border-radius: 999px;
  background: var(--surface-strong);
  border: 1px solid var(--line);
  color: var(--text);
  text-decoration: none;
  font-weight: 700;
  transition: background 0.2s, color 0.2s;
}
.social-link:hover {
  background: var(--text);
  color: #fff;
}
.social-icon {
  font-size: 1.2rem;
}
</style>