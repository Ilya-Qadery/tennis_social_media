import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Header } from '@/components/layout/Header';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { useCreateMatch } from '@/hooks/useMatches';
import { useCourts } from '@/hooks/useCourts';
import { Calendar, Clock, MapPin, Users } from 'lucide-react';

export const CreateMatch = () => {
  const navigate = useNavigate();
  const createMutation = useCreateMatch();
  const { data: courts } = useCourts();

  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    scheduled_at: '',
    duration_minutes: 90,
    court_id: '',
    court_name: '',
    match_type: 'singles' as const,
    is_public: true,
  });

  const handleSubmit = async () => {
    try {
      await createMutation.mutateAsync({
        scheduled_at: formData.scheduled_at,
        duration_minutes: formData.duration_minutes,
        court_id: formData.court_id || undefined,
        court_name: formData.court_name,
        match_type: formData.match_type,
        is_public: formData.is_public,
      });
      navigate('/matches');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <Header title="ایجاد مسابقه" showBack />

      <main className="p-4">
        {/* Progress Steps */}
        <div className="mb-6 flex items-center justify-center gap-2">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`h-2 w-8 rounded-full ${
                s <= step ? 'bg-primary-500' : 'bg-gray-200'
              }`}
            />
          ))}
        </div>

        <motion.div
          key={step}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
        >
          {step === 1 && (
            <Card>
              <h3 className="mb-4 text-lg font-bold">زمان و تاریخ</h3>
              <div className="space-y-4">
                <div>
                  <label className="mb-1 block text-sm font-medium">تاریخ</label>
                  <input
                    type="date"
                    value={formData.scheduled_at.split('T')[0]}
                    onChange={(e) => setFormData({
                      ...formData,
                      scheduled_at: `${e.target.value}T${formData.scheduled_at.split('T')[1] || '18:00'}`
                    })}
                    className="w-full rounded-xl border border-gray-300 p-3"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">ساعت</label>
                  <input
                    type="time"
                    value={formData.scheduled_at.split('T')[1] || '18:00'}
                    onChange={(e) => setFormData({
                      ...formData,
                      scheduled_at: `${formData.scheduled_at.split('T')[0] || new Date().toISOString().split('T')[0]}T${e.target.value}`
                    })}
                    className="w-full rounded-xl border border-gray-300 p-3"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">مدت (دقیقه)</label>
                  <div className="flex gap-2">
                    {[60, 90, 120].map((min) => (
                      <button
                        key={min}
                        onClick={() => setFormData({ ...formData, duration_minutes: min })}
                        className={`flex-1 rounded-xl py-2 text-sm font-medium ${
                          formData.duration_minutes === min
                            ? 'bg-primary-500 text-white'
                            : 'bg-gray-100 text-gray-700'
                        }`}
                      >
                        {min}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </Card>
          )}

          {step === 2 && (
            <Card>
              <h3 className="mb-4 text-lg font-bold">محل برگزاری</h3>
              <div className="space-y-3">
                {courts?.slice(0, 5).map((court) => (
                  <button
                    key={court.id}
                    onClick={() => setFormData({ ...formData, court_id: court.id })}
                    className={`w-full rounded-xl border-2 p-3 text-right ${
                      formData.court_id === court.id
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-200'
                    }`}
                  >
                    <p className="font-bold">{court.name}</p>
                    <p className="text-sm text-gray-500">{court.city}</p>
                  </button>
                ))}
                <div className="relative">
                  <input
                    type="text"
                    placeholder="یا نام زمین را وارد کنید"
                    value={formData.court_name}
                    onChange={(e) => setFormData({ ...formData, court_name: e.target.value })}
                    className="w-full rounded-xl border border-gray-300 p-3"
                  />
                </div>
              </div>
            </Card>
          )}

          {step === 3 && (
            <Card>
              <h3 className="mb-4 text-lg font-bold">تنظیمات نهایی</h3>
              <div className="space-y-4">
                <div>
                  <label className="mb-2 block text-sm font-medium">نوع مسابقه</label>
                  <div className="flex gap-2">
                    {[
                      { id: 'singles', label: 'تک‌نفره' },
                      { id: 'doubles', label: 'دو نفره' }
                    ].map((type) => (
                      <button
                        key={type.id}
                        onClick={() => setFormData({ ...formData, match_type: type.id as any })}
                        className={`flex-1 rounded-xl py-2 text-sm font-medium ${
                          formData.match_type === type.id
                            ? 'bg-primary-500 text-white'
                            : 'bg-gray-100 text-gray-700'
                        }`}
                      >
                        {type.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between rounded-xl bg-gray-50 p-3">
                  <span className="text-sm font-medium">عمومی (قابل مشاهده برای همه)</span>
                  <button
                    onClick={() => setFormData({ ...formData, is_public: !formData.is_public })}
                    className={`relative h-6 w-11 rounded-full ${
                      formData.is_public ? 'bg-primary-500' : 'bg-gray-300'
                    }`}
                  >
                    <span
                      className={`absolute top-1 h-4 w-4 rounded-full bg-white transition-all ${
                        formData.is_public ? 'right-1' : 'left-1'
                      }`}
                    />
                  </button>
                </div>
              </div>
            </Card>
          )}
        </motion.div>

        {/* Navigation Buttons */}
        <div className="mt-6 flex gap-3">
          {step > 1 && (
            <Button
              variant="outline"
              className="flex-1"
              onClick={() => setStep(step - 1)}
            >
              قبلی
            </Button>
          )}
          {step < 3 ? (
            <Button
              className="flex-1"
              onClick={() => setStep(step + 1)}
            >
              بعدی
            </Button>
          ) : (
            <Button
              className="flex-1"
              onClick={handleSubmit}
              isLoading={createMutation.isPending}
              dopamineTrigger
            >
              ایجاد مسابقه
            </Button>
          )}
        </div>
      </main>
    </div>
  );
};