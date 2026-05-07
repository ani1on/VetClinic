<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Admin dashboard</h1>
        <p class="section-copy">
          Real‑time metrics from the backend.
        </p>
      </div>
    </div>

    <div v-if="isLoading" class="muted">Loading dashboard…</div>
    <p v-if="error" class="error-text">{{ error }}</p>

    <section v-if="metrics.length" class="stats-grid">
      <article v-for="metric in metrics" :key="metric.label" class="stat-card">
        <p class="stat-value">{{ metric.value }}</p>
        <p class="stat-label">{{ metric.label }}</p>
      </article>
    </section>

    <!-- Остальная разметка с очередями операций оставлена как есть -->
    <section class="admin-grid">
      <article class="panel">
        <h2 class="section-title">Operations queue</h2>
        <div class="list-column">
          <article class="feed-card">
            <div class="meta-row">
              <strong>Approve tomorrow appointments</strong>
              <span class="chip">12 pending</span>
            </div>
            <p class="muted">Manager confirms time, doctor and payment status.</p>
          </article>
          <article class="feed-card">
            <div class="meta-row">
              <strong>Moderate new reviews</strong>
              <span class="chip">6 waiting</span>
            </div>
            <p class="muted">Check feedback before publishing to the public feed.</p>
          </article>
        </div>
      </article>
      <article class="panel">
        <h2 class="section-title">Content and stock</h2>
        <div class="list-column">
          <article class="feed-card soft">
            <strong>Catalog management</strong>
            <p class="muted">Create product, update price, mark hidden, change stock count.</p>
          </article>
          <article class="feed-card soft success">
            <strong>Doctors schedule</strong>
            <p class="muted">Edit working slots and disable unavailable time windows.</p>
          </article>
        </div>
      </article>
    </section>
  </section>
</template>

<script>
import adminService from '@/services/adminService';

export default {
  name: "AdminView",
  data() {
    return {
      metrics: [],
      isLoading: false,
      error: null,
    };
  },
  async created() {
    await this.loadDashboard();
  },
  methods: {
    async loadDashboard() {
      this.isLoading = true;
      try {
        const resp = await adminService.getDashboard();
        const m = resp.data;
        this.metrics = [
          { value: m.total_appointments, label: 'Total appointments' },
          { value: m.appointments_this_week, label: 'This week' },
          { value: m.pending_appointments, label: 'Pending' },
          { value: m.total_users, label: 'Users' },
          { value: m.new_users_this_week, label: 'New users this week' },
          { value: m.total_products, label: 'Products' },
          { value: m.low_stock_products, label: 'Low stock' },
          { value: m.pending_reviews, label: 'Pending reviews' },
        ];
      } catch (e) {
        this.error = 'Failed to load dashboard';
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>
<style scoped>
.error-text { color: #e53e3e; }
</style>