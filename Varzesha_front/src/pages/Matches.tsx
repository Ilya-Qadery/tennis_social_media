import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from '@/components/layout/Header';
import { MatchCard } from '@/components/matches/MatchCard';
import { Button } from '@/components/ui/Button';
import { useMatches, useAvailableMatches } from '@/hooks/useMatches';
import { Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

type TabType = 'my' | 'available';

export const Matches = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<TabType>('my');
  const { data: myMatches } = useMatches();
  const { data: availableMatches } = useAvailableMatches();

  const tabs = [
    { id: 'my' as const, label: 'مسابقات من' },
    { id: 'available' as const, label: 'در دسترس' },
  ];

  const matches = activeTab === 'my' ? myMatches : availableMatches;

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <Header title="مسابقات" />

      <main className="p-4">
        {/* Tabs */}
        <div className="mb-4 flex rounded-xl bg-white p-1 shadow-sm">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`relative flex-1 rounded-lg py-2 text-sm font-medium transition-colors ${
                activeTab === tab.id ? 'text-primary-700' : 'text-gray-500'
              }`}
            >
              {activeTab === tab.id && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute inset-0 rounded-lg bg-primary-100"
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                />
              )}
              <span className="relative z-10">{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Matches List */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-3"
          >
            {matches?.map((match) => (
              <MatchCard
                key={match.id}
                match={match}
                showJoinButton={activeTab === 'available'}
              />
            ))}

            {(!matches || matches.length === 0) && (
              <div className="rounded-2xl bg-white p-8 text-center">
                <p className="text-gray-500">
                  {activeTab === 'my'
                    ? 'هنوز مسابقه‌ای ایجاد نکرده‌اید'
                    : 'در حال حاضر مسابقه‌ای در دسترس نیست'}
                </p>
                <Button
                  variant="outline"
                  className="mt-4"
                  onClick={() => navigate('/matches/create')}
                >
                  <Plus size={18} className="ml-1" />
                  ایجاد مسابقه
                </Button>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </main>

      {/* Floating Action Button */}
      <motion.button
        className="fixed left-4 bottom-20 flex h-14 w-14 items-center justify-center rounded-full bg-primary-500 text-white shadow-glow"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => navigate('/matches/create')}
      >
        <Plus size={28} />
      </motion.button>
    </div>
  );
};