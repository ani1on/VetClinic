import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AuthView from "../views/AuthView.vue";
import CatalogView from "../views/CatalogView.vue";
import ProfileView from "../views/ProfileView.vue";
import AppointmentView from "../views/AppointmentView.vue";
import FavoritesView from "../views/FavoritesView.vue";
import AboutView from "../views/AboutView.vue";
import AdminView from "../views/AdminView.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/auth", name: "auth", component: AuthView },
  { path: "/catalog", name: "catalog", component: CatalogView },
  { path: "/profile", name: "profile", component: ProfileView },
  { path: "/appointment", name: "appointment", component: AppointmentView },
  { path: "/favorits", name: "favorits", component: FavoritesView },
  { path: "/about", name: "about", component: AboutView },
  { path: "/admin", name: "admin", component: AdminView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
