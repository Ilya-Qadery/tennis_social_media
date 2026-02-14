import { Variants } from 'framer-motion';

// Dopamine-triggering micro-interactions
export const pulseAnimation = {
  scale: [1, 1.05, 1],
  transition: { duration: 0.3 }
};

export const successAnimation = {
  scale: [1, 1.2, 1],
  rotate: [0, 10, -10, 0],
  transition: { duration: 0.5 }
};

export const slideUpVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: 'spring', stiffness: 300, damping: 30 }
  }
};

export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

export const cardHover = {
  rest: { scale: 1, y: 0 },
  hover: {
    scale: 1.02,
    y: -4,
    transition: { type: 'spring', stiffness: 400, damping: 25 }
  }
};

export const buttonTap = {
  scale: 0.95,
  transition: { duration: 0.1 }
};

export const pageTransition: Variants = {
  initial: { opacity: 0, x: 20 },
  animate: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.3, ease: 'easeOut' }
  },
  exit: {
    opacity: 0,
    x: -20,
    transition: { duration: 0.2 }
  }
};