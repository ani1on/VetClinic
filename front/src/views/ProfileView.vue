<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Profile</h1>
        <p class="section-copy">Personal cabinet with owner data, pet cards, prescriptions.</p>
      </div>
    </div>

    <section class="split-grid">
      <!-- Владелец -->
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

      <!-- Питомцы -->
      <article class="panel">
        <div class="section-heading">
          <h2 class="section-title">Pet cards</h2>
          <button class="button" @click="openAddPet">+ Add pet</button>
        </div>

        <div v-if="petsLoading" class="muted">Loading pets…</div>
        <p v-if="petsError" class="error-text">{{ petsError }}</p>

        <!-- Список питомцев -->
        <div v-if="pets.length" class="list-column">
          <article v-for="pet in pets" :key="pet.id" class="feed-card">
            <div class="meta-row">
              <strong>{{ pet.name }}</strong>
              <span class="chip">{{ pet.species }}</span>
            </div>
            <p class="muted">
              {{ pet.breed || '' }} {{ pet.gender ? ', ' + pet.gender : '' }}
              {{ pet.birth_date ? ', birth: ' + pet.birth_date : '' }}
            </p>
            <p class="muted" v-if="pet.weight">Weight: {{ pet.weight }} kg</p>
            <p class="muted" v-if="pet.notes">{{ pet.notes }}</p>
            <div class="hero-actions">
              <button class="button-secondary" @click="openEditPet(pet)">Edit</button>
              <button class="button" @click="deletePet(pet.id)">Delete</button>
            </div>
          </article>
        </div>
        <p v-else-if="!petsLoading" class="muted">No pets added yet.</p>

        <!-- Форма добавления / редактирования питомца -->
        <div v-if="showPetForm" class="panel soft" style="margin-top: 16px;">
          <h3 class="card-title" style="margin-top:0">{{ editingPet ? 'Edit pet' : 'New pet' }}</h3>
          <div class="form-grid two">
            <label class="field">
              <span>Name *</span>
              <input v-model="petForm.name" placeholder="Pet name" />
            </label>
            <label class="field">
              <span>Species *</span>
              <input v-model="petForm.species" placeholder="e.g. Dog, Cat" />
            </label>
            <label class="field">
              <span>Breed</span>
              <input v-model="petForm.breed" placeholder="Optional" />
            </label>
            <label class="field">
              <span>Gender</span>
              <select v-model="petForm.gender">
                <option value="">Not set</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </label>
            <label class="field">
              <span>Birth date</span>
              <input type="date" v-model="petForm.birth_date" />
            </label>
            <label class="field">
              <span>Weight (kg)</span>
              <input type="number" step="0.1" v-model="petForm.weight" placeholder="0.0" />
            </label>
          </div>
          <label class="field" style="margin-top:8px">
            <span>Color</span>
            <input v-model="petForm.color" placeholder="Optional" />
          </label>
          <label class="field">
            <span>Notes</span>
            <textarea v-model="petForm.notes" placeholder="Any special notes..."></textarea>
          </label>

          <div class="hero-actions">
            <button class="button" @click="savePet" :disabled="petSaving">
              {{ petSaving ? 'Saving…' : editingPet ? 'Update' : 'Create' }}
            </button>
            <button class="button-secondary" @click="closePetForm">Cancel</button>
          </div>
          <p v-if="petFormError" class="error-text">{{ petFormError }}</p>
        </div>
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
      // --- Profile ---
      profile: null,
      profileLoading: false,
      profileError: null,
      saving: false,
      saveError: null,

      // --- Pets ---
      pets: [],
      petsLoading: false,
      petsError: null,

      // --- Pet Form ---
      showPetForm: false,
      editingPet: null,        // объект питомца, если редактируем, иначе null
      petForm: {
        name: '',
        species: '',
        breed: '',
        gender: '',
        birth_date: '',
        weight: '',
        color: '',
        notes: ''
      },
      petSaving: false,
      petFormError: null,
    };
  },
  async created() {
    await Promise.all([this.fetchProfile(), this.fetchPets()]);
  },
  methods: {
    // ========== PROFILE ==========
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
    },

    // ========== PETS ==========
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

    // ----- Pet form helpers -----
    openAddPet() {
      this.editingPet = null;
      this.petForm = {
        name: '',
        species: '',
        breed: '',
        gender: '',
        birth_date: '',
        weight: '',
        color: '',
        notes: ''
      };
      this.petFormError = null;
      this.showPetForm = true;
    },
    openEditPet(pet) {
      this.editingPet = pet;
      this.petForm = {
        name: pet.name,
        species: pet.species,
        breed: pet.breed || '',
        gender: pet.gender || '',
        birth_date: pet.birth_date || '',
        weight: pet.weight !== null ? pet.weight : '',
        color: pet.color || '',
        notes: pet.notes || ''
      };
      this.petFormError = null;
      this.showPetForm = true;
    },
    closePetForm() {
      this.showPetForm = false;
      this.editingPet = null;
    },

    async savePet() {
      // Простая валидация обязательных полей
      if (!this.petForm.name.trim() || !this.petForm.species.trim()) {
        this.petFormError = 'Name and species are required';
        return;
      }

      this.petSaving = true;
      this.petFormError = null;

      // Подготавливаем payload, убирая пустые строки для необязательных числовых/датовых полей
      const payload = {
        name: this.petForm.name.trim(),
        species: this.petForm.species.trim(),
        breed: this.petForm.breed.trim() || null,
        gender: this.petForm.gender || null,
        birth_date: this.petForm.birth_date || null,
        weight: this.petForm.weight ? parseFloat(this.petForm.weight) : null,
        color: this.petForm.color.trim() || null,
        notes: this.petForm.notes.trim() || null,
      };

      try {
        if (this.editingPet) {
          await petService.updatePet(this.editingPet.id, payload);
        } else {
          await petService.createPet(payload);
        }
        this.closePetForm();
        await this.fetchPets(); // обновить список
      } catch (e) {
        this.petFormError = e.response?.data?.detail || 'Failed to save pet';
      } finally {
        this.petSaving = false;
      }
    },

    async deletePet(id) {
      if (!confirm('Delete this pet? It will be archived.')) return;
      try {
        await petService.deletePet(id);
        await this.fetchPets();
      } catch (e) {
        alert('Failed to delete pet');
      }
    }
  }
};
</script>

<style scoped>
.error-text { color: #e53e3e; margin-top: 0.5rem; }
</style>