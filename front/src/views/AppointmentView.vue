<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Appointment</h1>
        <p class="section-copy">
          Booking flow and list of existing records.
        </p>
      </div>
    </div>

    <section class="split-grid">
      <!-- Форма бронирования -->
      <article class="panel">
        <h2 class="section-title">New booking</h2>
        <div v-if="formLoading" class="muted">Loading form data…</div>
        <p v-if="formError" class="error-text">{{ formError }}</p>
        <div v-else class="form-grid two">
          <label class="field">
            <span>Pet *</span>
            <select v-model="newAppointment.pet_id">
              <option disabled value="">Select pet</option>
              <option v-for="pet in pets" :key="pet.id" :value="pet.id">
                {{ pet.name }} ({{ pet.species }})
              </option>
            </select>
          </label>
          <label class="field">
            <span>Service *</span>
            <select v-model="newAppointment.service_id">
              <option disabled value="">Select service</option>
              <option v-for="srv in services" :key="srv.id" :value="srv.id">
                {{ srv.name }} – {{ srv.price }} BYN
              </option>
            </select>
          </label>
          <label class="field">
            <span>Doctor</span>
            <select v-model="newAppointment.doctor_id">
              <option :value="null">Any doctor</option>
              <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
                {{ doc.full_name }} ({{ doc.specialization || 'General' }})
              </option>
            </select>
          </label>
          <label class="field">
            <span>Date *</span>
            <input type="date" v-model="newAppointment.appointment_date" />
          </label>
          <label class="field" />
          <label class="field">
            <span>Time *</span>
            <input type="time" v-model="newAppointment.appointment_time" />
          </label>
        </div>
        <label class="field">
          <span>Comment for doctor</span>
          <textarea v-model="newAppointment.comment" placeholder="Describe symptoms or pet behavior before visit."></textarea>
        </label>
        <div class="hero-actions">
          <button class="button" type="button" @click="createAppointment" :disabled="appointmentSaving">
            {{ appointmentSaving ? 'Saving…' : 'Create appointment' }}
          </button>
        </div>
        <p v-if="submitError" class="error-text">{{ submitError }}</p>
      </article>

      <!-- Существующие записи -->
      <article class="panel">
        <h2 class="section-title">My records</h2>
        <div v-if="apptsLoading" class="muted">Loading appointments…</div>
        <p v-if="apptsError" class="error-text">{{ apptsError }}</p>
        <div v-if="appointments.length" class="list-column">
          <article v-for="item in appointments" :key="item.id" class="feed-card">
            <div class="meta-row">
              <strong>{{ getPetName(item.pet_id) }} – {{ getServiceName(item.service_id) }}</strong>
              <span class="chip">{{ item.status }}</span>
            </div>
            <p class="muted">{{ item.appointment_date }} at {{ item.appointment_time }} with {{ getDoctorName(item.doctor_id) }}</p>
            <div class="inline-actions">
              <button
                v-if="item.status !== 'canceled' && item.status !== 'completed' && item.status !== 'paid'"
                class="button-secondary"
                @click="cancelAppointment(item.id)"
                :disabled="cancelling === item.id"
              >
                Cancel
              </button>
            </div>
          </article>
        </div>
        <p v-else-if="!apptsLoading" class="muted">No appointments yet.</p>
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
      // форма
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
      // список
      appointments: [],
      apptsLoading: false,
      apptsError: null,
      cancelling: null,
    };
  },
  async created() {
    await Promise.all([this.fetchFormData(), this.fetchAppointments()]);
  },
  methods: {
    async fetchFormData() {
      this.formLoading = true;
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
        this.formError = 'Failed to load pets, services or doctors';
      } finally {
        this.formLoading = false;
      }
    },
    async fetchAppointments() {
      this.apptsLoading = true;
      try {
        const resp = await appointmentService.getMyAppointments();
        this.appointments = resp.data;
      } catch (e) {
        this.apptsError = 'Failed to load appointments';
      } finally {
        this.apptsLoading = false;
      }
    },
    // Вспомогательные методы для получения имён по ID
    getPetName(petId) {
      const pet = this.pets.find(p => p.id === petId);
      return pet ? pet.name : `Pet #${petId}`;
    },
    getServiceName(serviceId) {
      const srv = this.services.find(s => s.id === serviceId);
      return srv ? srv.name : `Service #${serviceId}`;
    },
    getDoctorName(doctorId) {
      if (!doctorId) return 'any doctor';
      const doc = this.doctors.find(d => d.id === doctorId);
      return doc ? doc.full_name : `Doctor #${doctorId}`;
    },
    async createAppointment() {
      if (!this.newAppointment.pet_id || !this.newAppointment.service_id ||
          !this.newAppointment.appointment_date || !this.newAppointment.appointment_time) {
        this.submitError = 'Please fill all required fields (pet, service, date, time)';
        return;
      }

      this.appointmentSaving = true;
      this.submitError = null;
      try {
        const payload = {
          ...this.newAppointment,
          doctor_id: this.newAppointment.doctor_id ? parseInt(this.newAppointment.doctor_id) : null
        };
        await appointmentService.createAppointment(payload);
        // сброс формы
        this.newAppointment = {
          pet_id: '', service_id: '', doctor_id: null,
          appointment_date: '', appointment_time: '', comment: ''
        };
        await this.fetchAppointments();
      } catch (e) {
        this.submitError = e.response?.data?.detail || 'Failed to create appointment';
      } finally {
        this.appointmentSaving = false;
      }
    },
    async cancelAppointment(id) {
      this.cancelling = id;
      try {
        await appointmentService.cancelAppointment(id);
        await this.fetchAppointments();
      } catch (e) {
        alert('Failed to cancel');
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