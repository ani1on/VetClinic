<template>
  <section class="page">
    <!-- Глобальный тост -->
    <div v-if="toastMessage" class="toast" :class="toastType">
      {{ toastMessage }}
    </div>

    <!-- Hero-блок -->
    <div class="hero-card">
      <div>
        <span class="badge">Ветеринарная платформа FastPig</span>
        <h1 class="hero-title">Здоровые питомцы, спокойные хозяева, одна цифровая клиника.</h1>
        <p class="hero-subtitle">
          FastPig объединяет запись на приём, ветеринарный каталог, избранное и
          профили питомцев в одном простом и тёплом веб-приложении.
        </p>
        <div class="hero-actions">
          <router-link class="button" to="/appointment">Записаться на приём</router-link>
          <router-link class="button-secondary" to="/catalog">Открыть каталог</router-link>
        </div>
      </div>

      <div class="hero-aside">
        <div class="panel">
          <p class="mini-title">Сегодня в клинике</p>
          <p class="muted">
            {{ todayStats.operations }} операций,
            {{ todayStats.onlineConfirmations }} онлайн-подтверждений и
            {{ todayStats.repeatOrders }} повторных заказа.
          </p>
        </div>
        <div class="panel soft success">
          <p class="mini-title">Быстрый маршрут</p>
          <p class="muted">Клиент может записаться за три шага и сразу увидеть врача.</p>
        </div>
        <div class="panel soft">
          <p class="mini-title">Основной сценарий</p>
          <p class="muted">Авторизация → выбор услуги → запись → управление профилем.</p>
        </div>
      </div>
    </div>

    <!-- Статистика -->
    <section class="stats-grid">
      <article class="stat-card">
        <p class="stat-value">24/7</p>
        <p class="stat-label">Экстренная поддержка для срочных случаев и ночных консультаций.</p>
      </article>
      <article class="stat-card">
        <p class="stat-value">{{ doctorsCount }}</p>
        <p class="stat-label">Врачей, диагностов и специалистов по уходу в одной команде.</p>
      </article>
      <article class="stat-card">
        <p class="stat-value">{{ averageRatingDisplay }}</p>
        <p class="stat-label">Средняя оценка клиентов за качество обслуживания и внимание.</p>
      </article>
      <article class="stat-card">
        <p class="stat-value">15м</p>
        <p class="stat-label">Среднее время ответа при онлайн-подтверждении записи.</p>
      </article>
    </section>

    <!-- Услуги с сервера -->
    <section class="page">
      <div class="section-heading">
        <div>
          <h2 class="section-title">Популярные направления</h2>
          <p class="section-copy">
            Главная страница показывает то, что владельцы делают чаще всего: выбирают услугу,
            покупают повседневные товары и хранят все данные питомцев рядом.
          </p>
        </div>
      </div>

      <div v-if="isServicesLoading" class="muted">Загрузка услуг…</div>
      <p v-if="servicesError" class="error-text">{{ servicesError }}</p>

      <div v-if="services.length" class="tile-grid">
        <article v-for="service in services" :key="service.id" class="tile">
          <div class="meta-row">
            <span class="chip">{{ service.category || 'Услуга' }}</span>
            <strong>{{ service.price }} BYN</strong>
          </div>
          <h3 class="card-title">{{ service.name }}</h3>
          <p class="muted">{{ service.description }}</p>
        </article>
      </div>
    </section>

    <!-- Новости и быстрые ссылки -->
    <section class="split-grid">
      <article class="panel">
        <div class="section-heading">
          <div>
            <h2 class="section-title">Последние новости</h2>
            <p class="section-copy">Свежие новости клиники.</p>
          </div>
        </div>
        <div v-if="isNewsLoading" class="muted">Загрузка новостей…</div>
        <p v-if="newsError" class="error-text">{{ newsError }}</p>
        <div v-if="news.length" class="list-column">
          <article v-for="item in news" :key="item.id" class="feed-card">
            <img v-if="item.image_url" :src="item.image_url" :alt="item.title" class="card-image" />
            <div class="meta-row">
              <strong>{{ item.title }}</strong>
              <span class="chip">{{ item.created_at?.slice(0,10) }}</span>
            </div>
            <p class="muted">{{ item.content }}</p>
          </article>
        </div>
      </article>

      <article class="panel">
        <p class="mini-title">Быстрые ссылки</p>
        <div class="hero-actions">
          <router-link class="button-secondary" to="/profile">Карточки питомцев</router-link>
          <router-link class="button-secondary" to="/favorits">Избранное</router-link>
          <router-link class="button-secondary" to="/about">О клинике</router-link>
        </div>
      </article>
    </section>

    <!-- Блок одобренных отзывов -->
    <section class="reviews-section">
      <div class="section-heading">
        <div>
          <h2 class="section-title">Отзывы наших клиентов</h2>
          <p class="section-copy">Что говорят о нас владельцы питомцев.</p>
        </div>
      </div>
      <div v-if="reviewsLoading" class="muted">Загрузка отзывов…</div>
      <p v-if="reviewsError" class="error-text">{{ reviewsError }}</p>
      <div v-if="approvedReviews.length" class="reviews-grid">
        <article v-for="review in approvedReviews" :key="review.id" class="review-card tile">
          <div class="review-header">
            <div class="review-rating">
              <span v-for="n in 5" :key="n" class="star" :class="{ filled: n <= review.rating }">★</span>
            </div>
            <span class="review-author">{{ review.user_name || 'Аноним' }}</span>
          </div>
          <p class="review-comment">{{ review.comment }}</p>
          <p class="review-date muted">{{ formatDate(review.created_at) }}</p>
        </article>
      </div>
      <p v-else-if="!reviewsLoading && !approvedReviews.length" class="muted">
        Пока нет отзывов. Будьте первыми!
      </p>
    </section>
  </section>
</template>

<script>
import serviceService from '@/services/serviceService';
import newsService from '@/services/newsService';
import reviewService from '@/services/reviewService';
import doctorService from '@/services/doctorService';

export default {
  name: "HomeView",
  data() {
    return {
      toastMessage: '',
      toastType: '',
      doctorsCount: 0,
      averageRating: 0,
      todayStats: {
        operations: 0,
        onlineConfirmations: 0,
        repeatOrders: 0
      },
      services: [],
      isServicesLoading: false,
      servicesError: null,
      news: [],
      isNewsLoading: false,
      newsError: null,
      approvedReviews: [],
      reviewsLoading: false,
      reviewsError: null,
    };
  },
  computed: {
    averageRatingDisplay() {
      if (this.averageRating === 0) return 'Нет оценок';
      return this.averageRating.toFixed(1);
    }
  },
  async created() {
    await Promise.all([
      this.fetchServices(),
      this.fetchNews(),
      this.fetchApprovedReviews(),
      this.fetchDoctorsCount(),
      this.fetchTodayStats()
    ]);
  },
  methods: {
    showToast(text, type = 'success') {
      this.toastMessage = text;
      this.toastType = type;
      setTimeout(() => {
        this.toastMessage = '';
      }, 3000);
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
          return data.map(err => `Поле "${err.loc[err.loc.length-1]}": ${err.msg}`).join('; ');
        }
        if (data.detail) {
          if (typeof data.detail === 'string') return data.detail;
          if (Array.isArray(data.detail)) return data.detail.map(d => d.msg).join('; ');
        }
        if (data.message) return data.message;
      }
      return 'Произошла ошибка. Попробуйте обновить страницу.';
    },
    async fetchServices() {
      this.isServicesLoading = true;
      this.servicesError = null;
      try {
        const resp = await serviceService.getServices();
        this.services = resp.data;
      } catch (e) {
        this.servicesError = this.parseApiError(e);
        this.showToast(this.servicesError, 'error');
      } finally {
        this.isServicesLoading = false;
      }
    },
    async fetchNews() {
      this.isNewsLoading = true;
      this.newsError = null;
      try {
        const resp = await newsService.getNews();
        this.news = resp.data.news || [];
      } catch (e) {
        this.newsError = this.parseApiError(e);
        this.showToast(this.newsError, 'error');
      } finally {
        this.isNewsLoading = false;
      }
    },
    async fetchApprovedReviews() {
      this.reviewsLoading = true;
      this.reviewsError = null;
      try {
        const resp = await reviewService.getReviews({ status: 'approved' });
        this.approvedReviews = resp.data.reviews || resp.data;
        // Вычисляем среднюю оценку на основе одобренных отзывов
        if (this.approvedReviews.length) {
          const sum = this.approvedReviews.reduce((acc, r) => acc + r.rating, 0);
          this.averageRating = sum / this.approvedReviews.length;
        } else {
          this.averageRating = 0;
        }
      } catch (e) {
        this.reviewsError = this.parseApiError(e);
      } finally {
        this.reviewsLoading = false;
      }
    },
    async fetchDoctorsCount() {
      try {
        const resp = await doctorService.getAll();
        this.doctorsCount = resp.data.length;
      } catch (e) {
        console.warn('Не удалось загрузить количество врачей', e);
        this.doctorsCount = 0;
      }
    },
    async fetchTodayStats() {
      this.todayStats = {
        operations: 8,
        onlineConfirmations: 19,
        repeatOrders: 34
      };
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleDateString('ru-RU');
    }
  }
};
</script>

<style scoped>
.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 16px;
}
.error-text {
  color: #e53e3e;
  margin-top: 0.5rem;
  padding: 10px 14px;
  background: rgba(229, 62, 62, 0.08);
  border-radius: 12px;
  border-left: 3px solid #e53e3e;
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
.toast.success {
  background: linear-gradient(135deg, #2b7e3a, #3aa17e);
}
.toast.error {
  background: linear-gradient(135deg, #c62828, #e53e3e);
}
@keyframes toastIn {
  from { opacity: 0; transform: translateX(20px) scale(0.95); }
  to { opacity: 1; transform: translateX(0) scale(1); }
}

.stat-card {
  animation: fadeInUp 0.5s ease backwards;
}
.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }
.stat-card:nth-child(4) { animation-delay: 0.4s; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.reviews-section {
  margin-top: 24px;
}
.reviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
.review-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}
.review-rating {
  display: flex;
  gap: 4px;
}
.star {
  color: #ddd;
  font-size: 1.2rem;
  transition: transform 0.2s ease;
}
.star.filled {
  color: #ffb800;
}
.review-card:hover .star.filled {
  transform: scale(1.2);
}
.review-author {
  font-weight: 600;
  color: var(--muted);
}
.review-comment {
  margin: 0;
  line-height: 1.5;
}
.review-date {
  font-size: 0.8rem;
  margin-top: 8px;
  color: var(--muted);
}
</style>