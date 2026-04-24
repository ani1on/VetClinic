<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand-block">
        <div class="brand-mark">FP</div>
        <div>
          <p class="eyebrow">Veterinary care platform</p>
          <router-link class="brand-link" to="/">FastPig</router-link>
        </div>
      </div>

      <button class="menu-toggle" type="button" @click="isMenuOpen = !isMenuOpen">
        {{ isMenuOpen ? "Close" : "Menu" }}
      </button>

      <nav class="main-nav" :class="{ open: isMenuOpen }">
        <router-link
          v-for="item in navigation"
          :key="item.to"
          :to="item.to"
          class="nav-link"
          @click="isMenuOpen = false"
        >
          {{ item.label }}
        </router-link>
      </nav>
    </header>

    <main class="page-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      isMenuOpen: false,
      navigation: [
        { label: "Auth", to: "/auth" },
        { label: "Home", to: "/" },
        { label: "Catalog", to: "/catalog" },
        { label: "Profile", to: "/profile" },
        { label: "Appointment", to: "/appointment" },
        { label: "Favorits", to: "/favorits" },
        { label: "About", to: "/about" },
        { label: "Admin", to: "/admin" },
      ],
    };
  },
};
</script>

<style>
:root {
  --bg: #fffaf4;
  --bg-strong: #ffe8d6;
  --surface: rgba(255, 255, 255, 0.86);
  --surface-strong: #ffffff;
  --text: #2f241f;
  --muted: #6d5f57;
  --line: rgba(91, 66, 52, 0.12);
  --primary: #ff7a59;
  --primary-dark: #dd5b3b;
  --accent: #3aa17e;
  --shadow: 0 20px 50px rgba(128, 84, 52, 0.14);
  --radius-xl: 32px;
  --radius-lg: 24px;
  --radius-md: 18px;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-width: 320px;
  background:
    radial-gradient(circle at top left, rgba(255, 183, 77, 0.22), transparent 28%),
    radial-gradient(circle at top right, rgba(58, 161, 126, 0.18), transparent 24%),
    linear-gradient(180deg, #fff9f2 0%, #fff5ea 55%, #fffaf4 100%);
  color: var(--text);
  font-family: "Trebuchet MS", "Segoe UI", sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
}

button,
input,
select,
textarea {
  font: inherit;
}

#app {
  min-height: 100vh;
}

.app-shell {
  width: min(1200px, calc(100% - 32px));
  margin: 0 auto;
  padding: 24px 0 48px;
}

.topbar {
  position: sticky;
  top: 16px;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 28px;
  padding: 18px 22px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow);
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 54px;
  height: 54px;
  border-radius: 18px;
  background: linear-gradient(135deg, #ff7a59, #ffb26b);
  color: #fff;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.eyebrow {
  margin: 0 0 2px;
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.brand-link {
  font-size: 1.6rem;
  font-weight: 800;
}

.main-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
}

.nav-link {
  padding: 10px 16px;
  border-radius: 999px;
  color: var(--muted);
  transition: 0.2s ease;
}

.nav-link.router-link-exact-active,
.nav-link:hover {
  background: var(--text);
  color: #fff;
}

.menu-toggle {
  display: none;
  padding: 10px 16px;
  border: 0;
  border-radius: 999px;
  background: var(--text);
  color: #fff;
}

.page-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero-card,
.panel,
.tile,
.stat-card,
.feed-card {
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  background: var(--surface);
  box-shadow: var(--shadow);
}

.hero-card {
  position: relative;
  overflow: hidden;
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(300px, 0.8fr);
  gap: 24px;
  padding: 32px;
}

.hero-card::after {
  content: "";
  position: absolute;
  inset: auto -90px -90px auto;
  width: 240px;
  height: 240px;
  border-radius: 50%;
  background: rgba(255, 122, 89, 0.13);
}

.hero-title {
  margin: 0;
  font-size: clamp(2.2rem, 4vw, 4.6rem);
  line-height: 0.95;
}

.hero-subtitle {
  margin: 14px 0 0;
  max-width: 620px;
  color: var(--muted);
  font-size: 1.05rem;
  line-height: 1.7;
}

.hero-actions,
.inline-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}

.button,
.button-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 18px;
  border-radius: 999px;
  font-weight: 700;
}

.button {
  border: 0;
  background: linear-gradient(135deg, var(--primary), #ffb26b);
  color: #fff;
}

.button-secondary {
  border: 1px solid var(--line);
  background: #fff;
  color: var(--text);
}

.hero-aside {
  display: grid;
  gap: 14px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(58, 161, 126, 0.12);
  color: var(--accent);
  font-weight: 700;
}

.stats-grid,
.tile-grid,
.split-grid,
.catalog-grid,
.favorites-grid,
.schedule-grid,
.admin-grid,
.about-grid {
  display: grid;
  gap: 18px;
}

.stats-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.tile-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.split-grid {
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
}

.catalog-grid,
.favorites-grid,
.schedule-grid,
.admin-grid,
.about-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.stat-card,
.tile,
.panel,
.feed-card {
  padding: 24px;
}

.stat-value {
  margin: 0;
  font-size: 2rem;
  font-weight: 800;
}

.stat-label,
.muted {
  margin: 8px 0 0;
  color: var(--muted);
  line-height: 1.6;
}

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 16px;
}

.section-title {
  margin: 0;
  font-size: 1.8rem;
}

.section-copy {
  margin: 8px 0 0;
  color: var(--muted);
  max-width: 700px;
  line-height: 1.7;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 122, 89, 0.12);
  color: var(--primary-dark);
  font-size: 0.95rem;
  font-weight: 700;
}

.price-row,
.meta-row,
.list-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.list-column {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.divider {
  height: 1px;
  background: var(--line);
}

.mini-title,
.card-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 800;
}

.form-grid {
  display: grid;
  gap: 14px;
}

.form-grid.two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.field {
  display: grid;
  gap: 8px;
}

.field span {
  font-weight: 700;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 13px 14px;
  border: 1px solid rgba(91, 66, 52, 0.15);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.92);
  color: var(--text);
}

.field textarea {
  min-height: 110px;
  resize: vertical;
}

.feed-card {
  display: grid;
  gap: 12px;
}

.kpi {
  margin: 0;
  font-size: 2.3rem;
  font-weight: 800;
}

.soft {
  padding: 16px;
  border-radius: 18px;
  background: rgba(255, 122, 89, 0.08);
}

.success {
  background: rgba(58, 161, 126, 0.12);
}

.warn {
  background: rgba(255, 208, 122, 0.25);
}

@media (max-width: 980px) {
  .hero-card,
  .split-grid,
  .stats-grid,
  .tile-grid,
  .catalog-grid,
  .favorites-grid,
  .schedule-grid,
  .admin-grid,
  .about-grid,
  .form-grid.two {
    grid-template-columns: 1fr;
  }

  .topbar {
    align-items: flex-start;
    border-radius: 28px;
  }

  .menu-toggle {
    display: inline-flex;
  }

  .main-nav {
    display: none;
    width: 100%;
    justify-content: flex-start;
    padding-top: 8px;
  }

  .main-nav.open {
    display: flex;
  }
}

@media (max-width: 640px) {
  .app-shell {
    width: min(100% - 20px, 1200px);
    padding-top: 12px;
  }

  .topbar,
  .hero-card,
  .panel,
  .tile,
  .stat-card,
  .feed-card {
    padding: 18px;
  }

  .brand-link {
    font-size: 1.25rem;
  }
}
</style>
