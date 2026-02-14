// src/pages/Home.tsx - REDESIGNED WITH DOPAMINE TRIGGERS
import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
  Zap, Trophy, Target, TrendingUp, Users,
  ChevronLeft, Flame, Star, MapPin
} from 'lucide-react';
import { Header } from '@/components/layout/Header';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { StreakCounter } from '@/components/ui/StreakCounter';
import { Badge } from '@/components/ui/Badge';
import { useMatches } from '@/hooks/useMatches';
import { useMatchStats } from '@/hooks/useMatches';
import { useAuthStore } from '@/store/authStore';
import {
  toPersianNumber,
  getPersianGreeting,
  formatPersianDate
} from '@/utils/persian';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: 'spring', stiffness: 300, damping: 24 }
  }
};

export const Home = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const { data: upcomingMatches } = useMatches({ upcoming: true });
  const { data: stats } = useMatchStats();

  const quickActions = [
    {
      id: 'find-opponent',
      title: 'رقیب‌یابی',
      subtitle: 'حریف هم‌سطح در ۲ دقیقه',
      icon: Users,
      color: 'from-primary-500 to-primary-600',
      path: '/matches/available',
      badge: '۵ بازیکن فعال',
      dopamine: true,
    },
    {
      id: 'find-court',
      title: 'یافتن زمین',
      subtitle: 'بهترین زمین‌های نزدیک',
      icon: MapPin,
      color: 'from-trust-500 to-trust-600',
      path: '/courts',
    },
    {
      id: 'my-matches',
      title: 'مسابقات من',
      subtitle: 'مشاهده و مدیریت',
      icon: Trophy,
      color: 'from-accent-500 to-accent-600',
      path: '/matches',
      badge: stats?.total_matches ? `${toPersianNumber(stats.total_matches)} بازی` : undefined,
    },
    {
      id: 'training',
      title: 'تمرینات',
      subtitle: 'برنامه‌ریزی هدفمند',
      icon: Target,
      color: 'from-purple-500 to-purple-600',
      path: '/training',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <Header />

      <motion.main
        className="space-y-6 p-4"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Hero Section - Personalization + Context */}
        <motion.section
          variants={itemVariants}
          className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-500 via-primary-600 to-primary-700 p-6 text-white shadow-glow"
        >
          {/* Animated Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <motion.div
              className="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-white/10"
              animate={{ scale: [1, 1.2, 1], rotate: [0, 90, 0] }}
              transition={{ duration: 8, repeat: Infinity }}
            />
            <motion.div
              className="absolute -bottom-10 -left-10 h-32 w-32 rounded-full bg-white/10"
              animate={{ scale: [1, 1.3, 1], rotate: [0, -90, 0] }}
              transition={{ duration: 10, repeat: Infinity }}
            />
          </div>

          <div className="relative">
            <div className="flex items-start justify-between">
              <div>
                <motion.p
                  className="text-primary-100 text-sm"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  {getPersianGreeting()}، {user?.first_name || 'قهرمان'}! 👋
                </motion.p>
                <motion.h2
                  className="mt-1 text-2xl font-black"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  آماده بازی هستی؟
                </motion.h2>
                <motion.p
                  className="mt-2 text-sm text-primary-100"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  امروز ۲۲ درجه، هوای عالی برای تنیس! ☀️
                </motion.p>
              </div>

              {/* Streak Badge - Loss Aversion Trigger */}
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 500, delay: 0.6 }}
                className="rounded-2xl bg-white/20 p-3 backdrop-blur-sm"
              >
                <div className="flex items-center gap-1">
                  <Flame className="text-orange-300" size={20} fill="currentColor" />
                  <span className="font-bold">۷</span>
                </div>
                <p className="text-xs text-primary-100">روز متوالی</p>
              </motion.div>
            </div>

            {/* Quick Start Buttons - Fogg's Ability Principle */}
            <motion.div
              className="mt-6 flex gap-3"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
            >
              <Button
                variant="secondary"
                className="flex-1 bg-white text-primary-700 hover:bg-gray-100 shadow-lg"
                onClick={() => navigate('/matches/create')}
                leftIcon={<Zap size={18} className="text-accent-500" />}
              >
                شروع سریع
              </Button>
              <Button
                variant="outline"
                className="flex-1 border-2 border-white/50 text-white hover:bg-white/10"
                onClick={() => navigate('/courts')}
              >
                یافتن زمین
              </Button>
            </motion.div>
          </div>
        </motion.section>

        {/* Level Progress - Completion Bias */}
        <motion.section variants={itemVariants}>
          <Card className="border-l-4 border-l-reward-400">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="rounded-xl bg-reward-100 p-2">
                  <Star className="text-reward-500" size={20} fill="currentColor" />
                </div>
                <div>
                  <p className="font-bold text-gray-900">سطح: بازیکن ماهر</p>
                  <p className="text-xs text-gray-500">۸۵٪ پیشرفت</p>
                </div>
              </div>
              <Badge variant="gold" pulse>۲۵۰ XP تا سطح بعد</Badge>
            </div>
            <ProgressBar progress={85} color="reward" animated />
            <p className="mt-2 text-xs text-gray-500">
              ۳ مسابقه دیگر تا رسیدن به سطح «حرفه‌ای» و باز کردن زمین‌های VIP! 🏆
            </p>
          </Card>
        </motion.section>

        {/* Quick Actions - 2x2 Grid with Dopamine Triggers */}
        <motion.section variants={itemVariants}>
          <h3 className="mb-3 text-lg font-bold text-gray-900 flex items-center gap-2">
            دسترسی سریع
            <motion.span
              animate={{ rotate: [0, 15, -15, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              ⚡
            </motion.span>
          </h3>
          <div className="grid grid-cols-2 gap-3">
            {quickActions.map((action, index) => (
              <motion.div
                key={action.id}
                whileHover={{ scale: 1.03, y: -4 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => navigate(action.path)}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 + 0.3 }}
              >
                <Card className={`relative overflow-hidden cursor-pointer h-full ${action.dopamine ? 'ring-2 ring-primary-500/20' : ''}`}>
                  {action.badge && (
                    <motion.span
                      className="absolute right-2 top-2 rounded-full bg-accent-500 px-2 py-0.5 text-xs font-bold text-white"
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      {action.badge}
                    </motion.span>
                  )}

                  <div className={`mb-3 inline-flex rounded-xl bg-gradient-to-br ${action.color} p-3 text-white shadow-lg`}>
                    <action.icon size={24} />
                  </div>

                  <h4 className="font-bold text-gray-900 mb-1">{action.title}</h4>
                  <p className="text-xs text-gray-500 leading-relaxed">{action.subtitle}</p>

                  {action.dopamine && (
                    <motion.div
                      className="absolute bottom-2 left-2 h-2 w-2 rounded-full bg-green-500"
                      animate={{ scale: [1, 1.5, 1], opacity: [1, 0.5, 1] }}
                      transition={{ duration: 1.5, repeat: Infinity }}
                    />
                  )}
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Stats Overview - Social Proof */}
        <motion.section variants={itemVariants}>
          <h3 className="mb-3 text-lg font-bold text-gray-900">عملکرد شما</h3>
          <div className="grid grid-cols-3 gap-3">
            {[
              {
                label: 'بردها',
                value: stats?.won || 0,
                icon: Trophy,
                color: 'text-primary-600',
                bg: 'bg-primary-50'
              },
              {
                label: 'نرخ برد',
                value: `${stats?.win_rate || 0}%`,
                icon: TrendingUp,
                color: 'text-accent-600',
                bg: 'bg-accent-50',
                trend: '+۱۲٪'
              },
              {
                label: 'امتیاز',
                value: '۲,۴۵۰',
                icon: Star,
                color: 'text-reward-600',
                bg: 'bg-reward-50'
              },
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 + 0.5 }}
              >
                <Card className="text-center p-4">
                  <div className={`mx-auto mb-2 flex h-10 w-10 items-center justify-center rounded-xl ${stat.bg} ${stat.color}`}>
                    <stat.icon size={20} />
                  </div>
                  <p className="text-xl font-black text-gray-900">{toPersianNumber(stat.value)}</p>
                  <p className="text-xs text-gray-500">{stat.label}</p>
                  {stat.trend && (
                    <span className="mt-1 inline-block rounded-full bg-green-100 px-2 py-0.5 text-xs font-bold text-green-700">
                      {stat.trend}
                    </span>
                  )}
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Upcoming Matches - Scarcity Principle */}
        <motion.section variants={itemVariants}>
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-lg font-bold text-gray-900">مسابقات پیش‌رو</h3>
            <button
              onClick={() => navigate('/matches')}
              className="flex items-center gap-1 text-sm font-bold text-primary-600 hover:text-primary-700 transition-colors"
            >
              مشاهده همه
              <ChevronLeft size={16} />
            </button>
          </div>

          <div className="space-y-3">
            {upcomingMatches?.slice(0, 2).map((match, index) => (
              <motion.div
                key={match.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 + 0.6 }}
                whileHover={{ scale: 1.02 }}
                onClick={() => navigate(`/matches/${match.id}`)}
              >
                <Card className="cursor-pointer border-r-4 border-r-primary-500">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-bold text-gray-900">
                        {match.title || `مسابقه ${match.match_type_display}`}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        {formatPersianDate(match.scheduled_at)} • {match.court_name}
                      </p>
                    </div>
                    <div className="rounded-full bg-primary-100 p-2">
                      <ChevronLeft size={20} className="text-primary-600" />
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}

            {(!upcomingMatches || upcomingMatches.length === 0) && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="rounded-2xl bg-gradient-to-br from-gray-50 to-gray-100 p-8 text-center border-2 border-dashed border-gray-200"
              >
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-white shadow-soft">
                  <Trophy className="text-gray-400" size={32} />
                </div>
                <p className="text-gray-600 font-medium mb-2">هنوز مسابقه‌ای ندارید</p>
                <p className="text-sm text-gray-400 mb-4">اولین مسابقه خود را ایجاد کنید!</p>
                <Button
                  size="sm"
                  onClick={() => navigate('/matches/create')}
                  dopamineTrigger
                >
                  <Zap size={16} className="ml-1" />
                  ایجاد مسابقه
                </Button>
              </motion.div>
            )}
          </div>
        </motion.section>
      </motion.main>
    </div>
  );
};