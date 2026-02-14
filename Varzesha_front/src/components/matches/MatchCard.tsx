import React from 'react';
import { motion } from 'framer-motion';
import { MapPin, Clock, Users, Trophy } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import type { Match } from '@/types';
import { Card, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { toPersianNumber, formatPersianDate, getRelativeTime } from '@/utils/persian';
import { useJoinMatch } from '@/hooks/useMatches';

interface MatchCardProps {
  match: Match;
  showJoinButton?: boolean;
}

export const MatchCard = ({ match, showJoinButton = true }: MatchCardProps) => {
  const navigate = useNavigate();
  const joinMutation = useJoinMatch();

  const statusColors: Record<string, Badge['variant']> = {
    pending: 'warning',
    confirmed: 'success',
    completed: 'default',
    cancelled: 'error',
  };

  const handleJoin = async (e: React.MouseEvent) => {
    e.stopPropagation();
    await joinMutation.mutateAsync(match.id);
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={() => navigate(`/matches/${match.id}`)}
    >
      <Card className="cursor-pointer">
        <CardContent className="space-y-3">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div>
              <h3 className="font-bold text-gray-900">
                {match.title || `مسابقه ${match.match_type_display}`}
              </h3>
              <p className="text-sm text-gray-500">
                {formatPersianDate(match.scheduled_at)}
              </p>
            </div>
            <Badge variant={statusColors[match.status] || 'default'}>
              {match.status_display}
            </Badge>
          </div>

          {/* Details */}
          <div className="flex flex-wrap gap-3 text-sm text-gray-600">
            <div className="flex items-center gap-1">
              <Clock size={16} className="text-primary-500" />
              <span>{toPersianNumber(match.duration_minutes)} دقیقه</span>
            </div>
            <div className="flex items-center gap-1">
              <MapPin size={16} className="text-primary-500" />
              <span>{match.court?.name || match.court_name}</span>
            </div>
            <div className="flex items-center gap-1">
              <Users size={16} className="text-primary-500" />
              <span>
                {match.opponent ? '۲/۲ بازیکن' : '۱/۲ بازیکن'}
              </span>
            </div>
          </div>

          {/* Players */}
          <div className="flex items-center justify-between rounded-lg bg-gray-50 p-3">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-700">
                {match.organizer.name[0]}
              </div>
              <span className="text-sm font-medium">{match.organizer.name}</span>
            </div>

            <span className="text-lg font-bold text-gray-400">VS</span>

            {match.opponent ? (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium">{match.opponent.name}</span>
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-accent-100 text-sm font-bold text-accent-700">
                  {match.opponent.name[0]}
                </div>
              </div>
            ) : (
              <span className="text-sm text-gray-400">در انتظار حریف...</span>
            )}
          </div>

          {/* Join Button */}
          {showJoinButton && match.can_join && !match.is_organizer && (
            <Button
              fullWidth
              onClick={handleJoin}
              isLoading={joinMutation.isPending}
              dopamineTrigger={true}
            >
              <Trophy size={18} />
              پیوستن به مسابقه
            </Button>
          )}

          {/* NTRP Range */}
          {(match.ntrp_min || match.ntrp_max) && (
            <p className="text-xs text-gray-500">
              سطح مهارت: {match.ntrp_min ? `از ${toPersianNumber(match.ntrp_min)}` : ''}
              {match.ntrp_max ? ` تا ${toPersianNumber(match.ntrp_max)}` : ''}
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};