export interface DetectedDeadline {
  description: string;
  days: number;
  business_days: boolean;
  reference_date: string | null;
  law_reference: string;
  urgency: string;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  category?: string;
  subcategory?: string;
  detectedDeadlines?: DetectedDeadline[];
}

export interface Conversation {
  id: string;
  title: string;
  category?: string;
  created_at: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
}

export interface SSEEvent {
  type: 'conversation_id' | 'classification' | 'chunk' | 'detected_deadlines' | 'error';
  id?: string;
  category?: string;
  subcategory?: string;
  content?: string;
  deadlines?: DetectedDeadline[];
  message?: string;
}

export interface ChatWindowProps {
  messages: Message[];
  sending: boolean;
  currentCategory?: string;
  currentSubcategory?: string;
  onSend: (text: string) => void;
  hasDocumentAccess: boolean;
  hasAlertAccess: boolean;
  remainingChats?: number | null;
  userPlan: string;
}