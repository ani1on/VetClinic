<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Запись на приём</h1>
        <p class="section-copy">
          Бронирование и список ваших записей.
        </p>
      </div>
    </div>

    <section class="split-grid">
      <!-- Форма бронирования -->
      <article class="panel">
        <h2 class="section-title">Новая запись</h2>
        <div v-if="formLoading" class="muted">Загрузка данных формы…</div>
        <p v-if="formError" class="error-text">{{ formError }}</p>
        <div v-else class="form-grid two">
          <label class="field">
            <span>Питомец *</span>
            <select v-model="newAppointment.pet_id">
              <option disabled value="">-- Выберите питомца --</option>
              <option v-for="pet in pets" :key="pet.id" :value="pet.id">
                {{ pet.name }} ({{ pet.species }})
              </option>
            </select>
          </label>
          <label class="field">
            <span>Услуга *</span>
            <select v-model="newAppointment.service_id">
              <option disabled value="">-- Выберите услугу --</option>
              <option v-for="srv in services" :key="srv.id" :value="srv.id">
                {{ srv.name }} – {{ srv.price }} BYN
              </option>
            </select>
          </label>
          <label class="field">
            <span>Врач</span>
            <select v-model="newAppointment.doctor_id">
              <option :value="null">Любой врач</option>
              <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
                {{ doc.full_name }} ({{ doc.specialization || 'Общий' }})
              </option>
            </select>
          </label>
          <label class="field">
            <span>Дата *</span>
            <input type="date" v-model="newAppointment.appointment_date" :min="minDate" @change="validateDate" />
          </label>
          <label class="field">
            <span>Время *</span>
            <select v-model="newAppointment.appointment_time">
              <option disabled value="">-- Выберите время --</option>
              <option v-for="time in timeSlots" :key="time" :value="time">
                {{ time }}
              </option>
            </select>
          </label>
        </div>
        <label class="field">
          <span>Комментарий для врача</span>
          <textarea v-model="newAppointment.comment" placeholder="Опишите симптомы или поведение питомца перед визитом."></textarea>
        </label>
        <div class="hero-actions">
          <button class="button" type="button" @click="createAppointment" :disabled="appointmentSaving">
            {{ appointmentSaving ? 'Сохранение…' : 'Записаться' }}
          </button>
        </div>
        <p v-if="submitError" class="error-text">{{ submitError }}</p>
      </article>

      <!-- Существующие записи -->
      <article class="panel">
        <h2 class="section-title">Мои записи</h2>
        <div v-if="apptsLoading" class="muted">Загрузка записей…</div>
        <p v-if="apptsError" class="error-text">{{ apptsError }}</p>
        <div v-if="appointments.length" class="list-column">
          <article v-for="item in appointments" :key="item.id" class="feed-card">
            <div class="meta-row">
              <strong>{{ getPetName(item.pet_id) }} – {{ getServiceName(item.service_id) }}</strong>
              <span class="chip">{{ translateStatus(item.status) }}</span>
            </div>
            <p class="muted">{{ formatDateTime(item) }}</p>
            <div class="inline-actions">
              <button
                v-if="item.status !== 'canceled' && item.status !== 'completed' && item.status !== 'paid'"
                class="button-secondary"
                @click="cancelAppointment(item.id)"
                :disabled="cancelling === item.id"
              >
                {{ cancelling === item.id ? 'Отмена…' : 'Отменить' }}
              </button>
            </div>
          </article>
        </div>
        <p v-else-if="!apptsLoading" class="muted">У вас пока нет записей.</p>
      </article>
    </section>
  </section>
</template>

<script>
import appointmentService from '@/services/appointmentService';
import petService from '@/services/petService';
import serviceService from '@/services/serviceService';
import doctorService from '@/services/doctorService';

export default {
  name: "AppointmentView",
  data() {
    return {
      // Форма
      newAppointment: {
        pet_id: '',
        service_id: '',
        doctor_id: null,
        appointment_date: '',
        appointment_time: '',
        comment: ''
      },
      pets: [],
      services: [],
      doctors: [],
      formLoading: false,
      formError: null,
      appointmentSaving: false,
      submitError: null,
      // Список записей
      appointments: [],
      apptsLoading: false,
      apptsError: null,
      cancelling: null,
      // Доступные временные слоты
      timeSlots: ['13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'],
    };
  },
  computed: {
    minDate() {
      const today = new Date();
      const yyyy = today.getFullYear();
      const mm = String(today.getMonth() + 1).padStart(2, '0');
      const dd = String(today.getDate()).padStart(2, '0');
      return `${yyyy}-${mm}-${dd}`;
    }
  },
  async created() {
    await Promise.all([this.fetchFormData(), this.fetchAppointments()]);
  },
  methods: {
    // Улучшенный парсинг ошибок API с обработкой сетевых ошибок и 5xx
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
          const messages = data.map(err => {
            const field = err.loc[err.loc.length - 1];
            return `Поле "${field}": ${err.msg}`;
          });
          return messages.join('; ');
        }
        if (data.detail) {
          if (typeof data.detail === 'string') return data.detail;
          if (Array.isArray(data.detail)) return data.detail.map(d => d.msg).join('; ');
          return JSON.stringify(data.detail);
        }
        if (data.message) return data.message;
      }
      return 'Произошла ошибка. Попробуйте обновить страницу.';
    },

    translateStatus(status) {
      const map = {
        pending: 'Ожидает',
        confirmed: 'Подтверждено',
        completed: 'Завершено',
        paid: 'Оплачено',
        canceled: 'Отменено'
      };
      return map[status] || status;
    },

    formatDateTime(appt) {
      const date = appt.appointment_date;
      const time = appt.appointment_time;
      return `${date} в ${time}`;
    },

    async fetchFormData() {
      this.formLoading = true;
      this.formError = null;
      try {
        const [petsResp, servicesResp, doctorsResp] = await Promise.all([
          petService.getMyPets(),
          serviceService.getServices(),
          doctorService.getAll()
        ]);
        this.pets = petsResp.data;
        this.services = servicesResp.data;
        this.doctors = doctorsResp.data;
      } catch (e) {
        this.formError = this.parseApiError(e);
      } finally {
        this.formLoading = false;
      }
    },

    async fetchAppointments() {
      this.apptsLoading = true;
      this.apptsError = null;
      try {
        const resp = await appointmentService.getMyAppointments();
        this.appointments = resp.data;
      } catch (e) {
        this.apptsError = this.parseApiError(e);
      } finally {
        this.apptsLoading = false;
      }
    },

    getPetName(petId) {
      const pet = this.pets.find(p => p.id === petId);
      return pet ? pet.name : `Питомец #${petId}`;
    },

    getServiceName(serviceId) {
      const srv = this.services.find(s => s.id === serviceId);
      return srv ? srv.name : `Услуга #${serviceId}`;
    },

    getDoctorName(doctorId) {
      if (!doctorId) return 'Любой врач';
      const doc = this.doctors.find(d => d.id === doctorId);
      return doc ? doc.full_name : `Врач #${doctorId}`;
    },

    // Валидация даты
    validateDate() {
      const selected = this.newAppointment.appointment_date;
      if (!selected) return;

      const selectedDate = new Date(selected);
      const today = new Date();
      today.setHours(0, 0, 0, 0);

      if (selectedDate < today) {
        this.submitError = 'Дата не может быть раньше сегодняшнего дня.';
        this.newAppointment.appointment_date = '';
        return;
      }

      const dayOfWeek = selectedDate.getDay();
      if (dayOfWeek === 0 || dayOfWeek === 6) {
        this.submitError = 'Запись возможна только в будние дни (пн–пт).';
        this.newAppointment.appointment_date = '';
        return;
      }

      this.submitError = null;
    },

    async createAppointment() {
      if (!this.newAppointment.pet_id) {
        this.submitError = 'Выберите питомца.';
        return;
      }
      if (!this.newAppointment.service_id) {
        this.submitError = 'Выберите услугу.';
        return;
      }
      if (!this.newAppointment.appointment_date) {
        this.submitError = 'Выберите дату.';
        return;
      }
      if (!this.newAppointment.appointment_time) {
        this.submitError = 'Выберите время.';
        return;
      }

      const selectedDate = new Date(this.newAppointment.appointment_date);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (selectedDate < today) {
        this.submitError = 'Дата не может быть раньше сегодняшнего дня.';
        return;
      }
      const dayOfWeek = selectedDate.getDay();
      if (dayOfWeek === 0 || dayOfWeek === 6) {
        this.submitError = 'Запись возможна только в будние дни.';
        return;
      }

      this.appointmentSaving = true;
      this.submitError = null;
      try {
        const payload = {
          pet_id: this.newAppointment.pet_id,
          service_id: this.newAppointment.service_id,
          doctor_id: this.newAppointment.doctor_id ? parseInt(this.newAppointment.doctor_id) : null,
          appointment_date: this.newAppointment.appointment_date,
          appointment_time: this.newAppointment.appointment_time,
          comment: this.newAppointment.comment
        };
        await appointmentService.createAppointment(payload);
        // Сброс формы
        this.newAppointment = {
          pet_id: '',
          service_id: '',
          doctor_id: null,
          appointment_date: '',
          appointment_time: '',
          comment: ''
        };
        await this.fetchAppointments();
      } catch (e) {
        this.submitError = this.parseApiError(e);
      } finally {
        this.appointmentSaving = false;
      }
    },

    async cancelAppointment(id) {
      this.cancelling = id;
      this.apptsError = null;
      try {
        await appointmentService.cancelAppointment(id);
        await this.fetchAppointments();
      } catch (e) {
        this.apptsError = this.parseApiError(e);
      } finally {
        this.cancelling = null;
      }
    }
  }
};
</script>

<style scoped>
.error-text { color: #e53e3e; margin-top: 0.5rem; }
</style>