<template>
  <section class="page">
    <div class="hero-card">
      <div>
        <span class="badge">About clinic</span>
        <h1 class="hero-title">FastPig is a modern veterinary space with a human tone.</h1>
        <p class="hero-subtitle">
          This page can later display contacts, doctors, clinic licenses, working hours,
          branch addresses and FAQ from your backend or CMS.
        </p>
      </div>

      <article class="panel soft">
        <p class="mini-title">Contacts block</p>
        <p class="muted">Minsk, Lesnaya 14</p>
        <p class="muted">+375 29 700-10-10</p>
        <p class="muted">hello@fastpig.by</p>
      </article>
    </div>

    <section class="about-grid">
      <article v-for="fact in facts" :key="fact.title" class="tile">
        <h2 class="card-title">{{ fact.title }}</h2>
        <p class="muted">{{ fact.description }}</p>
      </article>
    </section>
  </section>
</template>

<script>
import { clinicFacts } from "../data/mock";

export default {
  name: "AboutView",
  data() {
    return {
      facts: clinicFacts,
    };
  },
};
</script>
