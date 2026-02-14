import React from 'react';
import { motion } from 'framer-motion';
import { Bell, ChevronLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useUIStore } from '@/store/uiStore';
import { getPersianGreeting } from '@/utils/persian';
import { useAuthStore } from '@/store/authStore';

interface HeaderProps {
  showBack?: boolean;
  title?: string;
  showNotification?: boolean;
}

export const Header = ({ showBack, title, showNotification = true }: HeaderProps) => {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const unreadCount = useUIStore((state) => state.unreadCount);

  return (
    <header className="sticky top-0 z-30 bg-white/80 px-4 py-3 backdrop-blur-md">
      <div className="flex items-center justify-between">
        {showBack ? (
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-1 text-gray-600"
          >
            <ChevronLeft size={24} />
            <span className="text-sm">بازگشت</span>
          </button>
        ) : (
          <div className="flex flex-col">
            <span className="text-xs text-gray-500">{getPersianGreeting()}</span>
            <h1 className="text-lg font-bold text-gray-900">
              {user?.first_name ? `${user.first_name} عزیز` : 'ورزشا'}
            </h1>
          </div>
        )}

        {title && <h1 className="text-lg font-bold text-gray-900">{title}</h1>}

        {showNotification && (
          <motion.button
            className="relative rounded-full p-2 text-gray-600 hover:bg-gray-100"
            whileTap={{ scale: 0.9 }}
            onClick={() => navigate('/notifications')}
          >
            <Bell size={24} />
            {unreadCount > 0 && (
              <span className="absolute right-1 top-1 flex h-5 w-5 items-center justify-center rounded-full bg-accent-500 text-xs font-bold text-white">
                {unreadCount > 9 ? '9+' : unreadCount}
              </span>
            )}
          </motion.button>
        )}
      </div>
    </header>
  );
};