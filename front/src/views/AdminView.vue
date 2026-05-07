<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Admin dashboard</h1>
        <p class="section-copy">Central management panel for clinic operations.</p>
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
      <div v-if="metricsLoading" class="muted">Loading metrics…</div>
      <p v-if="metricsError" class="error-text">{{ metricsError }}</p>
      <div v-if="metrics.length" class="stats-grid">
        <article v-for="metric in metrics" :key="metric.label" class="stat-card">
          <p class="stat-value">{{ metric.value }}</p>
          <p class="stat-label">{{ metric.label }}</p>
        </article>
      </div>
      <!-- Quick actions -->
      <div class="admin-grid">
        <article class="panel">
          <h2 class="section-title">Quick actions</h2>
          <div class="hero-actions">
            <button class="button-secondary" @click="activeTab='users'">Manage users</button>
            <button class="button-secondary" @click="activeTab='services'">Services</button>
            <button class="button-secondary" @click="activeTab='products'">Products</button>
            <button class="button-secondary" @click="activeTab='news'">News</button>
            <button class="button-secondary" @click="activeTab='clinic'">Clinic Info</button>
          </div>
        </article>
      </div>
    </section>

    <!-- Users -->
    <section v-if="activeTab === 'users'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">Users</h2>
        <div class="hero-actions">
          <button class="button-secondary" @click="refreshUsers" :disabled="usersLoading">
            Refresh
          </button>
        </div>
      </div>
      <div v-if="usersLoading" class="muted">Loading…</div>
      <p v-if="usersError" class="error-text">{{ usersError }}</p>
      <div v-if="users.length" class="list-column">
        <article v-for="user in users" :key="user.id" class="feed-card">
          <div class="meta-row">
            <strong>{{ user.name }}</strong>
            <span class="chip">{{ user.role }}</span>
          </div>
          <p class="muted">{{ user.phone }} {{ user.email }}</p>
          <p class="muted">Created: {{ new Date(user.created_at).toLocaleDateString() }}</p>
        </article>
      </div>
      <p v-else-if="!usersLoading" class="muted">No users found.</p>
    </section>

    <!-- Doctors (CRUD) -->
    <section v-if="activeTab === 'doctors'" class="list-section">
      <!-- остальная часть Doctors без изменений -->
      <div class="section-heading">
        <h2 class="section-title">Doctors</h2>
        <button class="button" @click="showDoctorForm = !showDoctorForm">
          {{ showDoctorForm ? 'Cancel' : 'New doctor' }}
        </button>
      </div>
      <!-- Форма -->
      <div v-if="showDoctorForm" class="panel soft">
        <div class="form-grid two">
          <label class="field">
            <span>Full name</span>
            <input v-model="doctorForm.full_name" />
          </label>
          <label class="field">
            <span>User</span>
            <select v-model="doctorForm.user_id">
              <option disabled value="">Select user</option>
              <option v-for="user in availableUsers" :key="user.id" :value="user.id">
                {{ user.name }} ({{ user.email || user.phone }})
              </option>
            </select>
          </label>
          <label class="field">
            <span>Specialization</span>
            <input v-model="doctorForm.specialization" />
          </label>
          <label class="field">
            <span>Photo URL</span>
            <input v-model="doctorForm.photo_url" />
          </label>
        </div>
        <label class="field">
          <span>Description</span>
          <textarea v-model="doctorForm.description"></textarea>
        </label>
        <div class="hero-actions">
          <button class="button" @click="saveDoctor" :disabled="doctorSaving">
            {{ doctorForm.id ? 'Update' : 'Create' }}
          </button>
          <button class="button-secondary" @click="resetDoctorForm">Reset</button>
        </div>
        <p v-if="doctorFormError" class="error-text">{{ doctorFormError }}</p>
      </div>
      <!-- Список -->
      <div v-if="doctorsLoading" class="muted">Loading…</div>
      <p v-if="doctorsError" class="error-text">{{ doctorsError }}</p>
      <div v-if="doctors.length" class="list-column">
        <article v-for="doc in doctors" :key="doc.id" class="feed-card">
          <div class="meta-row">
            <strong>{{ doc.full_name }}</strong>
            <span class="chip">{{ doc.specialization || 'General' }}</span>
          </div>
          <p class="muted">{{ doc.description }}</p>
          <div class="inline-actions">
            <button class="button-secondary" @click="editDoctor(doc)">Edit</button>
            <button class="button" @click="archiveDoctor(doc.id)" :disabled="doctorSaving === doc.id">
              Archive
            </button>
          </div>
        </article>
      </div>
      <p v-else-if="!doctorsLoading" class="muted">No doctors.</p>
    </section>

    <!-- Services (CRUD) -->
    <section v-if="activeTab === 'services'" class="list-section">
      <!-- Services как раньше -->
      <div class="section-heading">
        <h2 class="section-title">Services</h2>
        <button class="button" @click="showServiceForm = !showServiceForm">
          {{ showServiceForm ? 'Cancel' : 'New service' }}
        </button>
      </div>
      <div v-if="showServiceForm" class="panel soft">
        <div class="form-grid two">
          <label class="field"><span>Name</span><input v-model="serviceForm.name" /></label>
          <label class="field"><span>Category</span><input v-model="serviceForm.category" /></label>
          <label class="field"><span>Price</span><input type="number" v-model="serviceForm.price" /></label>
          <label class="field"><span>Duration (min)</span><input type="number" v-model="serviceForm.duration_minutes" /></label>
        </div>
        <label class="field"><span>Description</span><textarea v-model="serviceForm.description"></textarea></label>
        <div class="hero-actions">
          <button class="button" @click="saveService" :disabled="serviceSaving">
            {{ serviceForm.id ? 'Update' : 'Create' }}
          </button>
          <button class="button-secondary" @click="resetServiceForm">Reset</button>
        </div>
        <p v-if="serviceError" class="error-text">{{ serviceError }}</p>
      </div>
      <div v-if="servicesLoading" class="muted">Loading…</div>
      <p v-if="servicesLoadError" class="error-text">{{ servicesLoadError }}</p>
      <div v-if="services.length" class="list-column">
        <article v-for="srv in services" :key="srv.id" class="feed-card">
          <div class="meta-row">
            <strong>{{ srv.name }}</strong>
            <span class="chip">{{ srv.price }} BYN</span>
          </div>
          <p class="muted">{{ srv.category }} · {{ srv.duration_minutes }} min</p>
          <div class="inline-actions">
            <button class="button-secondary" @click="editService(srv)">Edit</button>
            <button class="button" @click="archiveService(srv.id)" :disabled="srv.id === serviceSaving">
              Archive
            </button>
          </div>
        </article>
      </div>
      <p v-else-if="!servicesLoading" class="muted">No services.</p>
    </section>

    <!-- Products (CRUD) -->
    <section v-if="activeTab === 'products'" class="list-section">
      <!-- Products без изменений -->
      <div class="section-heading">
        <h2 class="section-title">Products</h2>
        <button class="button" @click="showProductForm = !showProductForm">
          {{ showProductForm ? 'Cancel' : 'New product' }}
        </button>
      </div>
      <div v-if="showProductForm" class="panel soft">
        <div class="form-grid two">
          <label class="field"><span>Name</span><input v-model="productForm.name" /></label>
          <label class="field"><span>Category</span><input v-model="productForm.category" /></label>
          <label class="field"><span>Price</span><input type="number" v-model="productForm.price" /></label>
          <label class="field"><span>Stock</span><input type="number" v-model="productForm.stock_quantity" /></label>
        </div>
        <label class="field"><span>Description</span><textarea v-model="productForm.description"></textarea></label>
        <div class="hero-actions">
          <button class="button" @click="saveProduct" :disabled="productSaving">
            {{ productForm.id ? 'Update' : 'Create' }}
          </button>
          <button class="button-secondary" @click="resetProductForm">Reset</button>
        </div>
        <p v-if="productError" class="error-text">{{ productError }}</p>
      </div>
      <div v-if="productsLoading" class="muted">Loading…</div>
      <p v-if="productsLoadError" class="error-text">{{ productsLoadError }}</p>
      <div v-if="products.length" class="list-column">
        <article v-for="prod in products" :key="prod.id" class="feed-card">
          <div class="meta-row">
            <strong>{{ prod.name }}</strong>
            <span class="chip">{{ prod.price }} BYN</span>
          </div>
          <p class="muted">Stock: {{ prod.stock_quantity }} | {{ prod.is_available ? 'Active' : 'Archived' }}</p>
          <div class="inline-actions">
            <button class="button-secondary" @click="editProduct(prod)">Edit</button>
            <button class="button" @click="archiveProduct(prod.id)" :disabled="productSaving === prod.id">Archive</button>
          </div>
        </article>
      </div>
      <p v-else-if="!productsLoading" class="muted">No products.</p>
    </section>

    <!-- News (CRUD) -->
    <section v-if="activeTab === 'news'" class="list-section">
      <!-- News без изменений -->
      <div class="section-heading">
        <h2 class="section-title">News</h2>
        <button class="button" @click="showNewsForm = !showNewsForm">
          {{ showNewsForm ? 'Cancel' : 'New article' }}
        </button>
      </div>
      <div v-if="showNewsForm" class="panel soft">
        <div class="form-grid two">
          <label class="field"><span>Title</span><input v-model="newsForm.title" /></label>
          <label class="field"><span>Published</span>
            <select v-model="newsForm.is_published">
              <option :value="true">Yes</option>
              <option :value="false">No</option>
            </select>
          </label>
        </div>
        <label class="field"><span>Content</span><textarea v-model="newsForm.content"></textarea></label>
        <label class="field"><span>Image URL</span><input v-model="newsForm.image_url" /></label>
        <div class="hero-actions">
          <button class="button" @click="saveNews" :disabled="newsSaving">
            {{ newsForm.id ? 'Update' : 'Publish' }}
          </button>
          <button class="button-secondary" @click="resetNewsForm">Reset</button>
        </div>
        <p v-if="newsError" class="error-text">{{ newsError }}</p>
      </div>
      <div v-if="newsLoading" class="muted">Loading…</div>
      <p v-if="newsLoadError" class="error-text">{{ newsLoadError }}</p>
      <div v-if="newsList.length" class="list-column">
        <article v-for="item in newsList" :key="item.id" class="feed-card">
          <div class="meta-row">
            <strong>{{ item.title }}</strong>
            <span class="chip">{{ item.is_published ? 'Published' : 'Draft' }}</span>
          </div>
          <p class="muted">{{ item.content?.slice(0, 100) }}…</p>
          <div class="inline-actions">
            <button class="button-secondary" @click="editNews(item)">Edit</button>
            <button class="button" @click="deleteNews(item.id)" :disabled="newsSaving === item.id">Delete</button>
          </div>
        </article>
      </div>
      <p v-else-if="!newsLoading" class="muted">No news.</p>
    </section>

    <!-- Reviews (moderation) -->
    <section v-if="activeTab === 'reviews'" class="list-section">
      <!-- Reviews без изменений -->
      <div class="section-heading">
        <h2 class="section-title">Review moderation</h2>
      </div>
      <div v-if="reviewsLoading" class="muted">Loading…</div>
      <p v-if="reviewsLoadError" class="error-text">{{ reviewsLoadError }}</p>
      <div v-if="reviews.length" class="list-column">
        <article v-for="rev in reviews" :key="rev.id" class="feed-card">
          <div class="meta-row">
            <strong>Rating {{ rev.rating }}/5</strong>
            <span class="chip" :class="rev.status">{{ rev.status }}</span>
          </div>
          <p class="muted">{{ rev.comment }}</p>
          <div class="inline-actions">
            <button
              v-if="rev.status !== 'approved'"
              class="button-secondary"
              @click="moderateReview(rev.id, 'approved')"
            >
              Approve
            </button>
            <button
              v-if="rev.status !== 'rejected'"
              class="button"
              @click="moderateReview(rev.id, 'rejected')"
            >
              Reject
            </button>
          </div>
        </article>
      </div>
      <p v-else-if="!reviewsLoading" class="muted">No reviews to moderate.</p>
    </section>

    <!-- Appointments (admin view) – ОБНОВЛЁН -->
    <section v-if="activeTab === 'appointments'" class="list-section">
      <div class="section-heading">
        <h2 class="section-title">All appointments</h2>
      </div>
      <div v-if="appointmentsLoading" class="muted">Loading…</div>
      <p v-if="appointmentsLoadError" class="error-text">{{ appointmentsLoadError }}</p>
      <div v-if="appointments.length && !appointmentsLoading" class="list-column">
        <article v-for="appt in appointments" :key="appt.id" class="feed-card appt-card">
          <div class="appt-header">
            <div class="appt-title">
              <span class="appt-icon">🐾</span>
              <strong>{{ getApptPetName(appt.pet_id) }} – {{ getApptServiceName(appt.service_id) }}</strong>
            </div>
            <span class="chip status-chip" :class="'status-' + appt.status">{{ appt.status }}</span>
          </div>
        
          <div class="appt-details">
            <div class="appt-detail">
              <span class="label">📅 Date</span>
              <span>{{ appt.appointment_date }} at {{ appt.appointment_time }}</span>
            </div>
            <div class="appt-detail">
              <span class="label">👤 User</span>
              <span>#{{ appt.user_id }}</span>
            </div>
            <div class="appt-detail">
              <span class="label">🩺 Doctor</span>
              <span>{{ getApptDoctorName(appt.doctor_id) }}</span>
            </div>
          </div>
        
          <div class="appt-actions">
            <select
              v-model="appt._newStatus"
              class="status-select"
              @change="changeApptStatus(appt.id, appt._newStatus)"
            >
              <!-- скрытая опция для отображения текущего статуса, не показываем disabled -->
              <option v-if="!appt._newStatus" disabled value="">Change...</option>
              <option value="pending">🕒 Pending</option>
              <option value="confirmed">✅ Confirmed</option>
              <option value="completed">✔️ Completed</option>
              <option value="paid">💰 Paid</option>
              <option value="canceled">❌ Canceled</option>
            </select>
          </div>
        </article>
      </div>
      <p v-else-if="!appointmentsLoading" class="muted">No appointments.</p>
    </section>

    <!-- Clinic Info -->
    <section v-if="activeTab === 'clinic'" class="list-section">
      <!-- без изменений -->
      <div class="section-heading">
        <h2 class="section-title">Clinic Information</h2>
      </div>
      <div v-if="clinicLoading" class="muted">Loading clinic info…</div>
      <p v-if="clinicError" class="error-text">{{ clinicError }}</p>
      <div v-if="clinicInfo" class="panel soft">
        <div class="form-grid two">
          <label class="field"><span>Name</span><input v-model="clinicInfo.name" /></label>
          <label class="field"><span>Address</span><input v-model="clinicInfo.address" /></label>
          <label class="field"><span>Phone</span><input v-model="clinicInfo.phone" /></label>
          <label class="field"><span>Email</span><input v-model="clinicInfo.email" /></label>
        </div>
        <label class="field"><span>Working Hours</span><textarea v-model="clinicInfo.working_hours"></textarea></label>
        <label class="field"><span>Social Links</span><textarea v-model="clinicInfo.social_links"></textarea></label>
        <label class="field"><span>Licenses</span><textarea v-model="clinicInfo.licenses"></textarea></label>
        <label class="field"><span>About Text</span><textarea v-model="clinicInfo.about_text"></textarea></label>
        <div class="hero-actions">
          <button class="button" @click="saveClinicInfo" :disabled="clinicSaving">
            Save
          </button>
        </div>
        <p v-if="clinicSaveError" class="error-text">{{ clinicSaveError }}</p>
      </div>
      <p v-else-if="!clinicLoading" class="muted">
        No clinic info loaded. Click <strong>Save</strong> to create it.
      </p>
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
      // ----- Dashboard -----
      metrics: [],
      metricsLoading: false,
      metricsError: null,
      // ----- Users -----
      users: [],
      usersLoading: false,
      usersError: null,
      // ----- Doctors -----
      doctors: [],
      doctorsLoading: false,
      doctorsError: null,
      showDoctorForm: false,
      doctorForm: this.emptyDoctorForm(),
      doctorSaving: false,
      doctorFormError: null,
      availableUsers: [],
      // ----- Services -----
      services: [],
      servicesLoading: false,
      servicesLoadError: null,
      showServiceForm: false,
      serviceForm: this.emptyServiceForm(),
      serviceSaving: false,
      serviceError: null,
      // ----- Products -----
      products: [],
      productsLoading: false,
      productsLoadError: null,
      showProductForm: false,
      productForm: this.emptyProductForm(),
      productSaving: false,
      productError: null,
      // ----- News -----
      newsList: [],
      newsLoading: false,
      newsLoadError: null,
      showNewsForm: false,
      newsForm: this.emptyNewsForm(),
      newsSaving: false,
      newsError: null,
      // ----- Reviews -----
      reviews: [],
      reviewsLoading: false,
      reviewsLoadError: null,
      // ----- Appointments -----
      appointments: [],
      appointmentsLoading: false,
      appointmentsLoadError: null,
      // справочники для отображения имён
      allPets: [],
      allServices: [],
      allDoctors: [],
      // ----- Clinic -----
      clinicInfo: null,
      clinicLoading: false,
      clinicError: null,
      clinicSaving: false,
      clinicSaveError: null,
    };
  },
  watch: {
    activeTab(newTab) {
      this.loadTabData(newTab);
    }
  },
  created() {
    this.loadDashboardMetrics();
    this.loadTabData(this.activeTab);
    this.fetchAvailableUsers();
    this.loadReferenceData(); // загружаем справочники один раз
  },
  methods: {
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
      } catch (e) {
        console.warn('Failed to load reference data for admin', e);
      }
    },
    // Вспомогательные методы для получения имён
    getApptPetName(petId) {
      const pet = this.allPets.find(p => p.id === petId);
      return pet ? pet.name : `Pet #${petId}`;
    },
    getApptServiceName(serviceId) {
      const srv = this.allServices.find(s => s.id === serviceId);
      return srv ? srv.name : `Service #${serviceId}`;
    },
    getApptDoctorName(doctorId) {
      if (!doctorId) return 'any doctor';
      const doc = this.allDoctors.find(d => d.id === doctorId);
      return doc ? doc.full_name : `Doctor #${doctorId}`;
    },

    // ---------- Dashboard ----------
    async loadDashboardMetrics() {
      this.metricsLoading = true;
      try {
        const resp = await adminService.getDashboard();
        const m = resp.data;
        this.metrics = [
          { value: m.total_appointments, label: 'Total appointments' },
          { value: m.appointments_this_week, label: 'This week' },
          { value: m.pending_appointments, label: 'Pending' },
          { value: m.total_users, label: 'Users' },
          { value: m.new_users_this_week, label: 'New users this week' },
          { value: m.total_products, label: 'Products' },
          { value: m.low_stock_products, label: 'Low stock' },
          { value: m.pending_reviews, label: 'Pending reviews' },
        ];
      } catch (e) {
        this.metricsError = 'Failed to load dashboard';
      } finally {
        this.metricsLoading = false;
      }
    },

    // ---------- Переключение вкладок ----------
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

    // ---------- Users ----------
    async fetchUsers() {
      this.usersLoading = true;
      this.usersError = null;
      try {
        const resp = await userService.listUsers();
        this.users = resp.data.users || resp.data;
      } catch (e) {
        this.usersError = 'Failed to load users';
      } finally {
        this.usersLoading = false;
      }
    },
    refreshUsers() { return this.fetchUsers(); },

    // ---------- Doctors ----------
    emptyDoctorForm() {
      return {
        id: null,
        user_id: '',
        full_name: '',
        specialization: '',
        description: '',
        photo_url: '',
        is_active: true,
      };
    },
    async fetchAvailableUsers() {
      try {
        const resp = await userService.listUsers();
        this.availableUsers = resp.data.users || resp.data;
      } catch (e) {
        console.error('Failed to load users for doctor form');
      }
    },
    editDoctor(doc) {
      this.doctorForm = {
        id: doc.id,
        user_id: doc.user_id || '',
        full_name: doc.full_name,
        specialization: doc.specialization || '',
        description: doc.description || '',
        photo_url: doc.photo_url || '',
        is_active: doc.is_active,
      };
      this.showDoctorForm = true;
    },
    resetDoctorForm() {
      this.doctorForm = this.emptyDoctorForm();
      this.doctorFormError = null;
      this.showDoctorForm = false;
    },
    async saveDoctor() {
      this.doctorSaving = true;
      this.doctorFormError = null;
      try {
        const payload = {
          user_id: parseInt(this.doctorForm.user_id),
          full_name: this.doctorForm.full_name,
          specialization: this.doctorForm.specialization,
          description: this.doctorForm.description,
          photo_url: this.doctorForm.photo_url,
          is_active: this.doctorForm.is_active,
        };
        if (this.doctorForm.id) {
          const {  ...rest } = payload;
          await doctorService.updateDoctor(this.doctorForm.id, rest);
        } else {
          await doctorService.createDoctor(payload);
        }
        this.resetDoctorForm();
        await this.fetchDoctors();
        await this.loadReferenceData(); // обновить справочники
      } catch (e) {
        this.doctorFormError = e.response?.data?.detail || 'Save failed';
      } finally {
        this.doctorSaving = false;
      }
    },
    async archiveDoctor(id) {
      if (!confirm('Archive this doctor?')) return;
      try {
        await doctorService.deleteDoctor(id);
        await this.fetchDoctors();
        await this.loadReferenceData();
      } catch (e) {
        alert('Failed to archive');
      }
    },
    async fetchDoctors() {
      this.doctorsLoading = true;
      this.doctorsError = null;
      try {
        const resp = await doctorService.getAll();
        this.doctors = resp.data;
      } catch (e) {
        this.doctorsError = 'Failed to load doctors';
      } finally {
        this.doctorsLoading = false;
      }
    },

    // ---------- Services ----------
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
        this.servicesLoadError = 'Failed to load services';
      } finally {
        this.servicesLoading = false;
      }
    },
    editService(srv) {
      this.serviceForm = { ...srv, price: srv.price, duration_minutes: srv.duration_minutes };
      this.showServiceForm = true;
    },
    resetServiceForm() {
      this.serviceForm = this.emptyServiceForm();
      this.serviceError = null;
      this.showServiceForm = false;
    },
    async saveService() {
      this.serviceSaving = true;
      this.serviceError = null;
      try {
        const payload = {
          name: this.serviceForm.name,
          description: this.serviceForm.description,
          price: parseFloat(this.serviceForm.price),
          duration_minutes: parseInt(this.serviceForm.duration_minutes),
          category: this.serviceForm.category,
        };
        if (this.serviceForm.id) {
          await serviceService.updateService(this.serviceForm.id, payload);
        } else {
          await serviceService.createService(payload);
        }
        this.resetServiceForm();
        await this.fetchServices();
        await this.loadReferenceData();
      } catch (e) {
        this.serviceError = e.response?.data?.detail || 'Save failed';
      } finally {
        this.serviceSaving = false;
      }
    },
    async archiveService(id) {
      if (!confirm('Archive this service?')) return;
      try {
        await serviceService.deleteService(id);
        await this.fetchServices();
        await this.loadReferenceData();
      } catch (e) {
        alert('Failed to archive');
      }
    },

    // ---------- Products ----------
    emptyProductForm() {
      return { id: null, name: '', description: '', price: '', stock_quantity: 0, category: '' };
    },
    async fetchProducts() {
      this.productsLoading = true;
      this.productsLoadError = null;
      try {
        const resp = await productService.getProducts();
        this.products = resp.data.products || resp.data;
      } catch (e) {
        this.productsLoadError = 'Failed to load products';
      } finally {
        this.productsLoading = false;
      }
    },
    editProduct(prod) {
      this.productForm = { ...prod, price: prod.price, stock_quantity: prod.stock_quantity };
      this.showProductForm = true;
    },
    resetProductForm() {
      this.productForm = this.emptyProductForm();
      this.productError = null;
      this.showProductForm = false;
    },
    async saveProduct() {
      this.productSaving = true;
      this.productError = null;
      try {
        const payload = {
          name: this.productForm.name,
          description: this.productForm.description,
          price: parseFloat(this.productForm.price),
          stock_quantity: parseInt(this.productForm.stock_quantity),
          category: this.productForm.category,
          is_available: true,
        };
        if (this.productForm.id) {
          await productService.updateProduct(this.productForm.id, payload);
        } else {
          await productService.createProduct(payload);
        }
        this.resetProductForm();
        await this.fetchProducts();
      } catch (e) {
        this.productError = e.response?.data?.detail || 'Save failed';
      } finally {
        this.productSaving = false;
      }
    },
    async archiveProduct(id) {
      if (!confirm('Archive this product?')) return;
      try {
        await productService.deleteProduct(id);
        await this.fetchProducts();
      } catch (e) {
        alert('Failed to archive');
      }
    },

    // ---------- News ----------
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
        this.newsLoadError = 'Failed to load news';
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
      this.newsSaving = true;
      this.newsError = null;
      try {
        const payload = {
          title: this.newsForm.title,
          content: this.newsForm.content,
          image_url: this.newsForm.image_url,
          is_published: this.newsForm.is_published,
        };
        if (this.newsForm.id) {
          await newsService.updateNews(this.newsForm.id, payload);
        } else {
          await newsService.createNews(payload);
        }
        this.resetNewsForm();
        await this.fetchNews();
      } catch (e) {
        this.newsError = e.response?.data?.detail || 'Save failed';
      } finally {
        this.newsSaving = false;
      }
    },
    async deleteNews(id) {
      if (!confirm('Delete this news permanently?')) return;
      try {
        await newsService.deleteNews(id);
        await this.fetchNews();
      } catch (e) {
        alert('Failed to delete');
      }
    },

    // ---------- Reviews ----------
    async fetchReviews() {
      this.reviewsLoading = true;
      this.reviewsLoadError = null;
      try {
        const resp = await reviewService.getReviews();
        this.reviews = resp.data.reviews || resp.data;
      } catch (e) {
        this.reviewsLoadError = 'Failed to load reviews';
      } finally {
        this.reviewsLoading = false;
      }
    },
    async moderateReview(id, status) {
      try {
        await reviewService.moderateReview(id, status);
        await this.fetchReviews();
      } catch (e) {
        alert('Moderation failed');
      }
    },

    // ---------- Appointments ----------
    async fetchAllAppointments() {
      this.appointmentsLoading = true;
      this.appointmentsLoadError = null;
      try {
        const resp = await appointmentService.getAllAppointments();
        const list = resp.data.appointments || resp.data;
        this.appointments = list;
      } catch (e) {
        this.appointmentsLoadError = 'Failed to load appointments';
      } finally {
        this.appointmentsLoading = false;
      }
    },
    async changeApptStatus(id, status) {
      if (!status) return;
      try {
        await appointmentService.updateStatus(id, status);
        await this.fetchAllAppointments();
      } catch (e) {
        alert('Status update failed');
      }
    },

    // ---------- Clinic Info ----------
    async fetchClinicInfo() {
      this.clinicLoading = true;
      this.clinicError = null;
      try {
        const resp = await clinicService.getAbout();
        this.clinicInfo = resp.data;
      } catch (e) {
        if (e.response && e.response.status === 404) {
          this.clinicInfo = {
            id: null,
            name: '',
            address: '',
            phone: '',
            email: '',
            working_hours: '',
            social_links: '',
            licenses: '',
            about_text: '',
          };
        } else {
          this.clinicError = 'Failed to load clinic info';
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
        alert('Clinic information saved');
      } catch (e) {
        this.clinicSaveError = e.response?.data?.detail || 'Save failed';
      } finally {
        this.clinicSaving = false;
      }
    },
  }
};
</script>

<style scoped>
.chip.active {
  background: var(--primary);
  color: #fff;
}
.error-text {
  color: #e53e3e;
  margin: 0.5rem 0;
}
.list-section {
  margin-top: 12px;
}
/* ----- Appointment card ----- */
.appt-card {
  padding: 20px;
  border-radius: var(--radius-lg);
}

.appt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.appt-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
}

.appt-icon {
  font-size: 1.3rem;
}

.status-chip {
  text-transform: capitalize;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.85rem;
}

/* цвета статусов */
.status-pending { background: #fff3cd; color: #856404; }
.status-confirmed { background: #d1ecf1; color: #0c5460; }
.status-completed { background: #d4edda; color: #155724; }
.status-paid { background: #c3e6cb; color: #0b2e13; }
.status-canceled { background: #f8d7da; color: #721c24; }

.appt-details {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 14px;
}

.appt-detail {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.95rem;
}

.appt-detail .label {
  color: var(--muted);
  font-weight: 600;
  font-size: 0.85rem;
}

.appt-actions {
  display: flex;
  justify-content: flex-end;
}
</style>