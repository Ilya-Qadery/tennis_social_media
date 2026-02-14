// src/App.tsx - FIX ROUTING
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AnimatePresence } from 'framer-motion';
import { useAuthStore } from '@/store/authStore';

// Layout
import { BottomNav } from '@/components/layout/BottomNav';
import { ToastContainer } from '@/components/ui/Toast';

// Pages
import { Home } from '@/pages/Home';
import { Login } from '@/pages/Login';
import { Register } from '@/pages/Register';  // MISSING!
import { Matches } from '@/pages/Matches';
import { MatchDetail } from '@/pages/MatchDetail';  // MISSING!
import { Profile } from '@/pages/Profile';
import { Courts } from '@/pages/Courts';
import { CourtDetail } from '@/pages/CourtDetail';  // MISSING!
import { Training } from '@/pages/Training';
import { CreateMatch } from '@/pages/CreateMatch';
import { Notifications } from '@/pages/Notifications';  // MISSING!

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 1000 * 60 * 5, retry: 2 },
  },
});

// Layout wrapper that shows bottom nav
const MainLayout = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();
  const hideNavOnRoutes = ['/login', '/register', '/matches/create'];
  const showNav = !hideNavOnRoutes.some(route => location.pathname.startsWith(route));

  return (
    <div className="min-h-screen bg-gray-50">
      {children}
      {showNav && <BottomNav />}
      <ToastContainer />
    </div>
  );
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Routes with Layout */}
          <Route path="/*" element={
            <MainLayout>
              <Routes>
                <Route path="/" element={<PrivateRoute><Home /></PrivateRoute>} />
                <Route path="/matches" element={<PrivateRoute><Matches /></PrivateRoute>} />
                <Route path="/matches/:id" element={<PrivateRoute><MatchDetail /></PrivateRoute>} />
                <Route path="/matches/create" element={<PrivateRoute><CreateMatch /></PrivateRoute>} />
                <Route path="/courts" element={<PrivateRoute><Courts /></PrivateRoute>} />
                <Route path="/courts/:id" element={<PrivateRoute><CourtDetail /></PrivateRoute>} />
                <Route path="/training" element={<PrivateRoute><Training /></PrivateRoute>} />
                <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
                <Route path="/notifications" element={<PrivateRoute><Notifications /></PrivateRoute>} />
              </Routes>
            </MainLayout>
          } />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

export default App;