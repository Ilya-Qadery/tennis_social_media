import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { courtsApi } from '@/api/courts';
import { useUIStore } from '@/store/uiStore';

export const useCourts = (filters?: Parameters<typeof courtsApi.getCourts>[0]) => {
  return useQuery({
    queryKey: ['courts', filters],
    queryFn: () => courtsApi.getCourts(filters),
  });
};

export const useCourt = (id: string) => {
  return useQuery({
    queryKey: ['court', id],
    queryFn: () => courtsApi.getCourt(id),
    enabled: !!id,
  });
};

export const useCities = () => {
  return useQuery({
    queryKey: ['cities'],
    queryFn: courtsApi.getCities,
  });
};

export const useCourtReviews = (courtId: string) => {
  return useQuery({
    queryKey: ['courtReviews', courtId],
    queryFn: () => courtsApi.getReviews(courtId),
    enabled: !!courtId,
  });
};

export const useCreateReview = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: ({ courtId, rating, comment }: { courtId: string; rating: number; comment?: string }) =>
      courtsApi.createReview(courtId, rating, comment),
    onSuccess: (_, { courtId }) => {
      queryClient.invalidateQueries({ queryKey: ['courtReviews', courtId] });
      queryClient.invalidateQueries({ queryKey: ['court', courtId] });
      addToast('success', 'نظر شما با موفقیت ثبت شد');
    },
    onError: () => {
      addToast('error', 'خطا در ثبت نظر');
    },
  });
};