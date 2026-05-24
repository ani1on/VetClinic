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

      <button class="menu-toggle" type="button" @click="isMenuOpen = true">
        Menu
      </button>

      <!-- Десктопная навигация (остаётся без изменений) -->
      <nav class="main-nav desktop-nav">
        <router-link
          v-for="item in filteredNavigation"
          :key="item.to"
          :to="item.to"
          class="nav-link"
        >
          {{ item.label }}
        </router-link>

        <a
          v-if="!authState.isAuthenticated"
          class="nav-link"
          href="#"
          @click.prevent="goToAuth"
        >
          Auth
        </a>
        <a
          v-else
          class="nav-link"
          href="#"
          @click.prevent="handleLogout"
        >
          Logout
        </a>
      </nav>
    </header>

    <!-- Мобильный выдвижной ящик (drawer) -->
    <transition name="drawer-fade">
      <div v-if="isMenuOpen" class="drawer-overlay" @click="isMenuOpen = false"></div>
    </transition>
    <transition name="drawer-slide">
      <div v-if="isMenuOpen" class="drawer">
        <div class="drawer-header">
          <span class="drawer-title">Меню</span>
          <button class="drawer-close" @click="isMenuOpen = false">✕</button>
        </div>
        <nav class="drawer-nav">
          <router-link
            v-for="item in filteredNavigation"
            :key="item.to"
            :to="item.to"
            class="drawer-nav-link"
            @click="isMenuOpen = false"
          >
            {{ item.label }}
          </router-link>
          <a
            v-if="!authState.isAuthenticated"
            class="drawer-nav-link"
            href="#"
            @click.prevent="goToAuth"
          >
            Auth
          </a>
          <a
            v-else
            class="drawer-nav-link"
            href="#"
            @click.prevent="handleLogout"
          >
            Logout
          </a>
        </nav>
      </div>
    </transition>

    <main class="page-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { authState, logout } from '@/store/auth';

export default {
  name: "App",
  data() {
    return {
      isMenuOpen: false,
      authState: authState,
      allNavigation: [
        { label: "Home", to: "/" },
        { label: "Catalog", to: "/catalog" },
        { label: "Profile", to: "/profile" },
        { label: "Appointment", to: "/appointment" },
        { label: "Favorites", to: "/favorits" },   // исправлено
        { label: "About", to: "/about" },
        { label: "Admin", to: "/admin" },
      ],
    };
  },
  computed: {
    filteredNavigation() {
      if (!this.authState.isAuthenticated || this.authState.user?.role !== 'admin') {
        return this.allNavigation.filter(item => item.to !== '/admin');
      }
      return this.allNavigation;
    }
  },
  watch: {
    $route(to) {
      this.redirectIfAuthOnAuthPage(to);
    }
  },
  mounted() {
    this.redirectIfAuthOnAuthPage(this.$route);
  },
  methods: {
    redirectIfAuthOnAuthPage(route) {
      if (this.authState.isAuthenticated && route.path === '/auth') {
        this.$router.push('/');
      }
    },
    goToAuth() {
      this.isMenuOpen = false;
      this.$router.push('/auth');
    },
    async handleLogout() {
      this.isMenuOpen = false;
      await logout();
      this.$router.push('/auth');
    },
  },
};
</script>

<style>
/* ===== существующие переменные и общие стили (оставлены без изменений) ===== */
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

/* Десктопная навигация (видна только на широких экранах) */
.main-nav.desktop-nav {
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

/* Кнопка меню (показывается только на мобильных) */
.menu-toggle {
  display: none;
  padding: 10px 16px;
  border: 0;
  border-radius: 999px;
  background: var(--text);
  color: #fff;
  cursor: pointer;
}

/* ===== Стили для выдвижного ящика (drawer) ===== */
.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 100;
}

.drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: min(320px, 85%);
  background: var(--surface-strong);
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.1);
  z-index: 101;
  display: flex;
  flex-direction: column;
  padding: 20px;
  border-left: 1px solid var(--line);
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  margin-bottom: 16px;
  border-bottom: 1px solid var(--line);
}

.drawer-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text);
}

.drawer-close {
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: var(--muted);
  padding: 0;
  line-height: 1;
}

.drawer-nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.drawer-nav-link {
  padding: 12px 16px;
  border-radius: 20px;
  color: var(--text);
  font-weight: 600;
  transition: background 0.2s;
}

.drawer-nav-link.router-link-exact-active,
.drawer-nav-link:hover {
  background: var(--primary);
  color: #fff;
}

/* Анимации */
.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.2s ease;
}
.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}
.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 0.25s ease;
}
.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(100%);
}

/* ===== Адаптивность ===== */
@media (max-width: 980px) {
  .main-nav.desktop-nav {
    display: none;
  }
  .menu-toggle {
    display: inline-flex;
  }
}

/* остальные существующие медиа-запросы (можно оставить без изменений) */
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