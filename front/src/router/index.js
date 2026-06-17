import { createRouter, createWebHistory } from "vue-router";
import { authState } from '@/store/auth';
import { captureUTMFromCurrentURL } from '@/utils/utm';

const HomeView = () => import(/* webpackChunkName: "home" */ "../views/HomeView.vue");
const AuthView = () => import(/* webpackChunkName: "auth" */ "../views/AuthView.vue");
const CatalogView = () => import(/* webpackChunkName: "catalog" */ "../views/CatalogView.vue");
const ProfileView = () => import(/* webpackChunkName: "profile" */ "../views/ProfileView.vue");
const AppointmentView = () => import(/* webpackChunkName: "appointment" */ "../views/AppointmentView.vue");
const FavoritesView = () => import(/* webpackChunkName: "favorites" */ "../views/FavoritesView.vue");
const AboutView = () => import(/* webpackChunkName: "about" */ "../views/AboutView.vue");
const AdminView = () => import(/* webpackChunkName: "admin" */ "../views/AdminView.vue");
const NotFoundView = () => import(/* webpackChunkName: "not-found" */ "../views/NotFoundView.vue");

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/auth", name: "auth", component: AuthView },
  { path: "/catalog", name: "catalog", component: CatalogView, meta: { requiresAuth: true } },
  { path: "/profile", name: "profile", component: ProfileView, meta: { requiresAuth: true } },
  { path: "/appointment", name: "appointment", component: AppointmentView, meta: { requiresAuth: true } },
  { path: "/favorits", name: "favorits", component: FavoritesView, meta: { requiresAuth: true } },
  { path: "/about", name: "about", component: AboutView },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView },
  { path: "/admin", name: "admin", component: AdminView, meta: { requiresAuth: true, requiresAdmin: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach((to, from, next) => {
  captureUTMFromCurrentURL();

  if (to.meta.requiresAuth && !authState.isAuthenticated) {
    next('/auth');
    return;
  }

  if (to.meta.requiresAdmin && (!authState.user || authState.user.role !== 'admin')) {
    next({ name: 'home' });
    return;
  }

  if (to.name === 'auth' && authState.isAuthenticated) {
    next({ name: 'home' });
    return;
  }

  next();
});

router.afterEach((to) => {
  if (typeof window.ym === 'function') {
    window.ym(109920587, 'hit', to.fullPath);
  }
});

export default router;
