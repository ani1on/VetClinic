<template>
  <section class="page">
    <div class="hero-card">
      <div>
        <span class="badge">Authorization</span>
        <h1 class="hero-title">Enter your FastPig account.</h1>
        <p class="hero-subtitle">
          This page is ready for integration with your backend login, register,
          refresh token and password recovery logic.
        </p>
      </div>

      <div class="panel soft success">
        <p class="mini-title">What to connect later</p>
        <div class="chip-row">
          <span class="chip">JWT</span>
          <span class="chip">Refresh token</span>
          <span class="chip">Role check</span>
        </div>
      </div>
    </div>

    <section class="split-grid">
      <article class="panel">
        <h2 class="section-title">Login</h2>
        <div class="form-grid">
          <label class="field">
            <span>Email</span>
            <input type="email" placeholder="owner@fastpig.by" />
          </label>
          <label class="field">
            <span>Password</span>
            <input type="password" placeholder="********" />
          </label>
        </div>
        <div class="hero-actions">
          <button class="button" type="button">Sign in</button>
          <button class="button-secondary" type="button">Forgot password</button>
        </div>
      </article>

      <article class="panel">
        <h2 class="section-title">Registration</h2>
        <div class="form-grid two">
          <label class="field">
            <span>Name</span>
            <input type="text" placeholder="Anna" />
          </label>
          <label class="field">
            <span>Phone</span>
            <input type="text" placeholder="+375 29 000-00-00" />
          </label>
          <label class="field">
            <span>Email</span>
            <input type="email" placeholder="anna@mail.com" />
          </label>
          <label class="field">
            <span>Password</span>
            <input type="password" placeholder="Create password" />
          </label>
        </div>
        <div class="hero-actions">
          <button class="button" type="button">Create account</button>
        </div>
      </article>
    </section>
  </section>
</template>

<script>
import { login, register, authState } from '@/store/auth';

export default {
  name: "AuthView",
  data() {
    return {
      // данные формы логина
      loginForm: {
        login: '',
        password: '',
      },
      // данные формы регистрации
      registerForm: {
        name: '',
        phone: '',
        email: '',
        password: '',
      },
    };
  },
  methods: {
    async handleLogin() {
      try {
        await login(this.loginForm);
        this.$router.push('/'); // после успешного входа перенаправь на главную
      } catch {
        // ошибка уже в authState.error, можно показать
      }
    },
    async handleRegister() {
      try {
        await register(this.registerForm);
        this.$router.push('/');
      } catch {
        // обработка
      }
    },
  },
};
</script>
