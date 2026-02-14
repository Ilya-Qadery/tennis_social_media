import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ArrowLeft, Calendar, MapPin, Clock, Users,
  Trophy, Share2, MessageCircle
} from 'lucide-react';
import { Header } from '@/components/layout/Header';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { useMatch } from '@/hooks/useMatches';
import { toPersianNumber, formatPersianDate } from '@/utils/persian';

export const MatchDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: match, isLoading } = useMatch(id || '');

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header showBack title="جزئیات مسابقه" />
        <div className="p-4">
          <div className="h-32 animate-pulse rounded-2xl bg-gray-200" />
        </div>
      </div>
    );
  }

  if (!match) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header showBack title="جزئیات مسابقه" />
        <div className="p-4 text-center">
          <p className="text-gray-500">مسابقه یافت نشد</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <Header showBack title="جزئیات مسابقه" />

      <main className="p-4 space-y-4">
        {/* Status Banner */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className={`rounded-2xl p-4 text-center text-white ${
            match.status === 'confirmed' ? 'bg-primary-500' :
            match.status === 'pending' ? 'bg-accent-500' :
            match.status === 'completed' ? 'bg-trust-500' : 'bg-gray-500'
          }`}
        >
          <p className="font-bold text-lg">{match.status_display}</p>
          <p className="text-sm opacity-90">
            {match.status === 'pending' && 'در انتظار حریف'}
            {match.status === 'confirmed' && 'حریف پیدا شد!'}
            {match.status === 'completed' && 'مسابقه به پایان رسید'}
          </p>
        </motion.div>

        {/* Match Info */}
        <Card>
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            {match.title || `مسابقه ${match.match_type_display}`}
          </h2>

          <div className="space-y-3">
            <div className="flex items-center gap-3 text-gray-700">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-100 text-primary-600">
                <Calendar size={20} />
              </div>
              <div>
                <p className="text-sm text-gray-500">تاریخ</p>
                <p className="font-medium">{formatPersianDate(match.scheduled_at)}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 text-gray-700">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent-100 text-accent-600">
                <Clock size={20} />
              </div>
              <div>
                <p className="text-sm text-gray-500">مدت</p>
                <p className="font-medium">{toPersianNumber(match.duration_minutes)} دقیقه</p>
              </div>
            </div>

            <div className="flex items-center gap-3 text-gray-700">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-trust-100 text-trust-600">
                <MapPin size={20} />
              </div>
              <div>
                <p className="text-sm text-gray-500">محل برگزاری</p>
                <p className="font-medium">{match.court?.name || match.court_name}</p>
              </div>
            </div>
          </div>
        </Card>

        {/* Players */}
        <Card>
          <h3 className="font-bold text-gray-900 mb-4">بازیکنان</h3>
          <div className="flex items-center justify-between">
            <div className="text-center flex-1">
              <div className="mx-auto mb-2 flex h-16 w-16 items-center justify-center rounded-full bg-primary-100 text-2xl font-bold text-primary-700">
                {match.organizer.name[0]}
              </div>
              <p className="font-medium text-gray-900">{match.organizer.name}</p>
              <Badge variant="primary" className="mt-1">برگزارکننده</Badge>
            </div>

            <div className="text-2xl font-bold text-gray-300">VS</div>

            <div className="text-center flex-1">
              {match.opponent ? (
                <>
                  <div className="mx-auto mb-2 flex h-16 w-16 items-center justify-center rounded-full bg-accent-100 text-2xl font-bold text-accent-700">
                    {match.opponent.name[0]}
                  </div>
                  <p className="font-medium text-gray-900">{match.opponent.name}</p>
                  <Badge variant="accent" className="mt-1">حریف</Badge>
                </>
              ) : (
                <>
                  <div className="mx-auto mb-2 flex h-16 w-16 items-center justify-center rounded-full bg-gray-100 text-2xl font-bold text-gray-400">
                    ?
                  </div>
                  <p className="text-gray-500">در انتظار</p>
                </>
              )}
            </div>
          </div>
        </Card>

        {/* Score (if completed) */}
        {match.status === 'completed' && (
          <Card className="bg-gradient-to-br from-primary-50 to-accent-50 border-2 border-primary-200">
            <div className="text-center">
              <Trophy className="mx-auto mb-2 text-reward-500" size={32} />
              <h3 className="font-bold text-gray-900 mb-4">نتیجه مسابقه</h3>
              <div className="flex items-center justify-center gap-4 text-3xl font-black">
                <span className="text-primary-600">{match.organizer_score}</span>
                <span className="text-gray-400">-</span>
                <span className="text-accent-600">{match.opponent_score}</span>
              </div>
              {match.winner && (
                <p className="mt-2 text-sm text-gray-600">
                  برنده: <span className="font-bold text-primary-600">{match.winner.name}</span>
                </p>
              )}
            </div>
          </Card>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <Button variant="outline" className="flex-1" leftIcon={<Share2 size={18} />}>
            اشتراک‌گذاری
          </Button>
          <Button variant="outline" className="flex-1" leftIcon={<MessageCircle size={18} />}>
            پیام
          </Button>
        </div>

        {/* Join Button (if available) */}
        {match.can_join && (
          <Button fullWidth size="lg" dopamineTrigger>
            پیوستن به مسابقه
          </Button>
        )}
      </main>
    </div>
  );
};