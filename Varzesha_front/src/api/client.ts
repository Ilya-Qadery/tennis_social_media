import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { jwtDecode } from 'jwt-decode';
import { useAuthStore } from '@/store/authStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Token refresh logic
let isRefreshing = false;
let refreshSubscribers: ((token: string) => void)[] = [];

const subscribeTokenRefresh = (callback: (token: string) => void) => {
  refreshSubscribers.push(callback);
};

const onTokenRefreshed = (token: string) => {
  refreshSubscribers.forEach((callback) => callback(token));
  refreshSubscribers = [];
};

const refreshToken = async (): Promise<string | null> => {
  try {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return null;

    const response = await axios.post(`${API_BASE_URL}/users/auth/refresh/`, {
      refresh,
    });

    const { access } = response.data;
    localStorage.setItem('access_token', access);
    return access;
  } catch (error) {
    return null;
  }
};

// Request interceptor
apiClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');

    if (token) {
      try {
        const decoded: any = jwtDecode(token);
        const currentTime = Date.now() / 1000;

        // Token expired, try to refresh
        if (decoded.exp < currentTime) {
          if (!isRefreshing) {
            isRefreshing = true;
            const newToken = await refreshToken();
            isRefreshing = false;

            if (newToken) {
              onTokenRefreshed(newToken);
              config.headers.Authorization = `Bearer ${newToken}`;
            } else {
              // Refresh failed, logout
              useAuthStore.getState().logout();
              window.location.href = '/login';
            }
          } else {
            // Wait for refresh
            return new Promise((resolve) => {
              subscribeTokenRefresh((newToken) => {
                config.headers.Authorization = `Bearer ${newToken}`;
                resolve(config);
              });
            });
          }
        } else {
          config.headers.Authorization = `Bearer ${token}`;
        }
      } catch (error) {
        console.error('Token decode error:', error);
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const newToken = await refreshToken();
      if (newToken) {
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return apiClient(originalRequest);
      } else {
        useAuthStore.getState().logout();
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);