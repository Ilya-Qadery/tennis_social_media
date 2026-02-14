import React from 'react';
import { motion } from 'framer-motion';
import { Header } from '@/components/layout/Header';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { StreakCounter } from '@/components/ui/StreakCounter';
import { useAuthStore } from '@/store/authStore';
import { useMatchStats } from '@/hooks/useMatches';
import { toPersianNumber } from '@/utils/persian';
import {
  User,
  Settings,
  Trophy,
  Calendar,
  MapPin,
  ChevronLeft,
  LogOut
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Profile = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const { data: stats } = useMatchStats();

  const menuItems = [
    { icon: User, label: 'ویرایش پروفایل', path: '/profile/edit' },
    { icon: Trophy, label: 'دستاوردها', path: '/profile/achievements' },
    { icon: Calendar, label: 'تقویم مسابقات', path: '/profile/calendar' },
    { icon: MapPin, label: 'زمین‌های مورد علاقه', path: '/profile/favorites' },
    { icon: Settings, label: 'تنظیمات', path: '/settings' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <Header title="پروفایل" />

      <main className="p-4 space-y-4">
        {/* Profile Header */}
        <Card className="relative overflow-hidden">
          <div className="absolute inset-0 h-24 bg-gradient-to-r from-primary-500 to-primary-600" />

          <div className="relative pt-12">
            <div className="flex flex-col items-center">
              <div className="h-24 w-24 rounded-full border-4 border-white bg-gray-200 flex items-center justify-center text-3xl font-bold text-gray-400">
                {user?.first_name?.[0] || user?.phone?.[0]}
              </div>

              <h2 className="mt-3 text-xl font-bold text-gray-900">
                {user?.full_name || user?.phone}
              </h2>
              <p className="text-sm text-gray-500">{user?.phone}</p>

              <div className="mt-3 flex gap-2">
                <StreakCounter count={7} size="sm" />
              </div>
            </div>

            {/* Stats Row */}
            <div className="mt-6 grid grid-cols-3 gap-4 border-t border-gray-100 pt-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-gray-900">
                  {toPersianNumber(stats?.total_matches || 0)}
                </p>
                <p className="text-xs text-gray-500">مسابقه</p>
              </div>
              <div className="text-center border-x border-gray-100">
                <p className="text-2xl font-bold text-primary-600">
                  {toPersianNumber(stats?.win_rate || 0)}٪
                </p>
                <p className="text-xs text-gray-500">برد</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-accent-500">
                  {toPersianNumber(stats?.won || 0)}
                </p>
                <p className="text-xs text-gray-500">پیروزی</p>
              </div>
            </div>
          </div>
        </Card>

        {/* Level Progress */}
        <Card>
          <div className="flex items-center justify-between mb-2">
            <span className="font-bold text-gray-900">سطح بازیکن</span>
            <span className="text-sm text-primary-600">ماهر (B)</span>
          </div>
          <ProgressBar progress={75} color="primary" />
          <p className="mt-2 text-xs text-gray-500">
            {toPersianNumber(250)} امتیاز تا سطح بعدی
          </p>
        </Card>

        {/* Menu */}
        <Card className="p-2">
          {menuItems.map((item, index) => (
            <motion.button
              key={item.path}
              className={`flex w-full items-center justify-between p-3 text-right ${
                index !== menuItems.length - 1 ? 'border-b border-gray-100' : ''
              }`}
              whileTap={{ scale: 0.98 }}
              onClick={() => navigate(item.path)}
            >
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-gray-100 p-2 text-gray-600">
                  <item.icon size={20} />
                </div>
                <span className="font-medium text-gray-900">{item.label}</span>
              </div>
              <ChevronLeft size={20} className="text-gray-400" />
            </motion.button>
          ))}
        </Card>

        {/* Logout */}
        <Button
          variant="ghost"
          fullWidth
          className="text-red-500 hover:bg-red-50"
          onClick={() => {
            logout();
            navigate('/login');
          }}
        >
          <LogOut size={18} />
          خروج از حساب
        </Button>
      </main>
    </div>
  );
};