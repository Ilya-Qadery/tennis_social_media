import React from 'react';
import { motion } from 'framer-motion';
import { toPersianNumber } from '@/utils/persian';

interface ProgressBarProps {
  progress: number; // 0-100
  size?: 'sm' | 'md' | 'lg';
  color?: 'primary' | 'accent' | 'success' | 'reward';
  showLabel?: boolean;
  animated?: boolean;
  label?: string;
}

export const ProgressBar = ({
  progress,
  size = 'md',
  color = 'primary',
  showLabel = true,
  animated = true,
  label,
}: ProgressBarProps) => {
  const sizes = {
    sm: 'h-1.5',
    md: 'h-2.5',
    lg: 'h-4',
  };

  const colors = {
    primary: 'bg-primary-500',
    accent: 'bg-accent-500',
    success: 'bg-green-500',
    reward: 'bg-reward-400',
  };

  const clampedProgress = Math.min(100, Math.max(0, progress));

  return (
    <div className="w-full">
      {(showLabel || label) && (
        <div className="mb-1 flex justify-between text-sm">
          {label && <span className="text-gray-600">{label}</span>}
          {showLabel && (
            <span className="font-medium text-gray-900">
              {toPersianNumber(Math.round(clampedProgress))}%
            </span>
          )}
        </div>
      )}
      <div className={`w-full overflow-hidden rounded-full bg-gray-200 ${sizes[size]}`}>
        <motion.div
          className={`h-full rounded-full ${colors[color]}`}
          initial={{ width: 0 }}
          animate={{ width: `${clampedProgress}%` }}
          transition={animated ? { duration: 0.8, ease: 'easeOut' } : { duration: 0 }}
        />
      </div>
    </div>
  );
};