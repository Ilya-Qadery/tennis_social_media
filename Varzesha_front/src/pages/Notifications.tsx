import React from 'react';
import { motion } from 'framer-motion';
import { Bell, Check, Trash2 } from 'lucide-react';
import { Header } from '@/components/layout/Header';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { useUIStore } from '@/store/uiStore';

export const Notifications = () => {
  const { notifications, markAsRead, markAllAsRead } = useUIStore();

  return (
    <div className="min-h-screen bg-gray-50">
      <Header title="اعلانات" />

      <main className="p-4">
        {notifications.length > 0 && (
          <div className="mb-4 flex justify-end">
            <Button variant="ghost" size="sm" onClick={markAllAsRead}>
              <Check size={16} className="ml-1" />
              علامت‌گذاری همه
            </Button>
          </div>
        )}

        <div className="space-y-3">
          {notifications.length === 0 ? (
            <div className="text-center py-12">
              <Bell className="mx-auto mb-4 text-gray-300" size={48} />
              <p className="text-gray-500">اعلانی وجود ندارد</p>
            </div>
          ) : (
            notifications.map((notification, index) => (
              <motion.div
                key={notification.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <Card
                  className={`cursor-pointer transition-colors ${
                    !notification.read ? 'bg-primary-50 border-primary-200' : ''
                  }`}
                  onClick={() => markAsRead(notification.id)}
                >
                  <div className="flex items-start gap-3">
                    <div className={`rounded-full p-2 ${
                      notification.type === 'match' ? 'bg-accent-100 text-accent-600' :
                      notification.type === 'court' ? 'bg-primary-100 text-primary-600' :
                      'bg-gray-100 text-gray-600'
                    }`}>
                      <Bell size={18} />
                    </div>
                    <div className="flex-1">
                      <p className="font-bold text-gray-900">{notification.title}</p>
                      <p className="text-sm text-gray-600 mt-1">{notification.message}</p>
                      <p className="text-xs text-gray-400 mt-2">
                        {new Date(notification.created_at).toLocaleTimeString('fa-IR')}
                      </p>
                    </div>
                    {!notification.read && (
                      <div className="h-2 w-2 rounded-full bg-primary-500" />
                    )}
                  </div>
                </Card>
              </motion.div>
            ))
          )}
        </div>
      </main>
    </div>
  );
};