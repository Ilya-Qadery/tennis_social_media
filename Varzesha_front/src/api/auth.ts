import { apiClient } from './client';
import type {
  LoginCredentials,
  RegisterData,
  AuthResponse,
  User
} from '@/types';

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const { data } = await apiClient.post('/users/auth/login/', credentials);
    return data;
  },

  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await apiClient.post('/users/auth/register/', data);
    return response.data;
  },

  sendVerificationCode: async (phone: string): Promise<void> => {
    await apiClient.post('/users/auth/send-code/', { phone });
  },

  verifyPhone: async (phone: string, code: string): Promise<AuthResponse> => {
    const { data } = await apiClient.post('/users/auth/verify/', { phone, code });
    return data;
  },

  getMe: async (): Promise<User> => {
    const { data } = await apiClient.get('/users/me/');
    return data;
  },

  updateMe: async (data: Partial<User>): Promise<User> => {
    const response = await apiClient.patch('/users/me/', data);
    return response.data;
  },

  changePassword: async (oldPassword: string, newPassword: string): Promise<void> => {
    await apiClient.post('/users/me/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
      confirm_password: newPassword,
    });
  },
};