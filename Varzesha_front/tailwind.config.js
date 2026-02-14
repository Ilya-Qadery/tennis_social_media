/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary Action Colors - Green Psychology
        primary: {
          50: '#E8F8F5',
          100: '#D1F2EB',
          200: '#A9DFD4',
          300: '#7DCEC4',
          400: '#52BE80',
          500: '#2ECC71', // Main action color
          600: '#27AE60', // Hover state
          700: '#1E8449',
          800: '#196F3D',
          900: '#145A32',
        },
        // Urgency/Achievement - Orange Dopamine Trigger
        accent: {
          50: '#FEF5E7',
          100: '#FDEBD0',
          200: '#FAD7A0',
          300: '#F8C471',
          400: '#F5B041',
          500: '#FF6B35', // Urgency/CTA
          600: '#E85D04',
          700: '#D35400',
        },
        // Trust & Professionalism - Deep Blue
        trust: {
          50: '#EBF5FB',
          100: '#D6EAF8',
          200: '#AED6F1',
          300: '#85C1E9',
          400: '#5DADE2',
          500: '#1A3A5C', // Trust anchor
          600: '#154360',
          700: '#1A5276',
        },
        // Rewards & VIP - Gold
        reward: {
          50: '#FCF3CF',
          100: '#F9E79F',
          200: '#F7DC6F',
          300: '#F4D03F',
          400: '#F1C40F', // Gold/Rewards
          500: '#D4AC0D',
          600: '#B7950B',
        },
        // Semantic Colors
        success: '#2ECC71',
        warning: '#F1C40F',
        error: '#E74C3C',
        info: '#3498DB',
      },
      fontFamily: {
        sans: ['Vazirmatn', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        '2xs': '0.625rem',
        'xs': '0.75rem',
        'sm': '0.875rem',
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'elevated': '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
        'glow': '0 0 20px rgba(46, 204, 113, 0.3)',
      },
      animation: {
        'bounce-slow': 'bounce 2s infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'fade-in': 'fadeIn 0.2s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}