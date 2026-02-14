import React, { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { useCourts, useCities } from '@/hooks/useCourts';
import { Card } from '@/components/ui/Card';
import { MapPin, Star, Phone } from 'lucide-react';
import { toPersianNumber, formatToman } from '@/utils/persian';
import { motion } from 'framer-motion';

export const Courts = () => {
  const [selectedCity, setSelectedCity] = useState<string>();
  const { data: courts } = useCourts(selectedCity ? { city: selectedCity } : undefined);
  const { data: cities } = useCities();

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <Header title="زمین‌های تنیس" />

      <main className="p-4 space-y-4">
        {/* City Filter */}
        <div className="flex gap-2 overflow-x-auto pb-2 no-scrollbar">
          <button
            onClick={() => setSelectedCity(undefined)}
            className={`whitespace-nowrap rounded-full px-4 py-2 text-sm font-medium ${
              !selectedCity ? 'bg-primary-500 text-white' : 'bg-white text-gray-700'
            }`}
          >
            همه شهرها
          </button>
          {cities?.map((city) => (
            <button
              key={city}
              onClick={() => setSelectedCity(city)}
              className={`whitespace-nowrap rounded-full px-4 py-2 text-sm font-medium ${
                selectedCity === city ? 'bg-primary-500 text-white' : 'bg-white text-gray-700'
              }`}
            >
              {city}
            </button>
          ))}
        </div>

        {/* Courts List */}
        <div className="space-y-3">
          {courts?.map((court) => (
            <motion.div
              key={court.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <Card className="overflow-hidden">
                {court.main_image && (
                  <div className="h-40 w-full bg-gray-200">
                    <img
                      src={court.main_image}
                      alt={court.name}
                      className="h-full w-full object-cover"
                    />
                  </div>
                )}
                <div className="p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-bold text-gray-900">{court.name}</h3>
                      <div className="mt-1 flex items-center gap-1 text-sm text-gray-500">
                        <MapPin size={16} />
                        <span>{court.city}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-1 rounded-lg bg-yellow-50 px-2 py-1 text-yellow-700">
                      <Star size={16} className="fill-current" />
                      <span className="font-bold">{toPersianNumber(court.average_rating)}</span>
                    </div>
                  </div>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {court.indoor && (
                      <span className="rounded-full bg-blue-50 px-2 py-1 text-xs text-blue-700">
                        سالن
                      </span>
                    )}
                    {court.has_lights && (
                      <span className="rounded-full bg-yellow-50 px-2 py-1 text-xs text-yellow-700">
                        نورپردازی
                      </span>
                    )}
                    <span className="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-700">
                      {court.surface_type_display}
                    </span>
                  </div>

                  <div className="mt-4 flex items-center justify-between">
                    <span className="font-bold text-primary-600">
                      {formatToman(court.price_per_hour)} / ساعت
                    </span>
                    <button className="flex items-center gap-1 rounded-lg bg-primary-50 px-3 py-1.5 text-sm font-medium text-primary-700">
                      <Phone size={16} />
                      تماس
                    </button>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </main>
    </div>
  );
};