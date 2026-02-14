import React, { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { useTrainingStats, useGoals, useSessions } from '@/hooks/useTrainings';
import { toPersianNumber } from '@/utils/persian';
import { Trophy, Target, Calendar, ChevronLeft } from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export const Training = () => {
  const navigate = useNavigate();
  const { data: stats } = useTrainingStats();
  const { data: goals } = useGoals();
  const { data: sessions } = useSessions();

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <Header title="تمرینات" />

      <main className="p-4 space-y-4">
        {/* Stats Overview */}
        <div className="grid grid-cols-2 gap-3">
          <Card className="bg-gradient-to-br from-primary-500 to-primary-600 text-white">
            <Trophy className="mb-2 opacity-80" size={24} />
            <p className="text-2xl font-bold">{toPersianNumber(stats?.total_sessions || 0)}</p>
            <p className="text-sm opacity-80">جلسه تمرین</p>
          </Card>
          <Card className="bg-gradient-to-br from-accent-500 to-accent-600 text-white">
            <Calendar className="mb-2 opacity-80" size={24} />
            <p className="text-2xl font-bold">{toPersianNumber(stats?.this_week_sessions || 0)}</p>
            <p className="text-sm opacity-80">این هفته</p>
          </Card>
        </div>

        {/* Active Goals */}
        <section>
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-lg font-bold text-gray-900">اهداف فعال</h3>
            <button
              onClick={() => navigate('/training/goals')}
              className="text-sm text-primary-600"
            >
              مشاهده همه
            </button>
          </div>

          <div className="space-y-3">
            {goals?.filter(g => g.status === 'active').map((goal) => (
              <Card key={goal.id}>
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <Target size={20} className="text-primary-500" />
                    <span className="font-bold text-gray-900">{goal.title}</span>
                  </div>
                  <span className="text-sm font-medium text-primary-600">
                    {toPersianNumber(goal.progress_percentage)}٪
                  </span>
                </div>
                <ProgressBar progress={goal.progress_percentage} />
                <p className="mt-2 text-xs text-gray-500">
                  {toPersianNumber(goal.current_value)} از {toPersianNumber(goal.target_value)}
                </p>
              </Card>
            ))}

            {(!goals || goals.filter(g => g.status === 'active').length === 0) && (
              <Card className="text-center py-6">
                <p className="text-gray-500 mb-3">هدف فعالی ندارید</p>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/training/goals/create')}
                >
                  تعیین هدف جدید
                </Button>
              </Card>
            )}
          </div>
        </section>

        {/* Recent Sessions */}
        <section>
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-lg font-bold text-gray-900">تمرینات اخیر</h3>
            <button
              onClick={() => navigate('/training/sessions')}
              className="text-sm text-primary-600"
            >
              مشاهده همه
            </button>
          </div>

          <div className="space-y-3">
            {sessions?.slice(0, 3).map((session) => (
              <motion.div
                key={session.id}
                whileTap={{ scale: 0.98 }}
                onClick={() => navigate(`/training/sessions/${session.id}`)}
              >
                <Card className="cursor-pointer">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-bold text-gray-900">{session.title || 'تمرین'}</p>
                      <p className="text-sm text-gray-500">
                        {toPersianNumber(session.duration_minutes)} دقیقه • {session.intensity_display}
                      </p>
                    </div>
                    <ChevronLeft size={20} className="text-gray-400" />
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Quick Action */}
        <Button
          fullWidth
          size="lg"
          onClick={() => navigate('/training/sessions/create')}
          className="mt-4"
        >
          ثبت تمرین جدید
        </Button>
      </main>
    </div>
  );
};