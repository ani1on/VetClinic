import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AuthView from "../views/AuthView.vue";
import CatalogView from "../views/CatalogView.vue";
import ProfileView from "../views/ProfileView.vue";
import AppointmentView from "../views/AppointmentView.vue";
import FavoritesView from "../views/FavoritesView.vue";
import AboutView from "../views/AboutView.vue";
import AdminView from "../views/AdminView.vue";
import NotFoundView from '@/views/NotFoundView.vue';
import { authState } from '@/store/auth';

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
  // 1. Проверка обычной авторизации
  if (to.meta.requiresAuth && !authState.isAuthenticated) {
    next('/auth');
    return;
  }

  // 2. Проверка прав администратора
  if (to.meta.requiresAdmin && (!authState.user || authState.user.role !== 'admin')) {
    // Если не админ – отправляем на главную (можно заменить на '/auth')
    next({ name: 'home' });
    return;
  }

  // 3. Запрет входа на страницу авторизации для уже вошедших
  if (to.name === 'auth' && authState.isAuthenticated) {
    next({ name: 'home' });
    return;
  }

  next();
});

export default router;