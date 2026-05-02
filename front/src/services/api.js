import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
});

// ---- интерсептор запросов: цепляем токен ----
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ---- интерсептор ответов: рефреш при 401 ----
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const resp = await axios.post(
            `${apiClient.defaults.baseURL}/auth/refresh`,
            { refresh_token: refreshToken }
          );
          const { access_token, refresh_token } = resp.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return apiClient(originalRequest);
        } catch (refreshError) {
          // Рефреш провалился — разлогиниваем
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/auth';
          return Promise.reject(refreshError);
        }
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;