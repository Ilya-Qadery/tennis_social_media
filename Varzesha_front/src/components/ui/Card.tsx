import React from 'react';
import { motion } from 'framer-motion';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
  glow?: boolean;
  gradient?: boolean;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, hover = true, glow, gradient, children, ...props }, ref) => {
    return (
      <motion.div
        ref={ref}
        className={cn(
          'relative overflow-hidden rounded-2xl bg-white p-4 shadow-card',
          hover && 'transition-all duration-300 hover:shadow-elevated hover:-translate-y-1',
          glow && 'hover:shadow-glow',
          gradient && 'bg-gradient-to-br from-white to-gray-50',
          className
        )}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        {...props}
      >
        {children}
      </motion.div>
    );
  }
);

Card.displayName = 'Card';

export const CardHeader = ({ className, children }: { className?: string; children: React.ReactNode }) => (
  <div className={cn('mb-3 flex items-center justify-between', className)}>
    {children}
  </div>
);

export const CardTitle = ({ className, children }: { className?: string; children: React.ReactNode }) => (
  <h3 className={cn('text-lg font-bold text-gray-900', className)}>
    {children}
  </h3>
);

export const CardContent = ({ className, children }: { className?: string; children: React.ReactNode }) => (
  <div className={cn('', className)}>
    {children}
  </div>
);