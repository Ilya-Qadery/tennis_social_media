import { apiClient } from './client';
import type { Match, MatchStats } from '@/types';

interface MatchFilters {
  status?: string;
  upcoming?: boolean;
  past?: boolean;
}

interface CreateMatchData {
  title?: string;
  description?: string;
  scheduled_at: string;
  duration_minutes?: number;
  court_id?: string;
  court_name?: string;
  match_type?: 'singles' | 'doubles';
  ntrp_min?: number;
  ntrp_max?: number;
  is_public?: boolean;
}

export const matchesApi = {
  getMatches: async (filters?: MatchFilters): Promise<Match[]> => {
    const { data } = await apiClient.get('/matches/', { params: filters });
    return data;
  },

  getAvailableMatches: async (): Promise<Match[]> => {
    const { data } = await apiClient.get('/matches/available/');
    return data;
  },

  getMatch: async (id: string): Promise<Match> => {
    const { data } = await apiClient.get(`/matches/${id}/`);
    return data;
  },

  createMatch: async (data: CreateMatchData): Promise<Match> => {
    const response = await apiClient.post('/matches/create/', data);
    return response.data;
  },

  joinMatch: async (id: string): Promise<Match> => {
    const { data } = await apiClient.post(`/matches/${id}/join/`);
    return data;
  },

  leaveMatch: async (id: string): Promise<Match> => {
    const { data } = await apiClient.post(`/matches/${id}/leave/`);
    return data;
  },

  cancelMatch: async (id: string, reason?: string): Promise<Match> => {
    const { data } = await apiClient.post(`/matches/${id}/cancel/`, { reason });
    return data;
  },

  recordScore: async (
    id: string,
    organizerScore: number,
    opponentScore: number,
    setScores?: number[][]
  ): Promise<Match> => {
    const { data } = await apiClient.post(`/matches/${id}/score/`, {
      organizer_score: organizerScore,
      opponent_score: opponentScore,
      set_scores: setScores,
    });
    return data;
  },

  getStats: async (): Promise<MatchStats> => {
    const { data } = await apiClient.get('/matches/stats/');
    return data;
  },
};