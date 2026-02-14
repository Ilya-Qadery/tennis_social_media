import React from 'react';
import { motion } from 'framer-motion';
import { Flame } from 'lucide-react';
import { toPersianNumber } from '@/utils/persian';

interface StreakCounterProps {
  count: number;
  record?: number;
  size?: 'sm' | 'md' | 'lg';
}

export const StreakCounter = ({ count, record, size = 'md' }: StreakCounterProps) => {
  const sizes = {
    sm: { icon: 16, text: 'text-sm', padding: 'px-2 py-1' },
    md: { icon: 20, text: 'text-base', padding: 'px-3 py-1.5' },
    lg: { icon: 28, text: 'text-lg', padding: 'px-4 py-2' },
  };

  const isRecord = record && count >= record;

  return (
    <motion.div
      className={`inline-flex items-center gap-1.5 rounded-full ${sizes[size].padding} ${
        isRecord ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white' : 'bg-orange-100 text-orange-700'
      }`}
      animate={isRecord ? { scale: [1, 1.05, 1] } : undefined}
      transition={{ repeat: Infinity, duration: 2 }}
    >
      <Flame size={sizes[size].icon} className={isRecord ? 'fill-current' : ''} />
      <span className={`font-bold ${sizes[size].text}`}>
        {toPersianNumber(count)} روز
      </span>
      {isRecord && (
        <span className="mr-1 text-xs opacity-90">رکورد!</span>
      )}
    </motion.div>
  );
};