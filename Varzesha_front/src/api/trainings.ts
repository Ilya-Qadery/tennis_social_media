import { apiClient } from './client';
import type { Drill, TrainingSession, TrainingGoal, TrainingStats } from '@/types';

export const trainingsApi = {
  // Drills
  getDrills: async (filters?: { category?: string; difficulty?: string }): Promise<Drill[]> => {
    const { data } = await apiClient.get('/trainings/drills/', { params: filters });
    return data;
  },

  getDrill: async (id: string): Promise<Drill> => {
    const { data } = await apiClient.get(`/trainings/drills/${id}/`);
    return data;
  },

  createDrill: async (data: Partial<Drill>): Promise<Drill> => {
    const response = await apiClient.post('/trainings/drills/create/', data);
    return response.data;
  },

  // Sessions
  getSessions: async (filters?: { date_from?: string; date_to?: string }): Promise<TrainingSession[]> => {
    const { data } = await apiClient.get('/trainings/sessions/', { params: filters });
    return data;
  },

  getSession: async (id: string): Promise<TrainingSession> => {
    const { data } = await apiClient.get(`/trainings/sessions/${id}/`);
    return data;
  },

  createSession: async (data: Partial<TrainingSession>): Promise<TrainingSession> => {
    const response = await apiClient.post('/trainings/sessions/create/', data);
    return response.data;
  },

  updateSession: async (id: string, data: Partial<TrainingSession>): Promise<TrainingSession> => {
    const response = await apiClient.patch(`/trainings/sessions/${id}/`, data);
    return response.data;
  },

  deleteSession: async (id: string): Promise<void> => {
    await apiClient.delete(`/trainings/sessions/${id}/`);
  },

  addDrillToSession: async (sessionId: string, drillData: any): Promise<any> => {
    const { data } = await apiClient.post(`/trainings/sessions/${sessionId}/drills/`, drillData);
    return data;
  },

  removeDrillFromSession: async (sessionId: string, drillInstanceId: string): Promise<void> => {
    await apiClient.delete(`/trainings/sessions/${sessionId}/drills/${drillInstanceId}/`);
  },

  getTrainingStats: async (): Promise<TrainingStats> => {
    const { data } = await apiClient.get('/trainings/sessions/stats/');
    return data;
  },

  // Goals
  getGoals: async (filters?: { status?: string }): Promise<TrainingGoal[]> => {
    const { data } = await apiClient.get('/trainings/goals/', { params: filters });
    return data;
  },

  getGoal: async (id: string): Promise<TrainingGoal> => {
    const { data } = await apiClient.get(`/trainings/goals/${id}/`);
    return data;
  },

  createGoal: async (data: Partial<TrainingGoal>): Promise<TrainingGoal> => {
    const response = await apiClient.post('/trainings/goals/create/', data);
    return response.data;
  },

  updateGoal: async (id: string, data: Partial<TrainingGoal>): Promise<TrainingGoal> => {
    const response = await apiClient.patch(`/trainings/goals/${id}/`, data);
    return response.data;
  },

  updateGoalProgress: async (id: string, increment: number = 1): Promise<TrainingGoal> => {
    const { data } = await apiClient.post(`/trainings/goals/${id}/progress/`, { increment });
    return data;
  },
};