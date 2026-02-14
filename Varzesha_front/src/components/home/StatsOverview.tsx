import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Target, Flame, Award } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { StreakCounter } from '@/components/ui/StreakCounter';
import { toPersianNumber } from '@/utils/persian';
import { useMatchStats } from '@/hooks/useMatches';

export const StatsOverview = () => {
  const { data: stats } = useMatchStats();

  return (
    <div className="space-y-3">
      {/* Streak Banner */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="rounded-2xl bg-gradient-to-r from-orange-500 to-red-500 p-4 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm opacity-90">رکورد پیوسته شما</p>
            <StreakCounter count={7} record={7} size="lg" />
          </div>
          <Flame size={48} className="opacity-30" />
        </div>
        <p className="mt-2 text-xs opacity-80">
          ۳ روز دیگر تا دریافت نشان «پرشور» فاصله دارید!
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-3">
        <Card>
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-primary-100 p-2 text-primary-600">
              <TrendingUp size={20} />
            </div>
            <div>
              <p className="text-xs text-gray-500">بردها</p>
              <p className="text-xl font-bold text-gray-900">
                {toPersianNumber(stats?.won || 0)}
              </p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-accent-100 p-2 text-accent-600">
              <Target size={20} />
            </div>
            <div>
              <p className="text-xs text-gray-500">نرخ برد</p>
              <p className="text-xl font-bold text-gray-900">
                {toPersianNumber(stats?.win_rate || 0)}٪
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Level Progress */}
      <Card>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Award size={20} className="text-reward-500" />
            <span className="font-bold text-gray-900">سطح: بازیکن ماهر</span>
          </div>
          <span className="text-sm text-gray-500">۸۵٪</span>
        </div>
        <ProgressBar progress={85} color="reward" size="sm" />
        <p className="mt-2 text-xs text-gray-500">
          ۳ مسابقه دیگر تا رسیدن به سطح «حرفه‌ای»
        </p>
      </Card>
    </div>
  );
};