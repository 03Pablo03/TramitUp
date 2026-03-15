export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
}

export interface ApiError {
  error: string;
  details?: Record<string, any>;
  status?: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export interface UserProfileResponse {
  id: string;
  name: string | null;
  email: string | null;
  plan: string;
  categories_interest: string[];
  onboarding_completed: boolean;
  documents_used_today: number;
  remaining_chats_today: number;
}

export interface ConversationResponse {
  conversations: {
    id: string;
    title: string;
    category?: string;
    created_at: string;
  }[];
}

export interface MessageResponse {
  messages: {
    role: 'user' | 'assistant';
    content: string;
  }[];
}

export interface AlertResponse {
  id: string;
  title: string;
  description: string;
  due_date: string;
  status: 'active' | 'dismissed' | 'expired';
  urgency: 'low' | 'medium' | 'high';
  created_at: string;
}