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
        <span class="menu-icon">☰</span>
      </button>

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
          class="nav-link nav-link-accent"
          href="#"
          @click.prevent="goToAuth"
        >
          Войти
        </a>
        <a
          v-else
          class="nav-link nav-link-logout"
          href="#"
          @click.prevent="handleLogout"
        >
          Выйти
        </a>
      </nav>
    </header>

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
            class="drawer-nav-link drawer-nav-accent"
            href="#"
            @click.prevent="goToAuth"
          >
            Войти
          </a>
          <a
            v-else
            class="drawer-nav-link drawer-nav-logout"
            href="#"
            @click.prevent="handleLogout"
          >
            Выйти
          </a>
        </nav>
      </div>
    </transition>

    <main class="page-content">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
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
        { label: "Главная", to: "/" },
        { label: "Каталог", to: "/catalog" },
        { label: "Профиль", to: "/profile" },
        { label: "Запись", to: "/appointment" },
        { label: "Избранное", to: "/favorits" },
        { label: "О нас", to: "/about" },
        { label: "Админ", to: "/admin" },
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
  --primary-light: rgba(255, 122, 89, 0.12);
  --accent: #3aa17e;
  --accent-light: rgba(58, 161, 126, 0.12);
  --shadow: 0 20px 50px rgba(128, 84, 52, 0.14);
  --shadow-sm: 0 4px 12px rgba(128, 84, 52, 0.08);
  --shadow-hover: 0 24px 60px rgba(128, 84, 52, 0.2);
  --radius-xl: 32px;
  --radius-lg: 24px;
  --radius-md: 18px;
  --radius-sm: 12px;
  --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
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

a { color: inherit; text-decoration: none; }

button, input, select, textarea {
  font: inherit;
  outline: none;
}

#app { min-height: 100vh; }

.app-shell {
  width: min(1200px, calc(100% - 32px));
  margin: 0 auto;
  padding: 24px 0 48px;
}

/* ===== TOPBAR ===== */
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
  transition: box-shadow var(--transition);
}
.topbar:hover { box-shadow: var(--shadow-hover); }

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
  transition: transform var(--transition);
}
.brand-mark:hover { transform: scale(1.05) rotate(-2deg); }

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

/* ===== NAV ===== */
.main-nav.desktop-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 8px;
}
.nav-link {
  padding: 10px 16px;
  border-radius: 999px;
  color: var(--muted);
  font-weight: 600;
  transition: all var(--transition-fast);
  cursor: pointer;
}
.nav-link:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
  transform: translateY(-1px);
}
.nav-link.router-link-exact-active {
  background: var(--text);
  color: #fff;
  box-shadow: var(--shadow-sm);
}
.nav-link.router-link-exact-active:hover {
  background: var(--primary);
  transform: translateY(-1px);
}
.nav-link-accent {
  background: linear-gradient(135deg, var(--primary), #ffb26b);
  color: #fff !important;
  box-shadow: var(--shadow-sm);
}
.nav-link-accent:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 122, 89, 0.35);
}
.nav-link-logout {
  color: var(--muted) !important;
  border: 1px solid var(--line);
}
.nav-link-logout:hover {
  background: rgba(229, 62, 62, 0.08);
  color: #e53e3e !important;
  border-color: rgba(229, 62, 62, 0.2);
}

/* ===== MOBILE MENU ===== */
.menu-toggle {
  display: none;
  padding: 10px 16px;
  border: 0;
  border-radius: 999px;
  background: var(--text);
  color: #fff;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all var(--transition-fast);
}
.menu-toggle:hover {
  background: var(--primary);
  transform: scale(1.05);
}

/* ===== DRAWER ===== */
.drawer-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 100;
}
.drawer {
  position: fixed;
  top: 0; right: 0; bottom: 0;
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
  transition: all var(--transition-fast);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.drawer-close:hover {
  background: rgba(229, 62, 62, 0.08);
  color: #e53e3e;
  transform: rotate(90deg);
}
.drawer-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.drawer-nav-link {
  padding: 14px 18px;
  border-radius: var(--radius-md);
  color: var(--text);
  font-weight: 600;
  transition: all var(--transition-fast);
  cursor: pointer;
}
.drawer-nav-link:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
  transform: translateX(4px);
}
.drawer-nav-link.router-link-exact-active {
  background: var(--primary);
  color: #fff;
  box-shadow: var(--shadow-sm);
}
.drawer-nav-accent {
  background: linear-gradient(135deg, var(--primary), #ffb26b);
  color: #fff !important;
  margin-top: 8px;
}
.drawer-nav-logout {
  color: var(--muted) !important;
  border: 1px solid var(--line);
  margin-top: 8px;
}
.drawer-nav-logout:hover {
  background: rgba(229, 62, 62, 0.08);
  color: #e53e3e !important;
}

/* ===== ANIMATIONS ===== */
.drawer-fade-enter-active,
.drawer-fade-leave-active { transition: opacity 0.3s ease; }
.drawer-fade-enter-from,
.drawer-fade-leave-to { opacity: 0; }

.drawer-slide-enter-active,
.drawer-slide-leave-active { transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1); }
.drawer-slide-enter-from,
.drawer-slide-leave-to { transform: translateX(100%); }

.page-fade-enter-active,
.page-fade-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.page-fade-enter-from { opacity: 0; transform: translateY(8px); }
.page-fade-leave-to { opacity: 0; transform: translateY(-8px); }

/* ===== LAYOUT ===== */
.page-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInUp 0.4s ease;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== CARDS ===== */
.hero-card,
.panel,
.tile,
.stat-card,
.feed-card {
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  background: var(--surface);
  box-shadow: var(--shadow);
  transition: all var(--transition);
}
.tile:hover,
.stat-card:hover,
.feed-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
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
  transition: transform 0.6s ease;
}
.hero-card:hover::after { transform: scale(1.15); }

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

/* ===== BUTTONS ===== */
.button,
.button-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 20px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
}
.button {
  background: linear-gradient(135deg, var(--primary), #ffb26b);
  color: #fff;
  box-shadow: var(--shadow-sm);
}
.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 122, 89, 0.35);
}
.button:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
.button-secondary {
  border: 1px solid var(--line);
  background: #fff;
  color: var(--text);
}
.button-secondary:hover {
  border-color: var(--primary);
  color: var(--primary-dark);
  background: var(--primary-light);
  transform: translateY(-1px);
}
.button-secondary:active {
  transform: translateY(0);
}

/* ===== HERO ===== */
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
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 700;
  animation: fadeInUp 0.5s ease;
}

/* ===== GRIDS ===== */
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
.stats-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.tile-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.split-grid { grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr); }
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
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-label,
.muted {
  margin: 8px 0 0;
  color: var(--muted);
  line-height: 1.6;
}

/* ===== SECTION ===== */
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

/* ===== CHIPS ===== */
.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.chip {
  padding: 8px 14px;
  border-radius: 999px;
  background: var(--primary-light);
  color: var(--primary-dark);
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid transparent;
}
.chip:hover {
  background: var(--primary);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}
.chip.active {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary-dark);
  box-shadow: var(--shadow-sm);
}

/* ===== ROWS ===== */
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

/* ===== TITLES ===== */
.mini-title,
.card-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 800;
}

/* ===== FORMS ===== */
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
  font-size: 0.95rem;
}
.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 13px 16px;
  border: 2px solid rgba(91, 66, 52, 0.12);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.92);
  color: var(--text);
  transition: all var(--transition-fast);
}
.field input:focus,
.field select:focus,
.field textarea:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(255, 122, 89, 0.12);
  outline: none;
}
.field input::placeholder,
.field textarea::placeholder {
  color: var(--muted);
  opacity: 0.6;
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
  background: var(--primary-light);
}
.success {
  background: var(--accent-light);
}
.warn {
  background: rgba(255, 208, 122, 0.25);
}

/* ===== IMAGE CARDS ===== */
.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: var(--radius-md);
  transition: transform var(--transition);
}
.tile:hover .card-image {
  transform: scale(1.03);
}
.admin-card-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: var(--radius-md);
}

/* ===== LOADING ===== */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.skeleton {
  background: linear-gradient(90deg, var(--line) 25%, rgba(255,255,255,0.5) 50%, var(--line) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}

/* ===== RESPONSIVE ===== */
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
  .hero-title {
    font-size: clamp(1.6rem, 5vw, 2.5rem);
  }
}
</style>
