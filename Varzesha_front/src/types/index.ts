// User Types
export interface User {
  id: string;
  phone: string;
  first_name: string;
  last_name: string;
  full_name: string;
  email: string;
  is_phone_verified: boolean;
  is_coach: boolean;
  created_at: string;
}

export interface LoginCredentials {
  phone: string;
  password: string;
}

export interface RegisterData {
  phone: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface AuthResponse extends User, AuthTokens {}

// Profile Types
export interface PlayerProfile {
  id: string;
  user_id: string;
  phone: string;
  full_name: string;
  ntrp_rating: number;
  play_style: string;
  play_style_display: string;
  handedness: string;
  handedness_display: string;
  years_experience: number;
  height_cm?: number;
  weight_kg?: number;
  bio: string;
  avatar?: string;
  city: string;
  matches_played: number;
  matches_won: number;
  win_rate: number;
  created_at: string;
}

export interface CoachProfile {
  id: string;
  user_id: string;
  phone: string;
  full_name: string;
  is_verified: boolean;
  certification: string;
  years_experience: number;
  hourly_rate?: number;
  specialties: string[];
  bio: string;
  avatar?: string;
  city: string;
  available_days: string[];
  total_students: number;
  rating: number;
  created_at: string;
}

// Court Types
export type SurfaceType = 'hard' | 'clay' | 'grass' | 'carpet' | 'artificial';

export interface Court {
  id: string;
  name: string;
  city: string;
  address: string;
  surface_type: SurfaceType;
  surface_type_display: string;
  indoor: boolean;
  has_lights: boolean;
  price_per_hour: number;
  has_parking: boolean;
  has_showers: boolean;
  has_locker_room: boolean;
  has_equipment_rental: boolean;
  average_rating: number;
  total_ratings: number;
  main_image?: string;
  lat?: number;
  lng?: number;
  description?: string;
  phone?: string;
  website?: string;
  is_active: boolean;
  created_at: string;
}

export interface CourtReview {
  id: string;
  user_name: string;
  rating: number;
  comment: string;
  created_at: string;
}

// Match Types
export type MatchStatus = 'pending' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled' | 'no_show';
export type MatchType = 'singles' | 'doubles';

export interface Match {
  id: string;
  title: string;
  description: string;
  match_type: MatchType;
  match_type_display: string;
  status: MatchStatus;
  status_display: string;
  scheduled_at: string;
  duration_minutes: number;
  court?: Court;
  court_name: string;
  organizer: {
    id: string;
    name: string;
    phone: string;
  };
  opponent?: {
    id: string;
    name: string;
    phone: string;
  };
  ntrp_min?: number;
  ntrp_max?: number;
  is_public: boolean;
  can_join: boolean;
  is_organizer: boolean;
  organizer_score?: number;
  opponent_score?: number;
  set_scores: number[][];
  winner?: {
    id: string;
    name: string;
  };
  created_at: string;
}

export interface MatchStats {
  total_matches: number;
  won: number;
  lost: number;
  win_rate: number;
}

// Training Types
export type DrillCategory = 'forehand' | 'backhand' | 'serve' | 'volley' | 'footwork' | 'conditioning' | 'strategy' | 'warmup';
export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced' | 'professional';
export type IntensityLevel = 'low' | 'medium' | 'high' | 'very_high';

export interface Drill {
  id: string;
  name: string;
  category: DrillCategory;
  category_display: string;
  difficulty: DifficultyLevel;
  difficulty_display: string;
  duration_minutes: number;
  description: string;
  instructions: string;
  tips?: string;
  equipment_needed: string[];
  video_url?: string;
  image?: string;
  usage_count: number;
  created_by?: {
    id: string;
    name: string;
  };
  is_public: boolean;
}

export interface TrainingSession {
  id: string;
  title: string;
  date: string;
  duration_minutes: number;
  intensity: IntensityLevel;
  intensity_display: string;
  location_name: string;
  court?: Court;
  notes: string;
  feeling_score?: number;
  coach?: User;
  drills: TrainingDrill[];
  created_at: string;
}

export interface TrainingDrill {
  id: string;
  drill_id: string;
  drill_name: string;
  sets: number;
  reps_per_set: number;
  duration_minutes?: number;
  success_rate?: number;
  notes: string;
}

export interface TrainingGoal {
  id: string;
  title: string;
  description: string;
  target_value: number;
  current_value: number;
  progress_percentage: number;
  start_date: string;
  end_date?: string;
  status: 'active' | 'completed' | 'abandoned';
  status_display: string;
  created_at: string;
}

export interface TrainingStats {
  total_sessions: number;
  total_hours: number;
  total_minutes: number;
  this_week_sessions: number;
}

// UI Types
export interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'match' | 'court' | 'training' | 'system';
  read: boolean;
  created_at: string;
}