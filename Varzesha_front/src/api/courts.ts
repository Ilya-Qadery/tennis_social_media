import { apiClient } from './client';
import type { Court, CourtReview } from '@/types';

interface CourtFilters {
  city?: string;
  surface_type?: string;
  indoor?: boolean;
  has_lights?: boolean;
  min_price?: number;
  max_price?: number;
  min_rating?: number;
  has_parking?: boolean;
  has_showers?: boolean;
  search?: string;
}

export const courtsApi = {
  getCourts: async (filters?: CourtFilters): Promise<Court[]> => {
    const { data } = await apiClient.get('/courts/', { params: filters });
    return data;
  },

  getCourt: async (id: string): Promise<Court> => {
    const { data } = await apiClient.get(`/courts/${id}/`);
    return data;
  },

  getCities: async (): Promise<string[]> => {
    const { data } = await apiClient.get('/courts/cities/');
    return data.cities;
  },

  getReviews: async (courtId: string): Promise<CourtReview[]> => {
    const { data } = await apiClient.get(`/courts/${courtId}/reviews/`);
    return data;
  },

  createReview: async (courtId: string, rating: number, comment?: string): Promise<CourtReview> => {
    const { data } = await apiClient.post(`/courts/${courtId}/reviews/`, {
      rating,
      comment,
    });
    return data;
  },
};