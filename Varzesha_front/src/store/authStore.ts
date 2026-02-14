import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, AuthTokens } from '@/types';
import { authApi } from '@/api/auth';

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (phone: string, password: string) => Promise<void>;
  register: (data: { phone: string; password: string; first_name?: string; last_name?: string }) => Promise<void>;
  verifyPhone: (phone: string, code: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
  updateUser: (data: Partial<User>) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (phone, password) => {
        set({ isLoading: true });
        try {
          const response = await authApi.login({ phone, password });
          localStorage.setItem('access_token', response.access);
          localStorage.setItem('refresh_token', response.refresh);
          set({
            user: response,
            tokens: { access: response.access, refresh: response.refresh },
            isAuthenticated: true
          });
        } finally {
          set({ isLoading: false });
        }
      },

      register: async (data) => {
        set({ isLoading: true });
        try {
          const response = await authApi.register(data);
          localStorage.setItem('access_token', response.access);
          localStorage.setItem('refresh_token', response.refresh);
          set({
            user: response,
            tokens: { access: response.access, refresh: response.refresh },
            isAuthenticated: true
          });
        } finally {
          set({ isLoading: false });
        }
      },

      verifyPhone: async (phone, code) => {
        set({ isLoading: true });
        try {
          const response = await authApi.verifyPhone(phone, code);
          localStorage.setItem('access_token', response.access);
          localStorage.setItem('refresh_token', response.refresh);
          set({
            user: response,
            tokens: { access: response.access, refresh: response.refresh },
            isAuthenticated: true
          });
        } finally {
          set({ isLoading: false });
        }
      },

      logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        set({ user: null, tokens: null, isAuthenticated: false });
      },

      setUser: (user) => set({ user, isAuthenticated: true }),

      updateUser: async (data) => {
        const updated = await authApi.updateMe(data);
        set({ user: updated });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
);