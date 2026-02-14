import React from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  MapPin, Phone, Star, Clock, CheckCircle,
  Navigation, Share2, Heart
} from 'lucide-react';
import { Header } from '@/components/layout/Header';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { useCourt, useCourtReviews } from '@/hooks/useCourts';
import { toPersianNumber, formatToman } from '@/utils/persian';

export const CourtDetail = () => {
  const { id } = useParams<{ id: string }>();
  const { data: court, isLoading } = useCourt(id || '');
  const { data: reviews } = useCourtReviews(id || '');

  if (isLoading || !court) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header showBack title="جزئیات زمین" />
        <div className="p-4">
          <div className="h-48 animate-pulse rounded-2xl bg-gray-200" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <Header showBack title={court.name} />

      {/* Image */}
      <div className="relative h-64 bg-gray-200">
        {court.main_image ? (
          <img
            src={court.main_image}
            alt={court.name}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-gray-400">
            <MapPin size={48} />
          </div>
        )}
        <div className="absolute bottom-4 right-4 flex gap-2">
          <button className="rounded-full bg-white/90 p-2 backdrop-blur-sm">
            <Heart size={20} className="text-gray-600" />
          </button>
          <button className="rounded-full bg-white/90 p-2 backdrop-blur-sm">
            <Share2 size={20} className="text-gray-600" />
          </button>
        </div>
      </div>

      <main className="p-4 space-y-4">
        {/* Info */}
        <Card>
          <div className="flex items-start justify-between mb-3">
            <div>
              <h1 className="text-xl font-bold text-gray-900">{court.name}</h1>
              <div className="flex items-center gap-1 text-gray-500 mt-1">
                <MapPin size={16} />
                <span className="text-sm">{court.city}، {court.address}</span>
              </div>
            </div>
            <div className="flex items-center gap-1 rounded-xl bg-yellow-50 px-3 py-1 text-yellow-700">
              <Star size={18} className="fill-current" />
              <span className="font-bold">{toPersianNumber(court.average_rating)}</span>
              <span className="text-xs text-gray-400">({toPersianNumber(court.total_ratings)})</span>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 mb-4">
            {court.indoor && <Badge variant="info">سالن</Badge>}
            {court.has_lights && <Badge variant="warning">نورپردازی</Badge>}
            {court.has_parking && <Badge>پارکینگ</Badge>}
            <Badge variant="secondary">{court.surface_type_display}</Badge>
          </div>

          <div className="flex items-center justify-between rounded-xl bg-primary-50 p-4">
            <div>
              <p className="text-sm text-gray-600">قیمت هر ساعت</p>
              <p className="text-2xl font-black text-primary-700">
                {formatToman(court.price_per_hour)}
              </p>
            </div>
            <Button>رزرو زمین</Button>
          </div>
        </Card>

        {/* Facilities */}
        <Card>
          <h3 className="font-bold text-gray-900 mb-3">امکانات</h3>
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: 'روشنایی', available: court.has_lights },
              { label: 'پارکینگ', available: court.has_parking },
              { label: 'دوش', available: court.has_showers },
              { label: 'رختکن', available: court.has_locker_room },
              { label: 'اجاره تجهیزات', available: court.has_equipment_rental },
            ].map((item) => (
              <div
                key={item.label}
                className={`flex items-center gap-2 ${item.available ? 'text-gray-700' : 'text-gray-400'}`}
              >
                <CheckCircle
                  size={18}
                  className={item.available ? 'text-primary-500' : 'text-gray-300'}
                />
                <span className="text-sm">{item.label}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Reviews */}
        <Card>
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-bold text-gray-900">نظرات</h3>
            <Button variant="ghost" size="sm">مشاهده همه</Button>
          </div>

          <div className="space-y-3">
            {reviews?.slice(0, 2).map((review) => (
              <div key={review.id} className="border-b border-gray-100 pb-3 last:border-0">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-gray-900">{review.user_name}</span>
                  <div className="flex items-center gap-1 text-yellow-500">
                    <Star size={14} fill="currentColor" />
                    <span className="text-sm">{toPersianNumber(review.rating)}</span>
                  </div>
                </div>
                <p className="text-sm text-gray-600">{review.comment}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Contact Buttons */}
        <div className="flex gap-3">
          <Button fullWidth variant="outline" leftIcon={<Phone size={18} />}>
            تماس
          </Button>
          <Button fullWidth leftIcon={<Navigation size={18} />}>
            مسیریابی
          </Button>
        </div>
      </main>
    </div>
  );
};