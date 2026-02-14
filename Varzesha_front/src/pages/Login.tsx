// src/pages/Login.tsx - REDESIGNED
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Phone, Lock, ArrowLeft, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useAuthStore } from '@/store/authStore';
import { toPersianNumber } from '@/utils/persian';

export const Login = () => {
  const navigate = useNavigate();
  const { login, isLoading } = useAuthStore();
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await login(phone, password);
      navigate('/');
    } catch (err) {
      setError('شماره تلفن یا رمز عبور اشتباه است');
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-white">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute -top-40 -right-40 h-80 w-80 rounded-full bg-primary-200/30 blur-3xl"
          animate={{ scale: [1, 1.2, 1], rotate: [0, 90, 0] }}
          transition={{ duration: 20, repeat: Infinity }}
        />
        <motion.div
          className="absolute -bottom-40 -left-40 h-96 w-96 rounded-full bg-accent-200/20 blur-3xl"
          animate={{ scale: [1, 1.3, 1], rotate: [0, -90, 0] }}
          transition={{ duration: 25, repeat: Infinity }}
        />
      </div>

      {/* Content */}
      <div className="relative flex min-h-screen flex-col px-6 py-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="flex-1"
        >
          {/* Logo Section with Animation */}
          <div className="mb-12 text-center">
            <motion.div
              className="relative mx-auto mb-6 inline-block"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <motion.div
                className="flex h-24 w-24 items-center justify-center rounded-3xl bg-gradient-to-br from-primary-400 to-primary-600 text-white shadow-glow"
                animate={{
                  boxShadow: ['0 0 20px rgba(46, 204, 113, 0.3)', '0 0 40px rgba(46, 204, 113, 0.5)', '0 0 20px rgba(46, 204, 113, 0.3)']
                }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <span className="text-4xl font-bold">و</span>
              </motion.div>
              <motion.div
                className="absolute -right-2 -top-2 flex h-8 w-8 items-center justify-center rounded-full bg-accent-500 text-white"
                animate={{ rotate: [0, 15, -15, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <Sparkles size={16} />
              </motion.div>
            </motion.div>

            <motion.h1
              className="text-3xl font-black text-gray-900"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              ورزشا
            </motion.h1>
            <motion.p
              className="mt-2 text-gray-500"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              جامعه تنیس ایران
            </motion.p>
          </div>

          {/* Social Proof Banner */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
            className="mb-8 rounded-2xl bg-gradient-to-r from-primary-50 to-accent-50 p-4"
          >
            <div className="flex items-center gap-3">
              <div className="flex -space-x-2">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-gray-200 text-xs font-bold"
                  >
                    {String.fromCharCode(1575 + i)}
                  </div>
                ))}
              </div>
              <p className="text-sm text-gray-600">
                <span className="font-bold text-primary-600">{toPersianNumber(5243)}</span> بازیکن فعال
              </p>
            </div>
          </motion.div>

          {/* Form */}
          <motion.form
            onSubmit={handleSubmit}
            className="space-y-5"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <div className="group">
              <label className="mb-2 block text-sm font-semibold text-gray-700 transition-colors group-focus-within:text-primary-600">
                شماره موبایل
              </label>
              <div className="relative">
                <Phone className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 transition-colors group-focus-within:text-primary-500" size={20} />
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="۰۹۱۲۳۴۵۶۷۸۹"
                  className="w-full rounded-2xl border-2 border-gray-200 bg-white py-4 pr-12 pl-4 text-right transition-all focus:border-primary-500 focus:outline-none focus:ring-4 focus:ring-primary-500/10"
                  dir="ltr"
                />
              </div>
            </div>

            <div className="group">
              <label className="mb-2 block text-sm font-semibold text-gray-700 transition-colors group-focus-within:text-primary-600">
                رمز عبور
              </label>
              <div className="relative">
                <Lock className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 transition-colors group-focus-within:text-primary-500" size={20} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full rounded-2xl border-2 border-gray-200 bg-white py-4 pr-12 pl-12 text-right transition-all focus:border-primary-500 focus:outline-none focus:ring-4 focus:ring-primary-500/10"
                  dir="ltr"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 transition-colors hover:text-gray-600"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {error && (
              <motion.p
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="rounded-xl bg-red-50 p-3 text-center text-sm text-red-600"
              >
                {error}
              </motion.p>
            )}

            <Button
              type="submit"
              fullWidth
              size="lg"
              isLoading={isLoading}
              className="mt-6 shadow-glow transition-shadow hover:shadow-lg"
            >
              <span>ورود به اپلیکیشن</span>
              <ArrowLeft size={20} className="mr-2 rotate-180" />
            </Button>
          </motion.form>

          {/* Footer */}
          <motion.div
            className="mt-8 text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
          >
            <p className="text-sm text-gray-500">
              حساب کاربری ندارید؟{' '}
              <Link
                to="/register"
                className="relative font-bold text-primary-600 transition-colors hover:text-primary-700"
              >
                ثبت‌نام کنید
                <motion.span
                  className="absolute -bottom-1 left-0 h-0.5 w-full bg-primary-500"
                  initial={{ scaleX: 0 }}
                  whileHover={{ scaleX: 1 }}
                  transition={{ duration: 0.2 }}
                />
              </Link>
            </p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};