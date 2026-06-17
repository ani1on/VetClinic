<template>
  <section class="page">
    <div v-if="toastMessage" class="toast" :class="toastType">{{ toastMessage }}</div>

    <div class="section-heading">
      <div>
        <h1 class="section-title">Панель администратора</h1>
        <p class="section-copy">Центральная панель управления клиникой.</p>
      </div>
      <div class="chip-row">
        <span
          v-for="tab in tabs"
          :key="tab.key"
          class="chip"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </span>
      </div>
    </div>

    <!-- Dashboard -->
    <section v-if="activeTab === 'dashboard'" class="dashboard-section">
      <div v-if="metricsLoading" class="muted">Загрузка метрик…</div>
      <p v-if="metricsError" class="error-text">{{ metricsError }}</p>
      <div v-if="metrics.length" class="stats-grid">
        <article v-for="metric in metrics" :key="metric.label" class="stat-card">
          <p class="stat-value">{{ metric.value }}</p>
          <p class="stat-label">{{ metric.label }}</p>
        </article>
      </div>
      <div class="admin-grid">
        <article class="panel">
          <h2 class="section-title">Быстрые действия</h2>
          <div class="hero-actions">
            <button class="button-secondary" @click="activeTab='users'">Управление пользователями</button>
            <button class="button-secondary" @click="activeTab='services'">Услуги</button>
            <button class="button-secondary" @click="activeTab='products'">Товары</button>
            <button class="button-secondary" @click="activeTab='news'">Новости</button>
            <button class="button-secondary" @click="activeTab='clinic'">Информация о клинике</button>
          </div>
        </article>
      </div>
    </section>

    <!-- Users -->
    <section v-if="activeTab === 'users'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">Пользователи</h2>
        <div class="hero-actions">
          <button class="button-secondary" @click="refreshUsers" :disabled="usersLoading">Обновить</button>
        </div>
      </div>
      <div v-if="usersLoading" class="muted">Загрузка…</div>
      <p v-if="usersError" class="error-text">{{ usersError }}</p>
      <div v-if="users.length" class="list-column">
        <article v-for="user in users" :key="user.id" class="feed-card">
          <div class="meta-row">
            <strong>{{ user.name }}</strong>
            <span class="chip">{{ translateRole(user.role) }}</span>
          </div>
          <p class="muted">{{ user.phone }} {{ user.email }}</p>
          <p class="muted">Создан: {{ new Date(user.created_at).toLocaleDateString() }}</p>
          <div class="inline-actions">
            <select v-model="user._newRole" @change="changeUserRole(user.id, user._newRole)" class="role-select">
              <option value="client">Пользователь</option>
              <option value="admin">Администратор</option>
            </select>
            <button class="button" @click="deleteUser(user.id)">Удалить</button>
          </div>
        </article>
      </div>
      <p v-else-if="!usersLoading" class="muted">Пользователи не найдены.</p>
    </section>

    <!-- Doctors -->
    <section v-if="activeTab === 'doctors'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">Врачи</h2>
        <button class="button" @click="showDoctorForm = !showDoctorForm">
          {{ showDoctorForm ? 'Отмена' : 'Новый врач' }}
        </button>
      </div>
      <div v-if="showDoctorForm" class="panel soft">
        <div class="form-grid two">
          <label class="field"><span>ФИО</span><input v-model="doctorForm.full_name" /></label>
          <label class="field"><span>Пользователь</span>
            <select v-model="doctorForm.user_id">
              <option disabled value="">-- Выберите пользователя --</option>
              <option v-for="user in availableUsers" :key="user.id" :value="user.id">
                {{ user.name }} ({{ user.email || user.phone }})
              </option>
            </select>
          </label>
          <label class="field"><span>Специализация</span><input v-model="doctorForm.specialization" /></label>
          <label class="field"><span>URL фото</span><input v-model="doctorForm.photo_url" /></label>
        </div>
        <label class="field"><span>Описание</span><textarea v-model="doctorForm.description"></textarea></label>
        <div class="hero-actions">
          <button class="button" @click="saveDoctor" :disabled="doctorSaving">{{ doctorForm.id ? 'Обновить' : 'Создать' }}</button>
          <button class="button-secondary" @click="resetDoctorForm">Сбросить</button>
        </div>
        <p v-if="doctorFormError" class="error-text">{{ doctorFormError }}</p>
      </div>
      <div v-if="doctorsLoading" class="muted">Загрузка…</div>
      <p v-if="doctorsError" class="error-text">{{ doctorsError }}</p>
      <div v-if="doctors.length" class="list-column">
        <article v-for="doc in doctors" :key="doc.id" class="feed-card">
          <img v-if="doc.photo_url" :src="doc.photo_url" :alt="doc.full_name" class="admin-card-image" />
          <div class="meta-row">
            <strong>{{ doc.full_name }}</strong>
            <span class="chip">{{ doc.specialization || 'Общий' }}</span>
          </div>
          <p class="muted">{{ doc.description }}</p>
          <div class="inline-actions">
            <button class="button-secondary" @click="editDoctor(doc)">Редактировать</button>
            <button class="button" @click="archiveDoctor(doc.id)" :disabled="doctorSaving === doc.id">Архивировать</button>
          </div>
        </article>
      </div>
      <p v-else-if="!doctorsLoading" class="muted">Врачи не найдены.</p>
    </section>

    <!-- Services -->
    <section v-if="activeTab === 'services'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">Услуги</h2>
        <button class="button" @click="showServiceForm = !showServiceForm">{{ showServiceForm ? 'Отмена' : 'Новая услуга' }}</button>
      </div>
      <div v-if="showServiceForm" class="panel soft">
        <div class="form-grid two">
          <label class="field"><span>Название</span><input v-model="serviceForm.name" /></label>
          <label class="field"><span>Категория</span><input v-model="serviceForm.category" /></label>
          <label class="field"><span>Цена</span><input type="number" v-model="serviceForm.price" /></label>
          <label class="field"><span>Длительность (мин)</span><input type="number" v-model="serviceForm.duration_minutes" /></label>
        </div>
        <label class="field"><span>Описание</span><textarea v-model="serviceForm.description"></textarea></label>
        <div class="hero-actions">
          <button class="button" @click="saveService" :disabled="serviceSaving">{{ serviceForm.id ? 'Обновить' : 'Создать' }}</button>
          <button class="button-secondary" @click="resetServiceForm">Сбросить</button>
        </div>
        <p v-if="serviceError" class="error-text">{{ serviceError }}</p>
      </div>
      <div v-if="servicesLoading" class="muted">Загрузка…</div>
      <p v-if="servicesLoadError" class="error-text">{{ servicesLoadError }}</p>
      <div v-if="services.length" class="list-column">
        <article v-for="srv in services" :key="srv.id" class="feed-card">
          <div class="meta-row"><strong>{{ srv.name }}</strong><span class="chip">{{ srv.price }} BYN</span></div>
          <p class="muted">{{ srv.category }} · {{ srv.duration_minutes }} мин</p>
          <div class="inline-actions">
            <button class="button-secondary" @click="editService(srv)">Редактировать</button>
            <button class="button" @click="archiveService(srv.id)" :disabled="srv.id === serviceSaving">Архивировать</button>
          </div>
        </article>
      </div>
      <p v-else-if="!servicesLoading" class="muted">Услуги не найдены.</p>
    </section>

    <!-- Products -->
    <section v-if="activeTab === 'products'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">Товары</h2>
        <button class="button" @click="showProductForm = !showProductForm">{{ showProductForm ? 'Отмена' : 'Новый товар' }}</button>
      </div>
      <div v-if="showProductForm" class="panel soft">
        <div class="form-grid two">
          <label class="field"><span>Название</span><input v-model="productForm.name" /></label>
          <label class="field"><span>Категория</span><input v-model="productForm.category" /></label>
          <label class="field"><span>Цена</span><input type="number" v-model="productForm.price" /></label>
          <label class="field"><span>Количество</span><input type="number" v-model="productForm.stock_quantity" min="0" /></label>
          <label class="field"><span>URL изображения</span><input v-model="productForm.image_url" placeholder="https://..." /></label>
        </div>
        <label class="field"><span>Описание</span><textarea v-model="productForm.description"></textarea></label>
        <div class="hero-actions">
          <button class="button" @click="saveProduct" :disabled="productSaving">{{ productForm.id ? 'Обновить' : 'Создать' }}</button>
          <button class="button-secondary" @click="resetProductForm">Сбросить</button>
        </div>
        <p v-if="productError" class="error-text">{{ productError }}</p>
      </div>
      <div v-if="productsLoading" class="muted">Загрузка…</div>
      <p v-if="productsLoadError" class="error-text">{{ productsLoadError }}</p>
      <div v-if="products.length" class="list-column">
        <article v-for="prod in products" :key="prod.id" class="feed-card">
          <img v-if="prod.image_url" :src="prod.image_url" :alt="prod.name" class="admin-card-image" />
          <div class="meta-row"><strong>{{ prod.name }}</strong><span class="chip">{{ prod.price }} BYN</span></div>
          <p class="muted">Остаток: {{ prod.stock_quantity }} | {{ prod.is_available ? 'Активен' : 'В архиве' }}</p>
          <div class="inline-actions">
            <button class="button-secondary" @click="editProduct(prod)">Редактировать</button>
            <button class="button" @click="archiveProduct(prod.id)" :disabled="productSaving === prod.id">Архивировать</button>
          </div>
        </article>
      </div>
      <p v-else-if="!productsLoading" class="muted">Товары не найдены.</p>
    </section>

    <!-- News -->
    <section v-if="activeTab === 'news'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">Новости</h2>
        <button class="button" @click="showNewsForm = !showNewsForm">{{ showNewsForm ? 'Отмена' : 'Новая статья' }}</button>
      </div>
      <div v-if="showNewsForm" class="panel soft">
        <div class="form-grid two">
          <label class="field"><span>Заголовок</span><input v-model="newsForm.title" /></label>
          <label class="field"><span>Опубликовано</span>
            <select v-model="newsForm.is_published"><option :value="true">Да</option><option :value="false">Нет</option></select>
          </label>
        </div>
        <label class="field"><span>Содержание</span><textarea v-model="newsForm.content"></textarea></label>
        <label class="field"><span>URL изображения</span><input v-model="newsForm.image_url" /></label>
        <div class="hero-actions">
          <button class="button" @click="saveNews" :disabled="newsSaving">{{ newsForm.id ? 'Обновить' : 'Опубликовать' }}</button>
          <button class="button-secondary" @click="resetNewsForm">Сбросить</button>
        </div>
        <p v-if="newsError" class="error-text">{{ newsError }}</p>
      </div>
      <div v-if="newsLoading" class="muted">Загрузка…</div>
      <p v-if="newsLoadError" class="error-text">{{ newsLoadError }}</p>
      <div v-if="newsList.length" class="list-column">
        <article v-for="item in newsList" :key="item.id" class="feed-card">
          <img v-if="item.image_url" :src="item.image_url" :alt="item.title" class="admin-card-image" />
          <div class="meta-row"><strong>{{ item.title }}</strong><span class="chip">{{ item.is_published ? 'Опубликовано' : 'Черновик' }}</span></div>
          <p class="muted">{{ item.content?.slice(0, 100) }}…</p>
          <div class="inline-actions">
            <button class="button-secondary" @click="editNews(item)">Редактировать</button>
            <button class="button" @click="deleteNews(item.id)" :disabled="newsSaving === item.id">Удалить</button>
          </div>
        </article>
      </div>
      <p v-else-if="!newsLoading" class="muted">Новости не найдены.</p>
    </section>

    <!-- Reviews -->
    <section v-if="activeTab === 'reviews'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">Модерация отзывов</h2>
        <div class="hero-actions">
          <select v-model="reviewsFilterStatus" @change="fetchReviews" class="role-select">
            <option value="">Все статусы</option>
            <option value="pending">На модерации</option>
            <option value="approved">Одобренные</option>
            <option value="rejected">Отклонённые</option>
          </select>
          <button class="button-secondary" @click="fetchReviews" :disabled="reviewsLoading">Обновить</button>
        </div>
      </div>
      <div v-if="reviewsLoading" class="muted">Загрузка…</div>
      <p v-if="reviewsLoadError" class="error-text">{{ reviewsLoadError }}</p>
      <div v-if="reviews.length" class="list-column">
        <article v-for="rev in reviews" :key="rev.id" class="feed-card">
          <div class="meta-row">
            <strong>{{ rev.user_name || 'Пользователь #' + rev.user_id }}</strong>
            <span class="chip">{{ translateStatus(rev.status) }}</span>
          </div>
          <div class="meta-row">
            <span>Оценка {{ rev.rating }}/5</span>
            <span class="muted">{{ new Date(rev.created_at).toLocaleString() }}</span>
          </div>
          <p class="muted">{{ rev.comment }}</p>
          <div class="inline-actions">
            <button v-if="rev.status !== 'approved'" class="button-secondary" @click="moderateReview(rev.id, 'approved')">Одобрить</button>
            <button v-if="rev.status !== 'rejected'" class="button" @click="moderateReview(rev.id, 'rejected')">Отклонить</button>
          </div>
        </article>
      </div>
      <p v-else-if="!reviewsLoading" class="muted">Нет отзывов для отображения.</p>
    </section>

    <!-- Appointments -->
    <section v-if="activeTab === 'appointments'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">Все записи</h2>
      </div>
      <div v-if="appointmentsLoading" class="muted">Загрузка…</div>
      <p v-if="appointmentsLoadError" class="error-text">{{ appointmentsLoadError }}</p>
      <div v-if="appointments.length && !appointmentsLoading" class="list-column">
        <article v-for="appt in appointments" :key="appt.id" class="feed-card appt-card">
          <div class="appt-header">
            <div class="appt-title"><span class="appt-icon">🐾</span><strong>{{ getApptPetName(appt.pet_id) }} – {{ getApptServiceName(appt.service_id) }}</strong></div>
            <span class="chip status-chip" :class="'status-' + appt.status">{{ translateApptStatus(appt.status) }}</span>
          </div>
          <div class="appt-details">
            <div class="appt-detail"><span class="label">📅 Дата</span><span>{{ appt.appointment_date }} в {{ appt.appointment_time }}</span></div>
            <div class="appt-detail"><span class="label">👤 Пользователь</span><span>#{{ appt.user_id }}</span></div>
            <div class="appt-detail"><span class="label">🩺 Врач</span><span>{{ getApptDoctorName(appt.doctor_id) }}</span></div>
          </div>
          <div class="appt-actions">
            <select v-model="appt._newStatus" class="status-select" @change="changeApptStatus(appt.id, appt._newStatus)">
              <option v-if="!appt._newStatus" disabled value="">Изменить статус...</option>
              <option value="pending">🕒 Ожидает</option>
              <option value="confirmed">✅ Подтверждено</option>
              <option value="completed">✔️ Завершено</option>
              <option value="paid">💰 Оплачено</option>
              <option value="canceled">❌ Отменено</option>
            </select>
          </div>
        </article>
      </div>
      <p v-else-if="!appointmentsLoading" class="muted">Нет записей.</p>
    </section>

    <!-- Clinic Info -->
    <section v-if="activeTab === 'clinic'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">Информация о клинике</h2>
      </div>
      <div v-if="clinicLoading" class="muted">Загрузка информации…</div>
      <p v-if="clinicError" class="error-text">{{ clinicError }}</p>
      <div v-if="clinicInfo" class="panel soft">
        <div class="form-grid two">
          <label class="field"><span>Название</span><input v-model="clinicInfo.name" /></label>
          <label class="field"><span>Адрес</span><input v-model="clinicInfo.address" /></label>
          <label class="field"><span>Телефон</span><input v-model="clinicInfo.phone" /></label>
          <label class="field"><span>Email</span><input v-model="clinicInfo.email" /></label>
        </div>
        <label class="field"><span>Часы работы</span><textarea v-model="clinicInfo.working_hours"></textarea></label>
        <label class="field"><span>Социальные сети</span><textarea v-model="clinicInfo.social_links"></textarea></label>
        <label class="field"><span>Лицензии</span><textarea v-model="clinicInfo.licenses"></textarea></label>
        <label class="field"><span>О нас</span><textarea v-model="clinicInfo.about_text"></textarea></label>
        <div class="hero-actions">
          <button class="button" @click="saveClinicInfo" :disabled="clinicSaving">Сохранить</button>
        </div>
        <p v-if="clinicSaveError" class="error-text">{{ clinicSaveError }}</p>
      </div>
      <p v-else-if="!clinicLoading" class="muted">Информация о клинике не загружена. Нажмите <strong>Сохранить</strong> для создания.</p>
    </section>
  </section>
</template>

<script>
import adminService from '@/services/adminService';
import userService from '@/services/userService';
import doctorService from '@/services/doctorService';
import serviceService from '@/services/serviceService';
import productService from '@/services/productService';
import newsService from '@/services/newsService';
import reviewService from '@/services/reviewService';
import appointmentService from '@/services/appointmentService';
import clinicService from '@/services/clinicService';
import petService from '@/services/petService';

export default {
  name: "AdminView",
  data() {
    return {
      reviewsFilterStatus: '',
      toastMessage: '',
      toastType: '',
      activeTab: 'dashboard',
      tabs: [
        { key: 'dashboard', label: 'Dashboard' },
        { key: 'users', label: 'Users' },
        { key: 'doctors', label: 'Doctors' },
        { key: 'services', label: 'Services' },
        { key: 'products', label: 'Products' },
        { key: 'news', label: 'News' },
        { key: 'reviews', label: 'Reviews' },
        { key: 'appointments', label: 'Appointments' },
        { key: 'clinic', label: 'Clinic' },
      ],
      // Dashboard
      metrics: [],
      metricsLoading: false,
      metricsError: null,
      // Users
      users: [],
      usersLoading: false,
      usersError: null,
      // Doctors
      doctors: [],
      doctorsLoading: false,
      doctorsError: null,
      showDoctorForm: false,
      doctorForm: this.emptyDoctorForm(),
      doctorSaving: false,
      doctorFormError: null,
      availableUsers: [],
      // Services
      services: [],
      servicesLoading: false,
      servicesLoadError: null,
      showServiceForm: false,
      serviceForm: this.emptyServiceForm(),
      serviceSaving: false,
      serviceError: null,
      // Products
      products: [],
      productsLoading: false,
      productsLoadError: null,
      showProductForm: false,
      productForm: this.emptyProductForm(),
      productSaving: false,
      productError: null,
      // News
      newsList: [],
      newsLoading: false,
      newsLoadError: null,
      showNewsForm: false,
      newsForm: this.emptyNewsForm(),
      newsSaving: false,
      newsError: null,
      // Reviews
      reviews: [],
      reviewsLoading: false,
      reviewsLoadError: null,
      // Appointments
      appointments: [],
      appointmentsLoading: false,
      appointmentsLoadError: null,
      allPets: [],
      allServices: [],
      allDoctors: [],
      // Clinic
      clinicInfo: null,
      clinicLoading: false,
      clinicError: null,
      clinicSaving: false,
      clinicSaveError: null,
    };
  },
  watch: {
    activeTab(newTab) { this.loadTabData(newTab); }
  },
  created() {
    this.loadDashboardMetrics();
    this.loadTabData(this.activeTab);
    this.fetchAvailableUsers();
    this.loadReferenceData();
  },
  methods: {
    showToast(text, type = 'success') {
      this.toastMessage = text;
      this.toastType = type;
      setTimeout(() => { this.toastMessage = ''; }, 3000);
    },

    // Улучшенная обработка ошибок API с поддержкой сетевых ошибок и 5xx
    parseApiError(err) {
      // Ошибка сети (нет ответа от сервера)
      if (!err.response) {
        return 'Не удалось соединиться с сервером. Проверьте подключение к интернету.';
      }
      const status = err.response.status;
      // Ошибки сервера (5xx)
      if (status >= 500 && status <= 503) {
        return 'Сервер временно недоступен. Попробуйте позже.';
      }
      // Остальные ошибки (4xx и т.д.)
      const data = err.response.data;
      if (data) {
        if (Array.isArray(data) && data[0]?.loc) {
          return data.map(e => {
            const field = e.loc[e.loc.length - 1];
            let msg = e.msg;
            if (e.type === 'int_type' && field === 'user_id') msg = 'должен быть выбран';
            return `Поле "${field}": ${msg}`;
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

    translateRole(role) {
      return role === 'client' ? 'Пользователь' : (role === 'admin' ? 'Администратор' : role);
    },
    translateStatus(status) {
      const map = { pending: 'На модерации', approved: 'Одобрен', rejected: 'Отклонён' };
      return map[status] || status;
    },
    translateApptStatus(status) {
      const map = { pending: 'Ожидает', confirmed: 'Подтверждено', completed: 'Завершено', paid: 'Оплачено', canceled: 'Отменено' };
      return map[status] || status;
    },
    // --- Справочные данные ---
    async loadReferenceData() {
      try {
        const [petsRes, servicesRes, doctorsRes] = await Promise.all([
          petService.getAllPets(),
          serviceService.getServices(),
          doctorService.getAll()
        ]);
        this.allPets = petsRes.data || [];
        this.allServices = servicesRes.data || [];
        this.allDoctors = doctorsRes.data || [];
      } catch (e) { console.warn(e); }
    },
    getApptPetName(petId) {
      const pet = this.allPets.find(p => p.id === petId);
      return pet ? pet.name : `Питомец #${petId}`;
    },
    getApptServiceName(serviceId) {
      const srv = this.allServices.find(s => s.id === serviceId);
      return srv ? srv.name : `Услуга #${serviceId}`;
    },
    getApptDoctorName(doctorId) {
      if (!doctorId) return 'Любой врач';
      const doc = this.allDoctors.find(d => d.id === doctorId);
      return doc ? doc.full_name : `Врач #${doctorId}`;
    },
    // --- Dashboard ---
    async loadDashboardMetrics() {
      this.metricsLoading = true;
      try {
        const resp = await adminService.getDashboard();
        const m = resp.data;
        this.metrics = [
          { value: m.total_appointments, label: 'Всего записей' },
          { value: m.appointments_this_week, label: 'За эту неделю' },
          { value: m.pending_appointments, label: 'Ожидают' },
          { value: m.total_users, label: 'Пользователей' },
          { value: m.new_users_this_week, label: 'Новых на этой неделе' },
          { value: m.total_products, label: 'Товаров' },
          { value: m.low_stock_products, label: 'Низкий остаток' },
          { value: m.pending_reviews, label: 'Отзывов на модерации' },
        ];
      } catch (e) {
        this.metricsError = 'Не удалось загрузить панель управления';
        this.showToast(this.metricsError, 'error');
      } finally {
        this.metricsLoading = false;
      }
    },
    // --- Переключение вкладок ---
    loadTabData(tab) {
      switch (tab) {
        case 'users': return this.fetchUsers();
        case 'doctors': this.fetchAvailableUsers(); return this.fetchDoctors();
        case 'services': return this.fetchServices();
        case 'products': return this.fetchProducts();
        case 'news': return this.fetchNews();
        case 'reviews': return this.fetchReviews();
        case 'appointments': return this.fetchAllAppointments();
        case 'clinic': return this.fetchClinicInfo();
        default: break;
      }
    },
    // --- Users ---
    async fetchUsers() {
      this.usersLoading = true;
      this.usersError = null;
      try {
        const resp = await userService.listUsers();
        const usersData = resp.data.users || resp.data;
        this.users = usersData.map(u => ({ ...u, _newRole: u.role }));
      } catch (e) {
        this.usersError = this.parseApiError(e);
        this.showToast(this.usersError, 'error');
      } finally {
        this.usersLoading = false;
      }
    },
    refreshUsers() { return this.fetchUsers(); },
    async changeUserRole(userId, newRole) {
      try {
        await userService.updateUserRole(userId, { role: newRole });
        await this.fetchUsers();
        this.showToast('Роль пользователя изменена', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
        this.fetchUsers();
      }
    },
    async deleteUser(userId) {
      try {
        await userService.deleteUser(userId);
        await this.fetchUsers();
        this.showToast('Пользователь удалён', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },
    // --- Doctors ---
    emptyDoctorForm() {
      return { id: null, user_id: '', full_name: '', specialization: '', description: '', photo_url: '', is_active: true };
    },
    async fetchAvailableUsers() {
      try {
        const resp = await userService.listUsers();
        this.availableUsers = resp.data.users || resp.data;
      } catch (e) { console.error(e); }
    },
    async fetchDoctors() {
      this.doctorsLoading = true;
      this.doctorsError = null;
      try {
        const resp = await doctorService.getAll();
        this.doctors = resp.data;
      } catch (e) {
        this.doctorsError = this.parseApiError(e);
        this.showToast(this.doctorsError, 'error');
      } finally {
        this.doctorsLoading = false;
      }
    },
    editDoctor(doc) {
      this.doctorForm = { ...doc, user_id: doc.user_id || '' };
      this.showDoctorForm = true;
    },
    resetDoctorForm() {
      this.doctorForm = this.emptyDoctorForm();
      this.doctorFormError = null;
      this.showDoctorForm = false;
    },
    async saveDoctor() {
      this.doctorFormError = null;
      if (!this.doctorForm.full_name.trim()) {
        this.doctorFormError = 'ФИО обязательно.';
        return;
      }
      if (!this.doctorForm.user_id) {
        this.doctorFormError = 'Выберите пользователя.';
        return;
      }
      this.doctorSaving = true;
      try {
        const payload = { ...this.doctorForm, user_id: parseInt(this.doctorForm.user_id) };
        if (this.doctorForm.id) {
          await doctorService.updateDoctor(this.doctorForm.id, payload);
        } else {
          await doctorService.createDoctor(payload);
        }
        this.resetDoctorForm();
        await this.fetchDoctors();
        await this.loadReferenceData();
        this.showToast('Врач сохранён', 'success');
      } catch (e) {
        this.doctorFormError = this.parseApiError(e);
        this.showToast(this.doctorFormError, 'error');
      } finally {
        this.doctorSaving = false;
      }
    },
    async archiveDoctor(id) {
      if (!confirm('Архивировать врача?')) return;
      try {
        await doctorService.deleteDoctor(id);
        await this.fetchDoctors();
        await this.loadReferenceData();
        this.showToast('Врач архивирован', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },
    // --- Services ---
    emptyServiceForm() {
      return { id: null, name: '', description: '', price: '', duration_minutes: 30, category: '' };
    },
    async fetchServices() {
      this.servicesLoading = true;
      this.servicesLoadError = null;
      try {
        const resp = await serviceService.getServices();
        this.services = resp.data;
      } catch (e) {
        this.servicesLoadError = this.parseApiError(e);
        this.showToast(this.servicesLoadError, 'error');
      } finally {
        this.servicesLoading = false;
      }
    },
    editService(srv) {
      this.serviceForm = { ...srv };
      this.showServiceForm = true;
    },
    resetServiceForm() {
      this.serviceForm = this.emptyServiceForm();
      this.serviceError = null;
      this.showServiceForm = false;
    },
    async saveService() {
      this.serviceError = null;
      if (!this.serviceForm.name.trim()) {
        this.serviceError = 'Название обязательно.';
        return;
      }
      this.serviceSaving = true;
      try {
        const payload = { ...this.serviceForm, price: parseFloat(this.serviceForm.price), duration_minutes: parseInt(this.serviceForm.duration_minutes) };
        if (this.serviceForm.id) {
          await serviceService.updateService(this.serviceForm.id, payload);
        } else {
          await serviceService.createService(payload);
        }
        this.resetServiceForm();
        await this.fetchServices();
        await this.loadReferenceData();
        this.showToast('Услуга сохранена', 'success');
      } catch (e) {
        this.serviceError = this.parseApiError(e);
        this.showToast(this.serviceError, 'error');
      } finally {
        this.serviceSaving = false;
      }
    },
    async archiveService(id) {
      if (!confirm('Архивировать услугу?')) return;
      try {
        await serviceService.deleteService(id);
        await this.fetchServices();
        await this.loadReferenceData();
        this.showToast('Услуга архивирована', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },
    // --- Products ---
    emptyProductForm() {
      return { id: null, name: '', description: '', price: '', stock_quantity: 0, category: '', image_url: '' };
    },
    async fetchProducts() {
      this.productsLoading = true;
      this.productsLoadError = null;
      try {
        const resp = await productService.getProducts();
        this.products = resp.data.products || resp.data;
      } catch (e) {
        this.productsLoadError = this.parseApiError(e);
        this.showToast(this.productsLoadError, 'error');
      } finally {
        this.productsLoading = false;
      }
    },
    editProduct(prod) {
      this.productForm = { ...prod };
      this.showProductForm = true;
    },
    resetProductForm() {
      this.productForm = this.emptyProductForm();
      this.productError = null;
      this.showProductForm = false;
    },  
    async saveProduct() {
      this.productError = null;
      if (!this.productForm.name.trim()) {
        this.productError = 'Название обязательно.';
        return;
      }
    
      let quantity = parseInt(this.productForm.stock_quantity, 10);
      if (isNaN(quantity)) quantity = 0;
      if (quantity < 0) quantity = 0;
      this.productForm.stock_quantity = quantity;
    
      this.productSaving = true;
      try {
        const payload = {
          ...this.productForm,
          price: parseFloat(this.productForm.price),
          stock_quantity: quantity,
          is_available: true
        };
        if (this.productForm.id) {
          await productService.updateProduct(this.productForm.id, payload);
        } else {
          await productService.createProduct(payload);
        }
        this.resetProductForm();
        await this.fetchProducts();
        this.showToast('Товар сохранён', 'success');
      } catch (e) {
        this.productError = this.parseApiError(e);
        this.showToast(this.productError, 'error');
      } finally {
        this.productSaving = false;
      }
    },
    async archiveProduct(id) {
      if (!confirm('Архивировать товар?')) return;
      try {
        await productService.deleteProduct(id);
        await this.fetchProducts();
        this.showToast('Товар архивирован', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },
    // --- News ---
    emptyNewsForm() {
      return { id: null, title: '', content: '', image_url: '', is_published: true };
    },
    async fetchNews() {
      this.newsLoading = true;
      this.newsLoadError = null;
      try {
        const resp = await newsService.getNews({ published_only: false });
        this.newsList = resp.data.news || resp.data;
      } catch (e) {
        this.newsLoadError = this.parseApiError(e);
        this.showToast(this.newsLoadError, 'error');
      } finally {
        this.newsLoading = false;
      }
    },
    editNews(item) {
      this.newsForm = { ...item };
      this.showNewsForm = true;
    },
    resetNewsForm() {
      this.newsForm = this.emptyNewsForm();
      this.newsError = null;
      this.showNewsForm = false;
    },
    async saveNews() {
      this.newsError = null;
      if (!this.newsForm.title.trim()) {
        this.newsError = 'Заголовок обязателен.';
        return;
      }
      this.newsSaving = true;
      try {
        if (this.newsForm.id) {
          await newsService.updateNews(this.newsForm.id, this.newsForm);
        } else {
          await newsService.createNews(this.newsForm);
        }
        this.resetNewsForm();
        await this.fetchNews();
        this.showToast('Новость сохранена', 'success');
      } catch (e) {
        this.newsError = this.parseApiError(e);
        this.showToast(this.newsError, 'error');
      } finally {
        this.newsSaving = false;
      }
    },
    async deleteNews(id) {
      if (!confirm('Удалить новость?')) return;
      try {
        await newsService.deleteNews(id);
        await this.fetchNews();
        this.showToast('Новость удалена', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },
    // --- Reviews ---
    async fetchReviews() {
      this.reviewsLoading = true;
      this.reviewsLoadError = null;
      try {
        const params = {};
        if (this.reviewsFilterStatus) params.status = this.reviewsFilterStatus;
        const resp = await reviewService.getReviews(params);
        this.reviews = resp.data.reviews || resp.data;
      } catch (e) {
        this.reviewsLoadError = this.parseApiError(e);
        this.showToast(this.reviewsLoadError, 'error');
      } finally {
        this.reviewsLoading = false;
      }
    },
    async moderateReview(id, status) {
      try {
        await reviewService.moderateReview(id, status);
        await this.fetchReviews();
        this.showToast(`Отзыв ${status === 'approved' ? 'одобрен' : 'отклонён'}`, 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },
    // --- Appointments ---
    async fetchAllAppointments() {
      this.appointmentsLoading = true;
      this.appointmentsLoadError = null;
      try {
        const resp = await appointmentService.getAllAppointments();
        this.appointments = resp.data.appointments || resp.data;
      } catch (e) {
        this.appointmentsLoadError = this.parseApiError(e);
        this.showToast(this.appointmentsLoadError, 'error');
      } finally {
        this.appointmentsLoading = false;
      }
    },
    async changeApptStatus(id, status) {
      if (!status) return;
      try {
        await appointmentService.updateStatus(id, status);
        await this.fetchAllAppointments();
        this.showToast('Статус записи изменён', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },
    // --- Clinic ---
    async fetchClinicInfo() {
      this.clinicLoading = true;
      this.clinicError = null;
      try {
        const resp = await clinicService.getAbout();
        this.clinicInfo = resp.data;
      } catch (e) {
        if (e.response && e.response.status === 404) {
          this.clinicInfo = { id: null, name: '', address: '', phone: '', email: '', working_hours: '', social_links: '', licenses: '', about_text: '' };
        } else {
          this.clinicError = this.parseApiError(e);
          this.showToast(this.clinicError, 'error');
        }
      } finally {
        this.clinicLoading = false;
      }
    },
    async saveClinicInfo() {
      this.clinicSaving = true;
      this.clinicSaveError = null;
      try {
        await clinicService.updateAbout(this.clinicInfo);
        this.showToast('Информация о клинике сохранена', 'success');
      } catch (e) {
        this.clinicSaveError = this.parseApiError(e);
        this.showToast(this.clinicSaveError, 'error');
      } finally {
        this.clinicSaving = false;
      }
    },
  }
};
</script>

<style scoped>
.admin-card-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 16px;
}
.chip.active { background: var(--primary); color: #fff; }
.error-text { color: #e53e3e; margin: 0.5rem 0; }
.list-section { margin-top: 12px; }
.appt-card { padding: 20px; border-radius: var(--radius-lg); }
.appt-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.appt-title { display: flex; align-items: center; gap: 8px; font-size: 1.1rem; }
.appt-icon { font-size: 1.3rem; }
.status-chip { text-transform: capitalize; font-weight: 700; padding: 4px 12px; border-radius: 999px; font-size: 0.85rem; }
.status-pending { background: #fff3cd; color: #856404; }
.status-confirmed { background: #d1ecf1; color: #0c5460; }
.status-completed { background: #d4edda; color: #155724; }
.status-paid { background: #c3e6cb; color: #0b2e13; }
.status-canceled { background: #f8d7da; color: #721c24; }
.appt-details { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 14px; }
.appt-detail { display: flex; align-items: center; gap: 6px; font-size: 0.95rem; }
.appt-detail .label { color: var(--muted); font-weight: 600; font-size: 0.85rem; }
.appt-actions { display: flex; justify-content: flex-end; }
.toast {
  position: fixed; top: 20px; right: 20px; z-index: 1000; padding: 12px 20px; border-radius: 12px;
  background: #323232; color: white; font-weight: 500; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  animation: fadeIn 0.3s ease;
}
.toast.success { background: #2b7e3a; }
.toast.error { background: #c62828; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.role-select {
  padding: 6px 10px; border-radius: 20px; border: 1px solid var(--line); background: white;
}
/* Адаптивные вкладки для мобильных устройств */
@media (max-width: 768px) {
  .chip-row {
    overflow-x: auto;
    white-space: nowrap;
    flex-wrap: nowrap;
    padding-bottom: 8px;
    scrollbar-width: thin;
  }
  .chip-row::-webkit-scrollbar {
    height: 4px;
  }
  .chip-row::-webkit-scrollbar-track {
    background: var(--line);
    border-radius: 4px;
  }
  .chip-row::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 4px;
  }
  .chip {
    display: inline-flex;
    flex-shrink: 0;
  }
}
</style>