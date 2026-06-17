/* eslint-disable no-useless-escape */
<template>
  <section class="page">
    <div v-if="toastMessage" class="toast" :class="toastType">{{ toastMessage }}</div>

    <!-- Модальное окно "Забыли пароль?" -->
    <div v-if="showForgotModal" class="modal-overlay" @click.self="closeForgotModal">
      <div class="modal-container">
        <div class="modal-header">
          <h3 class="modal-title">Восстановление пароля</h3>
          <button class="modal-close" @click="closeForgotModal">✕</button>
        </div>
        <div class="modal-body">
          <p class="modal-description">
            Введите email, указанный при регистрации. Мы отправим ссылку для сброса пароля.
          </p>
          <label class="field">
            <span>Email</span>
            <input type="email" v-model="forgotEmail" placeholder="your@email.com" />
          </label>
          <p v-if="forgotError" class="error-text">{{ forgotError }}</p>
        </div>
        <div class="modal-footer">
          <button class="button-secondary" @click="closeForgotModal">Отмена</button>
          <button class="button" @click="requestPasswordReset" :disabled="forgotLoading">
            {{ forgotLoading ? 'Отправка…' : 'Отправить' }}
          </button>
        </div>
      </div>
    </div>

    <div class="hero-card">
      <div>
        <span class="badge">Авторизация</span>
        <h1 class="hero-title">Войдите в свой аккаунт FastPig.</h1>
      </div>
    </div>

    <section class="split-grid">
      <!-- Логин -->
      <article class="panel">
        <h2 class="section-title">Вход</h2>
        <div class="form-grid">
          <label class="field">
            <span>Email или телефон</span>
            <input type="text" v-model="loginForm.login" placeholder="owner@fastpig.by или +375..." />
            <span v-if="loginErrors.login" class="field-error">{{ loginErrors.login }}</span>
          </label>
          <label class="field">
            <span>Пароль</span>
            <input type="password" v-model="loginForm.password" placeholder="********" />
            <span v-if="loginErrors.password" class="field-error">{{ loginErrors.password }}</span>
          </label>
        </div>
        <p v-if="authState.error" class="error-text">{{ authState.error }}</p>
        <div class="hero-actions">
          <button class="button" type="button" @click="handleLogin" :disabled="authState.isLoading">
            {{ authState.isLoading ? 'Вход…' : 'Войти' }}
          </button>
          <button class="button-secondary" type="button" @click="openForgotModal">
            Забыли пароль?
          </button>
        </div>
      </article>

      <!-- Регистрация -->
      <article class="panel">
        <h2 class="section-title">Регистрация</h2>
        <div class="form-grid two">
          <label class="field">
            <span>Имя</span>
            <input type="text" v-model="registerForm.name" placeholder="Анна" />
            <span v-if="registerErrors.name" class="field-error">{{ registerErrors.name }}</span>
          </label>
          <label class="field">
            <span>Телефон</span>
            <input type="text" v-model="registerForm.phone" placeholder="+375 29 000-00-00" />
            <span v-if="registerErrors.phone" class="field-error">{{ registerErrors.phone }}</span>
          </label>
          <label class="field">
            <span>Email</span>
            <input type="email" v-model="registerForm.email" placeholder="anna@mail.com" />
            <span v-if="registerErrors.email" class="field-error">{{ registerErrors.email }}</span>
          </label>
          <div></div>
          <label class="field field-full">
            <span>Пароль</span>
            <input type="password" v-model="registerForm.password" placeholder="Придумайте пароль" @input="checkPasswordStrength" />
            <span v-if="registerErrors.password" class="field-error">{{ registerErrors.password }}</span>
            <div v-if="registerForm.password" class="password-strength">
              <div class="strength-bar" :class="passwordStrengthClass"></div>
              <span class="strength-text" :class="passwordStrengthClass">{{ passwordStrengthText }}</span>
              <ul class="password-requirements">
                <li :class="{ met: hasMinLength }">✔ Минимум 8 символов</li>
                <li :class="{ met: hasUppercase }">✔ Заглавная буква (A-Z)</li>
                <li :class="{ met: hasDigit }">✔ Цифра (0-9)</li>
                <li :class="{ met: hasSpecialChar }">✔ Спецсимвол (!@#$%^&* и т.д.)</li>
              </ul>
            </div>
          </label>
          <label class="field">
            <span>Подтверждение пароля</span>
            <input type="password" v-model="registerForm.confirmPassword" placeholder="Повторите пароль" />
            <span v-if="registerErrors.confirmPassword" class="field-error">{{ registerErrors.confirmPassword }}</span>
          </label>
        </div>
        <p v-if="registerFormGeneralError" class="error-text">{{ registerFormGeneralError }}</p>
        <div class="hero-actions">
          <button class="button" type="button" @click="handleRegister" :disabled="authState.isLoading || !isPasswordValid">
            {{ authState.isLoading ? 'Регистрация…' : 'Создать аккаунт' }}
          </button>
        </div>
      </article>
    </section>
  </section>
</template>

<script>
import { login, register, authState } from '@/store/auth';
// Импорт сервиса для восстановления пароля (создать при необходимости)
// import authService from '@/services/authService';

export default {
  name: 'AuthView',
  data() {
    return {
      loginForm: { login: '', password: '' },
      registerForm: {
        name: '',
        phone: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      authState,
      toastMessage: '',
      toastType: '',
      loginErrors: { login: '', password: '' },
      registerErrors: { name: '', phone: '', email: '', password: '', confirmPassword: '' },
      registerFormGeneralError: '',
      passwordStrength: 0,
      // Forgot password
      showForgotModal: false,
      forgotEmail: '',
      forgotLoading: false,
      forgotError: null,
    };
  },
  computed: {
    hasMinLength() {
      return this.registerForm.password.length >= 8;
    },
    hasUppercase() {
      return /[A-Z]/.test(this.registerForm.password);
    },
    hasDigit() {
      return /\d/.test(this.registerForm.password);
    },
    hasSpecialChar() {
      return /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(this.registerForm.password);
    },
    passwordStrengthText() {
      if (this.passwordStrength === 2) return 'Сильный пароль';
      if (this.passwordStrength === 1) return 'Средний пароль';
      return 'Слабый пароль';
    },
    passwordStrengthClass() {
      if (this.passwordStrength === 2) return 'strong';
      if (this.passwordStrength === 1) return 'medium';
      return 'weak';
    },
    isPasswordValid() {
      return this.passwordStrength >= 1;
    }
  },
  methods: {
    showToast(text, type = 'success') {
      this.toastMessage = text;
      this.toastType = type;
      setTimeout(() => { this.toastMessage = ''; }, 3000);
    },

    parseApiError(error) {
      if (!error.response) {
        return 'Не удалось соединиться с сервером. Проверьте подключение к интернету.';
      }
      const status = error.response.status;
      if (status >= 500 && status <= 503) {
        return 'Сервер временно недоступен. Попробуйте позже.';
      }
      const data = error.response.data;
      if (data) {
        if (Array.isArray(data) && data[0]?.loc) {
          return data.map(err => {
            const field = err.loc[err.loc.length - 1];
            let msg = err.msg;
            if (err.type === 'string_too_short') msg = `поле должно содержать минимум ${err.ctx.min_length} символов`;
            if (err.type === 'string_pattern_mismatch') msg = 'неверный формат (пример: +375291234567)';
            return `${field}: ${msg}`;
          }).join('; ');
        }
        if (data.detail) {
          if (typeof data.detail === 'string') return data.detail;
          if (Array.isArray(data.detail)) return data.detail.map(d => d.msg).join('; ');
        }
        if (data.message) return data.message;
      }
      return 'Произошла ошибка. Попробуйте обновить страницу.';
    },

    checkPasswordStrength() {
      const pwd = this.registerForm.password;
      if (!pwd) {
        this.passwordStrength = 0;
        return;
      }
      let score = 0;
      if (pwd.length >= 8) score++;
      if (/[A-Z]/.test(pwd)) score++;
      if (/\d/.test(pwd)) score++;
      if (/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(pwd)) score++;
      if (score >= 4) this.passwordStrength = 2;
      else if (score >= 3) this.passwordStrength = 1;
      else this.passwordStrength = 0;
    },

    validateLogin() {
      let isValid = true;
      this.loginErrors = { login: '', password: '' };
      if (!this.loginForm.login.trim()) {
        this.loginErrors.login = 'Введите email или телефон';
        isValid = false;
      }
      if (!this.loginForm.password) {
        this.loginErrors.password = 'Введите пароль';
        isValid = false;
      }
      return isValid;
    },

    validateRegister() {
      let isValid = true;
      this.registerErrors = { name: '', phone: '', email: '', password: '', confirmPassword: '' };
      this.registerFormGeneralError = '';

      if (!this.registerForm.name.trim()) {
        this.registerErrors.name = 'Имя обязательно';
        isValid = false;
      }
      const phoneRegex = /^\+?\d{10,15}$/;
      if (!this.registerForm.phone.trim()) {
        this.registerErrors.phone = 'Телефон обязателен';
        isValid = false;
      } else if (!phoneRegex.test(this.registerForm.phone.replace(/[\s-]/g, ''))) {
        this.registerErrors.phone = 'Неверный формат телефона (10-15 цифр, может начинаться с +)';
        isValid = false;
      }
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
      if (!this.registerForm.email.trim()) {
        this.registerErrors.email = 'Email обязателен';
        isValid = false;
      } else if (!emailRegex.test(this.registerForm.email)) {
        this.registerErrors.email = 'Введите корректный email (пример: name@domain.com)';
        isValid = false;
      }
      if (!this.registerForm.password) {
        this.registerErrors.password = 'Пароль обязателен';
        isValid = false;
      } else if (this.registerForm.password.length < 8) {
        this.registerErrors.password = 'Пароль должен содержать минимум 8 символов';
        isValid = false;
      } else if (!this.isPasswordValid) {
        this.registerErrors.password = 'Пароль слишком слабый. Используйте заглавные буквы, цифры и спецсимволы.';
        isValid = false;
      }
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.registerErrors.confirmPassword = 'Пароли не совпадают';
        isValid = false;
      }
      return isValid;
    },

    async handleLogin() {
      if (!this.validateLogin()) return;
      try {
        await login(this.loginForm);
        this.showToast('Вход выполнен успешно!', 'success');
        this.$router.push('/');
      } catch (err) {
        const msg = this.parseApiError(err);
        this.showToast(msg, 'error');
        this.authState.error = msg;
      }
    },

    async handleRegister() {
      if (!this.validateRegister()) return;
      try {
        await register({
          name: this.registerForm.name,
          phone: this.registerForm.phone,
          email: this.registerForm.email,
          password: this.registerForm.password
        });
        this.showToast('Регистрация прошла успешно!', 'success');
        this.$router.push('/');
      } catch (err) {
        const msg = this.parseApiError(err);
        this.showToast(msg, 'error');
        this.registerFormGeneralError = msg;
        if (err.response && Array.isArray(err.response.data)) {
          err.response.data.forEach(item => {
            const field = item.loc[item.loc.length - 1];
            if (field === 'name') this.registerErrors.name = item.msg;
            if (field === 'phone') this.registerErrors.phone = item.msg;
            if (field === 'email') this.registerErrors.email = item.msg;
            if (field === 'password') this.registerErrors.password = item.msg;
          });
        }
      }
    },

    // --- Forgot password methods ---
    openForgotModal() {
      this.forgotEmail = '';
      this.forgotError = null;
      this.showForgotModal = true;
    },
    closeForgotModal() {
      this.showForgotModal = false;
    },
    async requestPasswordReset() {
      if (!this.forgotEmail.trim()) {
        this.forgotError = 'Введите email.';
        return;
      }
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
      if (!emailRegex.test(this.forgotEmail)) {
        this.forgotError = 'Введите корректный email.';
        return;
      }

      this.forgotLoading = true;
      this.forgotError = null;
      try {
        // Замените на реальный сервис, если он существует
        // await authService.forgotPassword({ email: this.forgotEmail });
        // Временно имитируем запрос
        await new Promise(resolve => setTimeout(resolve, 1000));
        this.showToast('Ссылка для сброса пароля отправлена на указанный email.', 'success');
        this.closeForgotModal();
      } catch (err) {
        this.forgotError = this.parseApiError(err);
      } finally {
        this.forgotLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.error-text {
  color: #e53e3e;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  padding: 10px 14px;
  background: rgba(229, 62, 62, 0.08);
  border-radius: 12px;
  border-left: 3px solid #e53e3e;
}
.field-error {
  color: #e53e3e;
  font-size: 0.78rem;
  margin-top: 4px;
  display: block;
  animation: shake 0.3s ease;
}
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  padding: 14px 22px;
  border-radius: 14px;
  background: #323232;
  color: white;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  animation: toastIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.toast.success { background: linear-gradient(135deg, #2b7e3a, #3aa17e); }
.toast.error { background: linear-gradient(135deg, #c62828, #e53e3e); }
@keyframes toastIn {
  from { opacity: 0; transform: translateX(20px) scale(0.95); }
  to { opacity: 1; transform: translateX(0) scale(1); }
}

.split-grid .panel {
  animation: fadeInUp 0.5s ease backwards;
}
.split-grid .panel:nth-child(1) { animation-delay: 0.1s; }
.split-grid .panel:nth-child(2) { animation-delay: 0.2s; }
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.field-full {
  grid-column: 1 / -1;
}

.password-strength { margin-top: 8px; }
.strength-bar {
  height: 5px;
  width: 100%;
  background: #e0e0e0;
  border-radius: 999px;
  transition: all 0.3s ease;
  overflow: hidden;
}
.strength-bar.weak { background: linear-gradient(90deg, #e53e3e, #ff6b6b); width: 33%; }
.strength-bar.medium { background: linear-gradient(90deg, #f39c12, #f1c40f); width: 66%; }
.strength-bar.strong { background: linear-gradient(90deg, #2b7e3a, #3aa17e); width: 100%; }
.strength-text {
  font-size: 0.78rem;
  margin-top: 6px;
  display: block;
  font-weight: 600;
}
.strength-text.weak { color: #e53e3e; }
.strength-text.medium { color: #f39c12; }
.strength-text.strong { color: #2b7e3a; }
.password-requirements {
  list-style: none;
  padding: 0;
  margin: 8px 0 0;
  font-size: 0.78rem;
  color: #6d5f57;
}
.password-requirements li {
  margin: 5px 0;
  transition: all 0.2s ease;
  padding: 2px 0;
}
.password-requirements li.met {
  color: #2b7e3a;
  font-weight: 600;
}
.password-requirements li.met::before {
  content: "✓ ";
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.modal-container {
  background: var(--surface-strong);
  border-radius: 24px;
  width: 90%;
  max-width: 480px;
  box-shadow: var(--shadow);
  overflow: hidden;
  animation: modalSlideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes modalSlideIn {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--line);
}
.modal-title {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 800;
}
.modal-close {
  background: none;
  border: none;
  font-size: 1.6rem;
  cursor: pointer;
  color: var(--muted);
  line-height: 1;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}
.modal-close:hover {
  background: rgba(229, 62, 62, 0.08);
  color: #e53e3e;
  transform: rotate(90deg);
}
.modal-body { padding: 24px; }
.modal-description {
  margin: 0 0 16px;
  color: var(--muted);
}
.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--line);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>