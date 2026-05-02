<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Admin dashboard</h1>
        <p class="section-copy">
          Cabinet for staff and administrators with metrics, queue, product stock and moderation.
        </p>
      </div>
    </div>

    <section class="stats-grid">
      <article v-for="metric in metrics" :key="metric.label" class="stat-card">
        <p class="stat-value">{{ metric.value }}</p>
        <p class="stat-label">{{ metric.label }}</p>
      </article>
    </section>

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
import { adminMetrics } from "../data/mock";

export default {
  name: "AdminView",
  data() {
    return {
      metrics: adminMetrics,
    };
  },
};
</script>
