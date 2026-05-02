<template>
  <section class="page">
    <div class="hero-card">
      <div>
        <span class="badge">Authorization</span>
        <h1 class="hero-title">Enter your FastPig account.</h1>
      </div>
    </div>

    <section class="split-grid">
      <!-- Логин -->
      <article class="panel">
        <h2 class="section-title">Login</h2>
        <div class="form-grid">
          <label class="field">
            <span>Email or phone</span>
            <input type="text" v-model="loginForm.login" placeholder="owner@fastpig.by or +375..." />
          </label>
          <label class="field">
            <span>Password</span>
            <input type="password" v-model="loginForm.password" placeholder="********" />
          </label>
        </div>
        <p v-if="authState.error" class="error-text">{{ authState.error }}</p>
        <div class="hero-actions">
          <button class="button" type="button" @click="handleLogin" :disabled="authState.isLoading">
            Sign in
          </button>
          <button class="button-secondary" type="button">Forgot password</button>
        </div>
      </article>

      <!-- Регистрация -->
      <article class="panel">
        <h2 class="section-title">Registration</h2>
        <div class="form-grid two">
          <label class="field">
            <span>Name</span>
            <input type="text" v-model="registerForm.name" placeholder="Anna" />
          </label>
          <label class="field">
            <span>Phone</span>
            <input type="text" v-model="registerForm.phone" placeholder="+375 29 000-00-00" />
          </label>
          <label class="field">
            <span>Email</span>
            <input type="email" v-model="registerForm.email" placeholder="anna@mail.com" />
          </label>
          <label class="field">
            <span>Password</span>
            <input type="password" v-model="registerForm.password" placeholder="Create password" />
          </label>
        </div>
        <p v-if="authState.error" class="error-text">{{ authState.error }}</p>
        <div class="hero-actions">
          <button class="button" type="button" @click="handleRegister" :disabled="authState.isLoading">
            Create account
          </button>
        </div>
      </article>
    </section>
  </section>
</template>

<script>
import { login, register, authState } from '@/store/auth';

export default {
  name: 'AuthView',
  data() {
    return {
      loginForm: { login: '', password: '' },
      registerForm: { name: '', phone: '', email: '', password: '' },
      authState: authState,   // <-- прокидываем реактивный объект в data
    };
  },
  // computed больше не нужен, удалите его
  methods: {
    async handleLogin() {
      try {
        await login(this.loginForm);
        this.$router.push('/');
      } catch {
        // ошибка теперь отобразится автоматически
      }
    },
    async handleRegister() {
      try {
        await register(this.registerForm);
        this.$router.push('/');
      } catch {
        // ошибка отобразится
      }
    },
  },
};
</script>

<style scoped>
.error-text {
  color: #e53e3e;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}
</style>