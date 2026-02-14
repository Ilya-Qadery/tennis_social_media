import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { trainingsApi } from '@/api/trainings';
import { useUIStore } from '@/store/uiStore';

// Drills
export const useDrills = (filters?: { category?: string; difficulty?: string }) => {
  return useQuery({
    queryKey: ['drills', filters],
    queryFn: () => trainingsApi.getDrills(filters),
  });
};

export const useDrill = (id: string) => {
  return useQuery({
    queryKey: ['drill', id],
    queryFn: () => trainingsApi.getDrill(id),
    enabled: !!id,
  });
};

// Sessions
export const useSessions = (filters?: { date_from?: string; date_to?: string }) => {
  return useQuery({
    queryKey: ['sessions', filters],
    queryFn: () => trainingsApi.getSessions(filters),
  });
};

export const useSession = (id: string) => {
  return useQuery({
    queryKey: ['session', id],
    queryFn: () => trainingsApi.getSession(id),
    enabled: !!id,
  });
};

export const useCreateSession = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: trainingsApi.createSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
      queryClient.invalidateQueries({ queryKey: ['trainingStats'] });
      addToast('success', 'تمرین با موفقیت ثبت شد');
    },
    onError: () => {
      addToast('error', 'خطا در ثبت تمرین');
    },
  });
};

export const useUpdateSession = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof trainingsApi.updateSession>[1] }) =>
      trainingsApi.updateSession(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
      queryClient.invalidateQueries({ queryKey: ['session', id] });
      addToast('success', 'تمرین به‌روزرسانی شد');
    },
    onError: () => {
      addToast('error', 'خطا در به‌روزرسانی');
    },
  });
};

export const useDeleteSession = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: trainingsApi.deleteSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
      queryClient.invalidateQueries({ queryKey: ['trainingStats'] });
      addToast('success', 'تمرین حذف شد');
    },
    onError: () => {
      addToast('error', 'خطا در حذف تمرین');
    },
  });
};

// Training Stats
export const useTrainingStats = () => {
  return useQuery({
    queryKey: ['trainingStats'],
    queryFn: trainingsApi.getTrainingStats,
  });
};

// Goals
export const useGoals = (filters?: { status?: string }) => {
  return useQuery({
    queryKey: ['goals', filters],
    queryFn: () => trainingsApi.getGoals(filters),
  });
};

export const useGoal = (id: string) => {
  return useQuery({
    queryKey: ['goal', id],
    queryFn: () => trainingsApi.getGoal(id),
    enabled: !!id,
  });
};

export const useCreateGoal = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: trainingsApi.createGoal,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['goals'] });
      addToast('success', 'هدف با موفقیت ایجاد شد');
    },
    onError: () => {
      addToast('error', 'خطا در ایجاد هدف');
    },
  });
};

export const useUpdateGoal = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof trainingsApi.updateGoal>[1] }) =>
      trainingsApi.updateGoal(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['goals'] });
      queryClient.invalidateQueries({ queryKey: ['goal', id] });
      addToast('success', 'هدف به‌روزرسانی شد');
    },
    onError: () => {
      addToast('error', 'خطا در به‌روزرسانی هدف');
    },
  });
};

export const useUpdateGoalProgress = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: ({ id, increment }: { id: string; increment?: number }) =>
      trainingsApi.updateGoalProgress(id, increment),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['goals'] });
      queryClient.invalidateQueries({ queryKey: ['goal', id] });
      addToast('success', 'پیشرفت ثبت شد! 🎉');
    },
    onError: () => {
      addToast('error', 'خطا در ثبت پیشرفت');
    },
  });
};

// Training Drills (Session-Drill Link)
export const useAddDrillToSession = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: ({ sessionId, drillData }: { sessionId: string; drillData: any }) =>
      trainingsApi.addDrillToSession(sessionId, drillData),
    onSuccess: (_, { sessionId }) => {
      queryClient.invalidateQueries({ queryKey: ['session', sessionId] });
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
      addToast('success', 'تمرین اضافه شد');
    },
    onError: () => {
      addToast('error', 'خطا در اضافه کردن تمرین');
    },
  });
};

export const useRemoveDrillFromSession = () => {
  const queryClient = useQueryClient();
  const addToast = useUIStore((state) => state.addToast);

  return useMutation({
    mutationFn: ({ sessionId, drillInstanceId }: { sessionId: string; drillInstanceId: string }) =>
      trainingsApi.removeDrillFromSession(sessionId, drillInstanceId),
    onSuccess: (_, { sessionId }) => {
      queryClient.invalidateQueries({ queryKey: ['session', sessionId] });
      addToast('success', 'تمرین حذف شد');
    },
    onError: () => {
      addToast('error', 'خطا در حذف تمرین');
    },
  });
};