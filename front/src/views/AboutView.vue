<template>
  <section class="page">
    <div class="hero-card">
      <div>
        <span class="badge">О клинике</span>
        <h1 class="hero-title">FastPig — современное ветеринарное пространство с человеческим подходом.</h1>
        <p class="hero-subtitle">
          Здесь отображаются контакты, врачи, часы работы и другая информация из базы данных.
        </p>
      </div>

      <article v-if="clinic" class="panel soft">
        <p class="mini-title">Контактная информация</p>
        <p class="muted">{{ clinic.address || 'Адрес не указан' }}</p>
        <p class="muted">{{ clinic.phone || 'Телефон не указан' }}</p>
        <p class="muted">{{ clinic.email || 'Email не указан' }}</p>
        <p class="mini-title">Часы работы</p>
        <p class="muted">{{ clinic.working_hours || 'Не указаны' }}</p>
        <p class="mini-title">О нас</p>
        <p class="muted">{{ clinic.about_text || 'Нет описания' }}</p>
      </article>
      <article v-else-if="isLoading" class="panel soft">
        <p>Загрузка информации о клинике…</p>
      </article>
      <p v-if="error" class="error-text">{{ error }}</p>
    </div>

    <section class="about-grid">
      <article v-for="fact in facts" :key="fact.title" class="tile">
        <h2 class="card-title">{{ fact.title }}</h2>
        <p class="muted">{{ fact.description }}</p>
      </article>
    </section>

    <section class="social-section">
      <h2 class="section-title">Мы в соцсетях</h2>
      <div class="social-links">
        <a href="https://www.instagram.com/ani1onn" class="social-link instagram">
          <span class="social-icon">📷</span> Instagram
        </a>
        <a href="https://web.telegram.org/ani1on" class="social-link telegram">
          <span class="social-icon">📨</span> Telegram
        </a>
        <a href="https://vk.com/v_vrrrrrrrrrrrrrrrrtoi" class="social-link vk">
          <span class="social-icon">🔵</span> VK
        </a>
      </div>
    </section>
  </section>
</template>

<script>
import clinicService from '@/services/clinicService';

export default {
  name: "AboutView",
  data() {
    return {
      clinic: null,
      isLoading: false,
      error: null,
      facts: [
        { title: "Цифровая карта пациента", description: "Каждый визит остаётся в едином кабинете." },
        { title: "Отдельные зоны", description: "Тихие зоны для крупных и маленьких питомцев." },
        { title: "Собственный магазин", description: "Каталог клиники с кормами, уходом и наборами для врачей." },
        { title: "Горячая линия FastPig", description: "Помощь с маршрутизацией и ответы на вопросы." },
      ],
    };
  },
  async created() {
    await this.fetchClinicInfo();
  },
  methods: {
    // Улучшенный парсинг ошибок API с обработкой сетевых ошибок и 5xx
    parseApiError(error) {
      // Ошибка сети (нет ответа от сервера)
      if (!error.response) {
        return 'Не удалось соединиться с сервером. Проверьте подключение к интернету.';
      }
      
      const status = error.response.status;
      
      // Ошибки сервера (5xx)
      if (status >= 500 && status <= 503) {
        return 'Сервер временно недоступен. Попробуйте позже.';
      }
      
      // Ошибка 404 - данные не найдены (не показываем как ошибку, просто нет данных)
      if (status === 404) {
        return null; // Возвращаем null, чтобы не показывать ошибку
      }
      
      // Остальные ошибки (400, 401, 403 и т.д.)
      const data = error.response.data;
      if (data) {
        if (Array.isArray(data) && data[0]?.loc) {
          const messages = data.map(err => {
            const field = err.loc[err.loc.length - 1];
            return `Поле "${field}": ${err.msg}`;
          });
          return messages.join('; ');
        }
        if (data.detail) {
          if (typeof data.detail === 'string') return data.detail;
          if (Array.isArray(data.detail)) return data.detail.map(d => d.msg).join('; ');
        }
        if (data.message) return data.message;
      }
      
      return 'Произошла ошибка. Попробуйте обновить страницу.';
    },

    async fetchClinicInfo() {
      this.isLoading = true;
      this.error = null;
      try {
        const resp = await clinicService.getAbout();
        this.clinic = resp.data;
      } catch (e) {
        const errorMessage = this.parseApiError(e);
        // Показываем ошибку только если它不是 null (для 404 не показываем)
        if (errorMessage) {
          this.error = errorMessage;
        } else {
          // При 404 просто оставляем clinic = null, без ошибки
          this.clinic = null;
        }
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.error-text { 
  color: #e53e3e;
  margin-top: 12px;
  padding: 12px;
  background: rgba(229, 62, 62, 0.1);
  border-radius: 12px;
}

.social-section {
  margin-top: 32px;
  text-align: center;
}
.social-links {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 12px;
  flex-wrap: wrap;
}
.social-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 12px 18px;
  border-radius: 999px;
  background: var(--surface-strong);
  border: 1px solid var(--line);
  color: var(--text);
  text-decoration: none;
  font-weight: 700;
  transition: background 0.2s, color 0.2s;
}
.social-link:hover {
  background: var(--text);
  color: #fff;
}
.social-icon {
  font-size: 1.2rem;
}
</style>