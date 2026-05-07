import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { initAuth } from './store/auth';

(async () => {
  await initAuth();            // проверили токен
  const app = createApp(App);
  app.use(router);
  app.mount('#app');
})();