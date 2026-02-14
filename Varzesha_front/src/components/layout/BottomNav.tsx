// src/components/layout/BottomNav.tsx - FIXED
import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Home, Calendar, Plus, Trophy, User } from 'lucide-react';

export const BottomNav = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', icon: Home, label: 'خانه' },
    { path: '/matches', icon: Calendar, label: 'مسابقات' },
    { path: '/matches/create', icon: Plus, label: 'جدید', isCenter: true },
    { path: '/training', icon: Trophy, label: 'تمرین' },
    { path: '/profile', icon: User, label: 'پروفایل' },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-lg border-t border-gray-200 pb-safe">
      <div className="flex h-16 items-center justify-around px-2">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path ||
            (item.path !== '/' && location.pathname.startsWith(item.path));

          if (item.isCenter) {
            return (
              <NavLink key={item.path} to={item.path} className="relative -mt-6">
                <motion.div
                  className="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-glow"
                  whileTap={{ scale: 0.9 }}
                  whileHover={{ scale: 1.1, rotate: 90 }}
                  transition={{ type: 'spring', stiffness: 400 }}
                >
                  <item.icon size={28} strokeWidth={2.5} />
                </motion.div>
                <span className="absolute -bottom-5 left-1/2 -translate-x-1/2 text-xs font-medium text-gray-600 whitespace-nowrap">
                  {item.label}
                </span>
              </NavLink>
            );
          }

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={`relative flex flex-col items-center gap-1 p-2 ${
                isActive ? 'text-primary-600' : 'text-gray-400'
              }`}
            >
              <motion.div
                whileTap={{ scale: 0.8 }}
                animate={isActive ? { y: -2 } : { y: 0 }}
              >
                <item.icon
                  size={24}
                  strokeWidth={isActive ? 2.5 : 2}
                  className={isActive ? 'fill-primary-100' : ''}
                />
              </motion.div>
              <span className="text-xs font-medium">{item.label}</span>

              {isActive && (
                <motion.div
                  layoutId="bottomNavIndicator"
                  className="absolute -bottom-1 h-1 w-8 rounded-full bg-primary-500"
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                />
              )}
            </NavLink>
          );
        })}
      </div>
    </nav>
  );
};