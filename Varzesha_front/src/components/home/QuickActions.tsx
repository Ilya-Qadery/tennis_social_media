import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Users, MapPin, Trophy, Calendar, Zap } from 'lucide-react';
import { Card } from '@/components/ui/Card';

const actions = [
  {
    id: 'find-opponent',
    title: 'رقیب‌یابی',
    subtitle: 'حریف هم‌سطح در ۲ دقیقه',
    icon: Users,
    color: 'bg-primary-500',
    path: '/matches/available',
    badge: 'جدید',
  },
  {
    id: 'find-court',
    title: 'یافتن زمین',
    subtitle: 'بهترین زمین‌های نزدیک',
    icon: MapPin,
    color: 'bg-trust-500',
    path: '/courts',
  },
  {
    id: 'record-result',
    title: 'ثبت نتیجه',
    subtitle: 'امتیازدهی سریع',
    icon: Trophy,
    color: 'bg-accent-500',
    path: '/matches',
    badge: '۲ مسابقه',
  },
  {
    id: 'schedule',
    title: 'زمان‌بندی',
    subtitle: 'برنامه‌ریزی تمرین',
    icon: Calendar,
    color: 'bg-purple-500',
    path: '/training',
  },
];

export const QuickActions = () => {
  const navigate = useNavigate();

  return (
    <div className="grid grid-cols-2 gap-3">
      {actions.map((action, index) => (
        <motion.div
          key={action.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          onClick={() => navigate(action.path)}
        >
          <Card className="relative cursor-pointer overflow-hidden p-4">
            {/* Badge */}
            {action.badge && (
              <span className="absolute right-2 top-2 rounded-full bg-accent-500 px-2 py-0.5 text-xs font-bold text-white">
                {action.badge}
              </span>
            )}

            <div className={`mb-3 inline-flex rounded-xl ${action.color} p-3 text-white`}>
              <action.icon size={24} />
            </div>

            <h3 className="mb-1 font-bold text-gray-900">{action.title}</h3>
            <p className="text-xs text-gray-500">{action.subtitle}</p>
          </Card>
        </motion.div>
      ))}
    </div>
  );
};