import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { matchesApi } from '@/api/matches';
import { useUIStore } from '@/store/uiStore';

export const useMatches = (filters?: Parameters<typeof matchesApi.getMatches>[0]) => {
  return useQuery({
    queryKey: ['matches', filters],
    queryFn: () => matchesApi.getMatches(filters),
  });
};

export const useAvailableMatches = () => {
  return useQuery({
    queryKey: ['matches', 'available'],
    queryFn: matchesApi.getAvailableMatches,
  });
};

export const useMatch = (id: string) => {
  return useQuery({
    queryKey: ['match', id],
    queryFn: () => matchesApi.getMatch(id),
    enabled: !!id,
  });
};

export const useCreateMatch = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: matchesApi.createMatch,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['matches'] });
      addToast('success', 'مسابقه با موفقیت ایجاد شد');
    },
    onError: () => {
      addToast('error', 'خطا در ایجاد مسابقه');
    },
  });
};

export const useJoinMatch = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: matchesApi.joinMatch,
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['matches'] });
      queryClient.invalidateQueries({ queryKey: ['match', id] });
      addToast('success', 'شما با موفقیت به مسابقه پیوستید');
    },
    onError: () => {
      addToast('error', 'خطا در پیوستن به مسابقه');
    },
  });
};

export const useMatchStats = () => {
  return useQuery({
    queryKey: ['matchStats'],
    queryFn: matchesApi.getStats,
  });
};