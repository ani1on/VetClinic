<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Profile</h1>
        <p class="section-copy">Personal cabinet with owner data, pet cards, prescriptions.</p>
      </div>
    </div>

    <section class="split-grid">
      <article class="panel">
        <h2 class="section-title">Owner card</h2>
        <div v-if="profileLoading" class="muted">Loading profile…</div>
        <p v-if="profileError" class="error-text">{{ profileError }}</p>
        <div v-if="profile" class="form-grid two">
          <label class="field">
            <span>Full name</span>
            <input type="text" v-model="profile.name" />
          </label>
          <label class="field">
            <span>Phone</span>
            <input type="text" v-model="profile.phone" />
          </label>
          <label class="field">
            <span>Email</span>
            <input type="email" v-model="profile.email" />
          </label>
        </div>
        <div class="hero-actions">
          <button class="button" type="button" @click="saveProfile" :disabled="saving">
            {{ saving ? 'Saving…' : 'Save changes' }}
          </button>
        </div>
        <p v-if="saveError" class="error-text">{{ saveError }}</p>
      </article>

      <article class="panel">
        <h2 class="section-title">Pet cards</h2>
        <div v-if="petsLoading" class="muted">Loading pets…</div>
        <p v-if="petsError" class="error-text">{{ petsError }}</p>
        <div v-if="pets.length" class="list-column">
          <article v-for="pet in pets" :key="pet.id" class="feed-card">
            <div class="meta-row">
              <strong>{{ pet.name }}</strong>
              <span class="chip">{{ pet.species }}</span>
            </div>
            <p class="muted">
              {{ pet.age || 'Age not set' }}, {{ pet.gender }}, {{ pet.notes }}
            </p>
          </article>
        </div>
        <p v-else-if="!petsLoading" class="muted">No pets added.</p>
      </article>
    </section>

    <section class="panel">
      <h2 class="section-title">History and recommendations</h2>
      <div class="tile-grid">
        <article class="tile soft">
          <h3 class="card-title">Medical history</h3>
          <p class="muted">Visits, diagnoses, lab results and attached files from the backend.</p>
        </article>
        <article class="tile soft success">
          <h3 class="card-title">Prescriptions</h3>
          <p class="muted">Current medication plans and dosage reminders for each pet.</p>
        </article>
        <article class="tile soft warn">
          <h3 class="card-title">Recommendations</h3>
          <p class="muted">Doctor tips, repeat purchases and preventive procedures.</p>
        </article>
      </div>
    </section>
  </section>
</template>

<script>
import userService from '@/services/userService';
import petService from '@/services/petService';

export default {
  name: "ProfileView",
  data() {
    return {
      profile: null,
      profileLoading: false,
      profileError: null,
      saving: false,
      saveError: null,
      pets: [],
      petsLoading: false,
      petsError: null,
    };
  },
  async created() {
    await Promise.all([this.fetchProfile(), this.fetchPets()]);
  },
  methods: {
    async fetchProfile() {
      this.profileLoading = true;
      try {
        const resp = await userService.getProfile();
        this.profile = resp.data;
      } catch (e) {
        this.profileError = 'Failed to load profile';
      } finally {
        this.profileLoading = false;
      }
    },
    async fetchPets() {
      this.petsLoading = true;
      try {
        const resp = await petService.getMyPets();
        this.pets = resp.data;
      } catch (e) {
        this.petsError = 'Failed to load pets';
      } finally {
        this.petsLoading = false;
      }
    },
    async saveProfile() {
      if (!this.profile) return;
      this.saving = true;
      this.saveError = null;
      try {
        await userService.updateProfile({
          name: this.profile.name,
          phone: this.profile.phone,
          email: this.profile.email,
        });
        alert('Profile updated');
      } catch (e) {
        this.saveError = e.response?.data?.detail || 'Failed to update profile';
      } finally {
        this.saving = false;
      }
    }
  }
};
</script>
<style scoped>
.error-text { color: #e53e3e; margin-top: 0.5rem; }
</style>