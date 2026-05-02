import { reactive } from 'vue';
import authService from '@/services/authService';

// Ключи для localStorage
const TOKEN_KEY = 'access_token';
const REFRESH_KEY = 'refresh_token';

function saveTokens(access, refresh) {
  localStorage.setItem(TOKEN_KEY, access);
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

// Реактивное состояние
export const authState = reactive({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
});

// ===== Действия =====

export async function login(credentials) {
  authState.isLoading = true;
  authState.error = null;
  try {
    const response = await authService.login(credentials);
    const { access_token, refresh_token, user } = response.data;
    saveTokens(access_token, refresh_token);
    authState.user = user;
    authState.isAuthenticated = true;
  } catch (err) {
    authState.error = err.response?.data?.detail || 'Ошибка входа';
    throw err;
  } finally {
    authState.isLoading = false;
  }
}

export async function register(data) {
  authState.isLoading = true;
  authState.error = null;
  try {
    const response = await authService.register(data);
    const { access_token, refresh_token, user } = response.data;
    saveTokens(access_token, refresh_token);
    authState.user = user;
    authState.isAuthenticated = true;
  } catch (err) {
    authState.error = err.response?.data?.detail || 'Ошибка регистрации';
    throw err;
  } finally {
    authState.isLoading = false;
  }
}

export async function logout() {
  const refresh = localStorage.getItem(REFRESH_KEY);
  try {
    if (refresh) await authService.logout(refresh);
  } catch {
    // не критично
  }
  clearTokens();
  authState.user = null;
  authState.isAuthenticated = false;
}

export async function fetchProfile() {
  try {
    const resp = await authService.getProfile();
    authState.user = resp.data;
    authState.isAuthenticated = true;
  } catch {
    // Если 401 – интерсептор попробует обновить и повторит, либо разлогинет
    authState.isAuthenticated = false;
  }
}

// Восстановление сессии при запуске
export async function initAuth() {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    await fetchProfile();  // если токен валиден, isAuthenticated станет true
  }
}