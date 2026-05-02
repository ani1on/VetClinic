<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Appointment</h1>
        <p class="section-copy">
          Booking flow and list of existing records. All form fields are ready for API integration.
        </p>
      </div>
    </div>

    <section class="split-grid">
      <article class="panel">
        <h2 class="section-title">New booking</h2>
        <div class="form-grid two">
          <label class="field">
            <span>Pet</span>
            <select>
              <option>Peppa</option>
              <option>Boris</option>
            </select>
          </label>
          <label class="field">
            <span>Service</span>
            <select>
              <option>Primary examination</option>
              <option>Vaccination package</option>
              <option>Ultrasound and diagnostics</option>
            </select>
          </label>
          <label class="field">
            <span>Date</span>
            <input type="date" />
          </label>
          <label class="field">
            <span>Time</span>
            <input type="time" />
          </label>
        </div>
        <label class="field">
          <span>Comment for doctor</span>
          <textarea placeholder="Describe symptoms or pet behavior before visit."></textarea>
        </label>
        <div class="hero-actions">
          <button class="button" type="button">Create appointment</button>
        </div>
      </article>

      <article class="panel">
        <h2 class="section-title">My records</h2>
        <div class="list-column">
          <article v-for="item in appointments" :key="`${item.pet}-${item.date}`" class="feed-card">
            <div class="meta-row">
              <strong>{{ item.pet }} - {{ item.service }}</strong>
              <span class="chip">{{ item.status }}</span>
            </div>
            <p class="muted">{{ item.date }} at {{ item.time }} with {{ item.doctor }}</p>
          </article>
        </div>
      </article>
    </section>
  </section>
</template>

<script>
import { appointments } from "../data/mock";

export default {
  name: "AppointmentView",
  data() {
    return {
      appointments,
    };
  },
};
</script>
