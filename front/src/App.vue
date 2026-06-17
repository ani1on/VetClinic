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
  --blue: #4a90d9;
  --blue-light: rgba(74, 144, 217, 0.12);
  --purple: #8b5cf6;
  --purple-light: rgba(139, 92, 246, 0.12);
  --pink: #ec4899;
  --pink-light: rgba(236, 72, 153, 0.12);
  --yellow: #f59e0b;
  --yellow-light: rgba(245, 158, 11, 0.12);
  --shadow: 0 20px 50px rgba(128, 84, 52, 0.14);
  --shadow-sm: 0 4px 12px rgba(128, 84, 52, 0.08);
  --shadow-hover: 0 24px 60px rgba(128, 84, 52, 0.2);
  --shadow-colored: 0 12px 40px rgba(255, 122, 89, 0.18);
  --radius-xl: 32px;
  --radius-lg: 24px;
  --radius-md: 18px;
  --radius-sm: 12px;
  --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

* { box-sizing: border-box; }

body {
  margin: 0;
  min-width: 320px;
  background:
    radial-gradient(circle at top left, rgba(255, 183, 77, 0.25), transparent 30%),
    radial-gradient(circle at top right, rgba(58, 161, 126, 0.2), transparent 26%),
    radial-gradient(circle at bottom left, rgba(139, 92, 246, 0.1), transparent 30%),
    radial-gradient(circle at bottom right, rgba(236, 72, 153, 0.08), transparent 25%),
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
  width: min(1200px, calc(100% - 48px));
  margin: 0 auto;
  padding: 32px 0 64px;
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
  margin-bottom: 40px;
  padding: 16px 24px;
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
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: linear-gradient(135deg, #ff7a59, #ffb26b);
  color: #fff;
  font-weight: 800;
  font-size: 1.1rem;
  letter-spacing: 0.08em;
  transition: transform var(--transition);
  box-shadow: 0 4px 16px rgba(255, 122, 89, 0.3);
}
.brand-mark:hover { transform: scale(1.08) rotate(-3deg); }

.eyebrow {
  margin: 0 0 2px;
  color: var(--muted);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-weight: 600;
}
.brand-link {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--text), var(--primary-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ===== NAV ===== */
.main-nav.desktop-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 6px;
}
.nav-link {
  padding: 10px 18px;
  border-radius: 999px;
  color: var(--muted);
  font-weight: 600;
  font-size: 0.95rem;
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
  box-shadow: 0 4px 16px rgba(255, 122, 89, 0.3);
  padding: 10px 22px;
}
.nav-link-accent:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 122, 89, 0.4);
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
  padding: 12px 20px;
  border: 0;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--text), #4a3f3a);
  color: #fff;
  cursor: pointer;
  font-size: 1.3rem;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-sm);
}
.menu-toggle:hover {
  background: linear-gradient(135deg, var(--primary), #ffb26b);
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(255, 122, 89, 0.35);
}

/* ===== DRAWER ===== */
.drawer-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(6px);
  z-index: 100;
}
.drawer {
  position: fixed;
  top: 0; right: 0; bottom: 0;
  width: min(340px, 88%);
  background: var(--surface-strong);
  box-shadow: -8px 0 30px rgba(0, 0, 0, 0.12);
  z-index: 101;
  display: flex;
  flex-direction: column;
  padding: 24px;
  border-left: 1px solid var(--line);
}
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 2px solid var(--line);
}
.drawer-title {
  font-size: 1.5rem;
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
  width: 44px;
  height: 44px;
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
  gap: 6px;
}
.drawer-nav-link {
  padding: 16px 20px;
  border-radius: var(--radius-md);
  color: var(--text);
  font-weight: 600;
  transition: all var(--transition-fast);
  cursor: pointer;
  font-size: 1.05rem;
}
.drawer-nav-link:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
  transform: translateX(6px);
}
.drawer-nav-link.router-link-exact-active {
  background: linear-gradient(135deg, var(--primary), #ffb26b);
  color: #fff;
  box-shadow: 0 4px 16px rgba(255, 122, 89, 0.3);
}
.drawer-nav-accent {
  background: linear-gradient(135deg, var(--primary), #ffb26b);
  color: #fff !important;
  margin-top: 12px;
  box-shadow: 0 4px 16px rgba(255, 122, 89, 0.3);
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
  gap: 32px;
}
.page {
  display: flex;
  flex-direction: column;
  gap: 32px;
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
  transform: translateY(-6px);
  box-shadow: var(--shadow-hover);
}
.hero-card {
  position: relative;
  overflow: hidden;
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(300px, 0.8fr);
  gap: 32px;
  padding: 40px;
  background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,248,240,0.9));
}
.hero-card::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--accent), var(--purple), var(--pink));
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
.hero-card::after {
  content: "";
  position: absolute;
  inset: auto -100px -100px auto;
  width: 280px;
  height: 280px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 122, 89, 0.12), rgba(58, 161, 126, 0.08));
  transition: transform 0.6s ease;
}
.hero-card:hover::after { transform: scale(1.2); }

.hero-title {
  margin: 0;
  font-size: clamp(2.4rem, 4.5vw, 4.8rem);
  line-height: 1;
  letter-spacing: -0.02em;
}
.hero-subtitle {
  margin: 18px 0 0;
  max-width: 620px;
  color: var(--muted);
  font-size: 1.1rem;
  line-height: 1.8;
}
.hero-actions,
.inline-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 28px;
}

/* ===== BUTTONS ===== */
.button,
.button-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 24px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
  letter-spacing: 0.01em;
}
.button {
  background: linear-gradient(135deg, var(--primary), #ffb26b);
  color: #fff;
  box-shadow: 0 4px 16px rgba(255, 122, 89, 0.3);
}
.button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(255, 122, 89, 0.4);
}
.button:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}
.button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
.button-secondary {
  border: 2px solid var(--line);
  background: #fff;
  color: var(--text);
}
.button-secondary:hover {
  border-color: var(--primary);
  color: var(--primary-dark);
  background: var(--primary-light);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 122, 89, 0.15);
}
.button-secondary:active {
  transform: translateY(0);
}

/* ===== HERO ===== */
.hero-aside {
  display: grid;
  gap: 16px;
}
.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 10px 16px;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--accent-light), rgba(58, 161, 126, 0.06));
  color: var(--accent);
  font-weight: 700;
  border: 1px solid rgba(58, 161, 126, 0.2);
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
  gap: 24px;
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
  padding: 28px;
}
.stat-card {
  position: relative;
  overflow: hidden;
}
.stat-card::before {
  content: "";
  position: absolute;
  top: 0; left: 0;
  width: 4px;
  height: 100%;
  border-radius: 4px 0 0 4px;
}
.stat-card:nth-child(1)::before { background: linear-gradient(180deg, var(--primary), #ffb26b); }
.stat-card:nth-child(2)::before { background: linear-gradient(180deg, var(--accent), #6dd5b0); }
.stat-card:nth-child(3)::before { background: linear-gradient(180deg, var(--blue), #7bc4f5); }
.stat-card:nth-child(4)::before { background: linear-gradient(180deg, var(--purple), #c4b5fd); }

.stat-value {
  margin: 0;
  font-size: 2.4rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-label,
.muted {
  margin: 10px 0 0;
  color: var(--muted);
  line-height: 1.7;
  font-size: 0.95rem;
}

/* ===== SECTION ===== */
.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 4px;
}
.section-title {
  margin: 0;
  font-size: 2rem;
  letter-spacing: -0.01em;
}
.section-copy {
  margin: 10px 0 0;
  color: var(--muted);
  max-width: 700px;
  line-height: 1.7;
  font-size: 1rem;
}

/* ===== CHIPS ===== */
.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.chip {
  padding: 9px 16px;
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
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(255, 122, 89, 0.3);
}
.chip.active {
  background: linear-gradient(135deg, var(--primary), #ffb26b);
  color: #fff;
  border-color: var(--primary-dark);
  box-shadow: 0 4px 16px rgba(255, 122, 89, 0.35);
}

/* ===== ROWS ===== */
.price-row,
.meta-row,
.list-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}
.list-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--line), transparent);
  margin: 8px 0;
}

/* ===== TITLES ===== */
.mini-title,
.card-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.01em;
}

/* ===== FORMS ===== */
.form-grid {
  display: grid;
  gap: 18px;
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
  color: var(--text);
}
.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 14px 18px;
  border: 2px solid rgba(91, 66, 52, 0.12);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.95);
  color: var(--text);
  transition: all var(--transition-fast);
  font-size: 0.95rem;
}
.field input:focus,
.field select:focus,
.field textarea:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(255, 122, 89, 0.12);
  outline: none;
  background: #fff;
}
.field input::placeholder,
.field textarea::placeholder {
  color: var(--muted);
  opacity: 0.5;
}
.field textarea {
  min-height: 120px;
  resize: vertical;
}

.feed-card {
  display: grid;
  gap: 14px;
}
.kpi {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 800;
}
.soft {
  padding: 20px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary-light), rgba(255, 178, 107, 0.08));
}
.success {
  background: linear-gradient(135deg, var(--accent-light), rgba(109, 213, 176, 0.08));
}
.warn {
  background: linear-gradient(135deg, var(--yellow-light), rgba(255, 208, 122, 0.15));
}

/* ===== IMAGE CARDS ===== */
.card-image {
  width: 100%;
  height: 220px;
  object-fit: cover;
  border-radius: var(--radius-md);
  transition: transform var(--transition);
}
.tile:hover .card-image {
  transform: scale(1.04);
}
.admin-card-image {
  width: 100%;
  height: 190px;
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
    width: min(100% - 24px, 1200px);
    padding-top: 16px;
  }
  .topbar,
  .hero-card,
  .panel,
  .tile,
  .stat-card,
  .feed-card {
    padding: 20px;
  }
  .hero-card {
    padding: 24px;
  }
  .brand-link {
    font-size: 1.25rem;
  }
  .hero-title {
    font-size: clamp(1.8rem, 5vw, 2.8rem);
  }
  .section-title {
    font-size: 1.6rem;
  }
}
</style>
