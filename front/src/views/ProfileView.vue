<template>
  <section class="page">
    <!-- Тосты -->
    <div v-if="toastMessage" class="toast" :class="toastType">{{ toastMessage }}</div>

    <div class="section-heading">
      <div>
        <h1 class="section-title">Профиль</h1>
        <p class="section-copy">Личный кабинет с данными владельца, карточками питомцев, корзиной и отзывами.</p>
      </div>
    </div>

    <!-- Карточка владельца и Питомцы -->
    <section class="split-grid">
      <article class="panel">
        <h2 class="section-title">Карточка владельца</h2>
        <div v-if="profileLoading" class="muted">Загрузка профиля…</div>
        <p v-if="profileError" class="error-text">{{ profileError }}</p>
        <div v-if="profile" class="form-grid two">
          <label class="field"><span>ФИО</span><input type="text" v-model="profile.name" /></label>
          <label class="field"><span>Телефон</span><input type="text" v-model="profile.phone" /></label>
          <label class="field"><span>Email</span><input type="email" v-model="profile.email" /></label>
        </div>
        <div class="hero-actions">
          <button class="button" @click="saveProfile" :disabled="saving">{{ saving ? 'Сохранение…' : 'Сохранить изменения' }}</button>
        </div>
        <p v-if="saveError" class="error-text">{{ saveError }}</p>
      </article>

      <article class="panel">
        <div class="section-heading">
          <h2 class="section-title">Карточки питомцев</h2>
          <button class="button" @click="openAddPet">+ Добавить питомца</button>
        </div>
        <div v-if="petsLoading" class="muted">Загрузка питомцев…</div>
        <p v-if="petsError" class="error-text">{{ petsError }}</p>
        <div v-if="pets.length" class="list-column">
          <article v-for="pet in pets" :key="pet.id" class="feed-card">
            <div class="meta-row"><strong>{{ pet.name }}</strong><span class="chip">{{ pet.species }}</span></div>
            <p class="muted">{{ pet.breed || '' }} {{ translateGender(pet.gender) ? ', ' + translateGender(pet.gender) : '' }}{{ pet.birth_date ? ', дата рождения: ' + pet.birth_date : '' }}</p>
            <p class="muted" v-if="pet.weight">Вес: {{ pet.weight }} кг</p>
            <p class="muted" v-if="pet.color">Окрас: {{ pet.color }}</p>
            <p class="muted" v-if="pet.notes">{{ pet.notes }}</p>
            <div class="hero-actions">
              <button class="button-secondary" @click="openEditPet(pet)">Редактировать</button>
              <button class="button" @click="deletePet(pet.id)">Удалить</button>
            </div>
          </article>
        </div>
        <p v-else-if="!petsLoading" class="muted">Пока нет добавленных питомцев.</p>

        <div v-if="showPetForm" class="panel soft" style="margin-top: 16px;">
          <h3 class="card-title">{{ editingPet ? 'Редактировать питомца' : 'Новый питомец' }}</h3>
          <div class="form-grid two">
            <label class="field"><span>Кличка *</span><input v-model="petForm.name" placeholder="Кличка" /></label>
            <label class="field"><span>Вид *</span><input v-model="petForm.species" placeholder="Собака, Кошка" /></label>
            <label class="field"><span>Порода</span><input v-model="petForm.breed" placeholder="Необязательно" /></label>
            <label class="field"><span>Пол</span><select v-model="petForm.gender"><option value="">Не указан</option><option value="male">Мужской</option><option value="female">Женский</option></select></label>
            <label class="field"><span>Дата рождения</span><input type="date" v-model="petForm.birth_date" :max="maxBirthDate" /></label>
            <label class="field"><span>Вес (кг)</span><input type="number" step="0.1" v-model="petForm.weight" /></label>
          </div>
          <label class="field"><span>Окрас</span><input v-model="petForm.color" /></label>
          <label class="field"><span>Заметки</span><textarea v-model="petForm.notes"></textarea></label>
          <div class="hero-actions">
            <button class="button" @click="savePet" :disabled="petSaving">{{ petSaving ? 'Сохранение…' : (editingPet ? 'Обновить' : 'Создать') }}</button>
            <button class="button-secondary" @click="closePetForm">Отмена</button>
          </div>
          <p v-if="petFormError" class="error-text">{{ petFormError }}</p>
        </div>
      </article>
    </section>

    <!-- Корзина -->
    <section class="panel">
      <div class="section-heading">
        <h2 class="section-title">Моя корзина</h2>
        <button class="button" @click="createOrder" :disabled="cart.items?.length === 0 || orderCreating">{{ orderCreating ? 'Оформление…' : 'Оформить заказ' }}</button>
      </div>
      <div v-if="cartLoading" class="muted">Загрузка корзины…</div>
      <p v-if="cartError" class="error-text">{{ cartError }}</p>
      <div v-if="cart.items?.length" class="list-column">
        <article v-for="item in cart.items" :key="item.id" class="feed-card">
          <div class="meta-row"><strong>{{ getProductName(item.product_id) || `Товар #${item.product_id}` }}</strong><strong>{{ (item.product?.price || 0) * item.quantity }} BYN</strong></div>
          <div class="price-row">
            <div class="inline-actions">
              <button class="button-secondary" @click="updateCartItem(item.id, item.quantity - 1)" :disabled="item.quantity <= 1">−</button>
              <span>{{ item.quantity }}</span>
              <button class="button-secondary" @click="updateCartItem(item.id, item.quantity + 1)">+</button>
            </div>
            <button class="button" @click="removeCartItem(item.id)">Удалить</button>
          </div>
        </article>
        <div class="divider"></div>
        <div class="meta-row"><strong>Итого:</strong><strong>{{ cartTotal }} BYN</strong></div>
      </div>
      <p v-else-if="!cartLoading" class="muted">Корзина пуста.</p>
    </section>

    <!-- Оставить отзыв -->
    <section class="panel">
      <div class="section-heading">
        <h2 class="section-title">Оставить отзыв о клинике</h2>
      </div>
      <div class="form-grid two">
        <label class="field">
          <span>Оценка *</span>
          <select v-model="newReview.rating">
            <option disabled value="">-- Выберите --</option>
            <option v-for="n in 5" :key="n" :value="n">{{ n }} {{ n === 1 ? 'звезда' : (n < 5 ? 'звезды' : 'звёзд') }}</option>
          </select>
        </label>
        <label class="field full-width">
          <span>Комментарий</span>
          <textarea v-model="newReview.comment" rows="3" placeholder="Поделитесь впечатлениями о работе клиники..."></textarea>
        </label>
      </div>
      <div class="hero-actions">
        <button class="button" @click="submitReview" :disabled="reviewSubmitting">{{ reviewSubmitting ? 'Отправка…' : 'Отправить отзыв' }}</button>
      </div>
      <p v-if="reviewSubmitError" class="error-text">{{ reviewSubmitError }}</p>
    </section>

    <!-- Мои отзывы -->
    <section class="panel">
      <div class="section-heading">
        <h2 class="section-title">Мои отзывы</h2>
        <button class="button-secondary" @click="fetchMyReviews">Обновить</button>
      </div>
      <div v-if="reviewsLoading" class="muted">Загрузка отзывов…</div>
      <p v-if="reviewsError" class="error-text">{{ reviewsError }}</p>
      <div v-if="myReviews.length" class="list-column">
        <article v-for="rev in myReviews" :key="rev.id" class="feed-card">
          <div class="meta-row"><strong>Оценка {{ rev.rating }}/5</strong><span class="chip">{{ translateReviewStatus(rev.status) }}</span></div>
          <p class="muted">{{ rev.comment }}</p>
          <p class="muted" v-if="rev.created_at">Создан: {{ new Date(rev.created_at).toLocaleDateString() }}</p>
          <div class="hero-actions">
            <button class="button" @click="deleteMyReview(rev.id)" :disabled="rev.deleting">Удалить</button>
          </div>
        </article>
      </div>
      <p v-else-if="!reviewsLoading" class="muted">Вы ещё не оставляли отзывы.</p>
    </section>
  </section>
</template>

<script>
import userService from '@/services/userService';
import petService from '@/services/petService';
import cartService from '@/services/cartService';
import reviewService from '@/services/reviewService';
import orderService from '@/services/orderService';
import productService from '@/services/productService';

export default {
  name: "ProfileView",
  data() {
    return {
      toastMessage: '', toastType: '',
      profile: null, profileLoading: false, profileError: null, saving: false, saveError: null,
      pets: [], petsLoading: false, petsError: null,
      showPetForm: false, editingPet: null, petSaving: false, petFormError: null,
      petForm: { name: '', species: '', breed: '', gender: '', birth_date: '', weight: '', color: '', notes: '' },
      cart: { items: [] }, cartLoading: false, cartError: null, orderCreating: false, allProducts: [],
      newReview: { rating: '', comment: '' }, reviewSubmitting: false, reviewSubmitError: null,
      myReviews: [], reviewsLoading: false, reviewsError: null,
    };
  },
  computed: {
    maxBirthDate() {
      const today = new Date();
      const yyyy = today.getFullYear();
      const mm = String(today.getMonth() + 1).padStart(2, '0');
      const dd = String(today.getDate()).padStart(2, '0');
      return `${yyyy}-${mm}-${dd}`;
    },
    cartTotal() {
      return this.cart.items?.reduce((sum, item) => sum + (item.product?.price || 0) * item.quantity, 0) || 0;
    }
  },
  async created() {
    // Загружаем профиль сначала, а потом остальные данные, чтобы правильно отфильтровать отзывы
    await this.fetchProfile();
    await Promise.all([
      this.fetchPets(),
      this.fetchCart(),
      this.fetchAllProducts(),
      this.fetchMyReviews()
    ]);
  },
  methods: {
    showToast(text, type = 'success') {
      this.toastMessage = text;
      this.toastType = type;
      setTimeout(() => { this.toastMessage = ''; }, 3000);
    },

    // Улучшенный парсинг ошибок с обработкой сетевых и 5xx
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

    translateGender(g) { if (g === 'male') return 'Мужской'; if (g === 'female') return 'Женский'; return ''; },
    translateReviewStatus(status) {
      const map = { pending: 'На модерации', approved: 'Одобрен', rejected: 'Отклонён' };
      return map[status] || status;
    },
    getProductName(id) { const p = this.allProducts.find(p => p.id === id); return p ? p.name : null; },

    // Профиль
    async fetchProfile() {
      this.profileLoading = true;
      this.profileError = null;
      try {
        const resp = await userService.getProfile();
        this.profile = resp.data;
      } catch (e) {
        this.profileError = this.parseApiError(e);
        this.showToast(this.profileError, 'error');
      } finally {
        this.profileLoading = false;
      }
    },
    async saveProfile() {
      if (!this.profile) return;
      this.saving = true;
      this.saveError = null;
      try {
        await userService.updateProfile({ name: this.profile.name, phone: this.profile.phone, email: this.profile.email });
        this.showToast('Профиль обновлён', 'success');
      } catch (e) {
        this.saveError = this.parseApiError(e);
        this.showToast(this.saveError, 'error');
      } finally {
        this.saving = false;
      }
    },

    // Питомцы
    async fetchPets() {
      this.petsLoading = true;
      this.petsError = null;
      try {
        const resp = await petService.getMyPets();
        this.pets = resp.data;
      } catch (e) {
        this.petsError = this.parseApiError(e);
      } finally {
        this.petsLoading = false;
      }
    },
    openAddPet() { this.editingPet = null; this.petForm = { name: '', species: '', breed: '', gender: '', birth_date: '', weight: '', color: '', notes: '' }; this.petFormError = null; this.showPetForm = true; },
    openEditPet(pet) {
      this.editingPet = pet;
      this.petForm = { name: pet.name, species: pet.species, breed: pet.breed || '', gender: pet.gender || '', birth_date: pet.birth_date || '', weight: pet.weight !== null ? pet.weight : '', color: pet.color || '', notes: pet.notes || '' };
      this.petFormError = null;
      this.showPetForm = true;
    },
    closePetForm() { this.showPetForm = false; this.editingPet = null; },
    async savePet() {
      if (!this.petForm.name.trim() || !this.petForm.species.trim()) { this.petFormError = 'Кличка и вид обязательны.'; return; }
      if (this.petForm.birth_date) {
        const birthDate = new Date(this.petForm.birth_date);
        const today = new Date(); today.setHours(0,0,0,0);
        if (birthDate > today) { this.petFormError = 'Дата рождения не может быть в будущем.'; return; }
      }
      this.petSaving = true;
      this.petFormError = null;
      const payload = {
        name: this.petForm.name.trim(), species: this.petForm.species.trim(), breed: this.petForm.breed.trim() || null,
        gender: this.petForm.gender || null, birth_date: this.petForm.birth_date || null,
        weight: this.petForm.weight ? parseFloat(this.petForm.weight) : null, color: this.petForm.color.trim() || null,
        notes: this.petForm.notes.trim() || null,
      };
      try {
        if (this.editingPet) await petService.updatePet(this.editingPet.id, payload);
        else await petService.createPet(payload);
        this.closePetForm();
        await this.fetchPets();
        this.showToast(this.editingPet ? 'Питомец обновлён' : 'Питомец добавлен', 'success');
      } catch (e) {
        this.petFormError = this.parseApiError(e);
        this.showToast(this.petFormError, 'error');
      } finally {
        this.petSaving = false;
      }
    },
    async deletePet(id) {
      // Убираем confirm, удаляем сразу
      try {
        await petService.deletePet(id);
        await this.fetchPets();
        this.showToast('Питомец удалён', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },

    // Корзина
    async fetchCart() {
      this.cartLoading = true;
      this.cartError = null;
      try {
        const resp = await cartService.getCart();
        this.cart = resp.data;
      } catch (e) {
        this.cartError = this.parseApiError(e);
      } finally {
        this.cartLoading = false;
      }
    },
    async fetchAllProducts() {
      try {
        const resp = await productService.getProducts();
        this.allProducts = resp.data.products || resp.data;
      } catch (e) {
        console.warn('Не удалось загрузить товары', e);
      }
    },
    async updateCartItem(itemId, qty) {
      if (qty < 1) return;
      try {
        await cartService.updateItem(itemId, qty);
        await this.fetchCart();
        this.showToast('Количество обновлено', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },
    async removeCartItem(itemId) {
      try {
        await cartService.removeItem(itemId);
        await this.fetchCart();
        this.showToast('Товар удалён', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    },
    async createOrder() {
      if (!this.cart.items?.length) { this.showToast('Корзина пуста', 'error'); return; }
      this.orderCreating = true;
      try {
        await orderService.createOrder();
        await this.fetchCart();
        this.showToast('Заказ оформлен!', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      } finally {
        this.orderCreating = false;
      }
    },

    // Отзывы
    async submitReview() {
      this.reviewSubmitError = null;
      if (!this.newReview.rating) { this.reviewSubmitError = 'Выберите оценку.'; return; }
      this.reviewSubmitting = true;
      try {
        await reviewService.createReview({ rating: parseInt(this.newReview.rating), comment: this.newReview.comment || '' });
        this.showToast('Отзыв отправлен на модерацию', 'success');
        this.newReview = { rating: '', comment: '' };
        await this.fetchMyReviews();
      } catch (e) {
        this.reviewSubmitError = this.parseApiError(e);
        this.showToast(this.reviewSubmitError, 'error');
      } finally {
        this.reviewSubmitting = false;
      }
    },
    async fetchMyReviews() {
      this.reviewsLoading = true;
      this.reviewsError = null;
      try {
        const resp = await reviewService.getReviews();
        const all = resp.data.reviews || resp.data;
        // Фильтруем по user_id, только если профиль уже загружен
        if (this.profile && this.profile.id) {
          this.myReviews = all.filter(r => r.user_id === this.profile.id);
        } else {
          this.myReviews = [];
        }
      } catch (e) {
        this.reviewsError = this.parseApiError(e);
        this.showToast(this.reviewsError, 'error');
      } finally {
        this.reviewsLoading = false;
      }
    },
    async deleteMyReview(id) {
      // Убираем confirm, удаляем сразу
      try {
        await reviewService.deleteReview(id);
        this.myReviews = this.myReviews.filter(r => r.id !== id);
        this.showToast('Отзыв удалён', 'success');
      } catch (e) {
        this.showToast(this.parseApiError(e), 'error');
      }
    }
  }
};
</script>

<style scoped>
.error-text { color: #e53e3e; margin-top: 0.5rem; }
.toast { position: fixed; top: 20px; right: 20px; z-index: 1000; padding: 12px 20px; border-radius: 12px; background: #323232; color: white; font-weight: 500; box-shadow: 0 4px 12px rgba(0,0,0,0.15); animation: fadeIn 0.3s ease; }
.toast.success { background: #2b7e3a; }
.toast.error { background: #c62828; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
.full-width { grid-column: span 2; }
@media (max-width: 640px) { .full-width { grid-column: span 1; } }
</style>