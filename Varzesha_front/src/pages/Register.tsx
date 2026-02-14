import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { Eye, EyeOff, Phone, Lock, User } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useAuthStore } from '@/store/authStore';

export const Register = () => {
  const navigate = useNavigate();
  const { register, isLoading } = useAuthStore();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    phone: '',
    password: '',
    first_name: '',
    last_name: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await register(formData);
      navigate('/');
    } catch (err: any) {
      setError(err.message || 'خطا در ثبت‌نام');
    }
  };

  return (
    <div className="flex min-h-screen flex-col bg-white px-6 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex-1"
      >
        {/* Logo */}
        <div className="mb-8 text-center">
          <motion.div
            className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-3xl bg-primary-500 text-white shadow-glow"
            whileHover={{ scale: 1.05, rotate: 5 }}
          >
            <span className="text-3xl font-bold">و</span>
          </motion.div>
          <h1 className="text-2xl font-bold text-gray-900">ورزشا</h1>
          <p className="mt-2 text-gray-500">به جامعه تنیس ایران بپیوندید</p>
        </div>

        {/* Progress */}
        <div className="mb-6 flex justify-center gap-2">
          {[1, 2].map((s) => (
            <div
              key={s}
              className={`h-2 w-12 rounded-full transition-all ${
                s <= step ? 'bg-primary-500' : 'bg-gray-200'
              }`}
            />
          ))}
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {step === 1 ? (
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
              <div className="mb-4">
                <label className="mb-1 block text-sm font-medium text-gray-700">شماره موبایل</label>
                <div className="relative">
                  <Phone className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({...formData, phone: e.target.value})}
                    placeholder="۰۹۱۲۳۴۵۶۷۸۹"
                    className="w-full rounded-xl border border-gray-300 py-3 pr-10 pl-4 text-right focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
                    dir="ltr"
                  />
                </div>
              </div>

              <div className="mb-4">
                <label className="mb-1 block text-sm font-medium text-gray-700">رمز عبور</label>
                <div className="relative">
                  <Lock className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    placeholder="حداقل ۸ کاراکتر"
                    className="w-full rounded-xl border border-gray-300 py-3 pr-10 pl-12 text-right focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
                    dir="ltr"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                  >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
              </div>

              <Button type="button" fullWidth size="lg" onClick={() => setStep(2)}>
                ادامه
              </Button>
            </motion.div>
          ) : (
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
              <div className="mb-4">
                <label className="mb-1 block text-sm font-medium text-gray-700">نام</label>
                <div className="relative">
                  <User className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    value={formData.first_name}
                    onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                    placeholder="نام خود را وارد کنید"
                    className="w-full rounded-xl border border-gray-300 py-3 pr-10 pl-4 text-right focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
                  />
                </div>
              </div>

              <div className="mb-4">
                <label className="mb-1 block text-sm font-medium text-gray-700">نام خانوادگی</label>
                <div className="relative">
                  <User className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    value={formData.last_name}
                    onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                    placeholder="نام خانوادگی خود را وارد کنید"
                    className="w-full rounded-xl border border-gray-300 py-3 pr-10 pl-4 text-right focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
                  />
                </div>
              </div>

              {error && <p className="text-sm text-red-500">{error}</p>}

              <div className="flex gap-3">
                <Button type="button" variant="outline" className="flex-1" onClick={() => setStep(1)}>
                  بازگشت
                </Button>
                <Button type="submit" fullWidth isLoading={isLoading} className="flex-1">
                  ثبت‌نام
                </Button>
              </div>
            </motion.div>
          )}
        </form>

        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">
            قبلاً ثبت‌نام کرده‌اید؟{' '}
            <Link to="/login" className="font-bold text-primary-600 hover:text-primary-700">
              وارد شوید
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};