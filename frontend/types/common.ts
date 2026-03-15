export interface BaseEntity {
  id: string;
  created_at: string;
  updated_at?: string;
}

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface FormState {
  loading: boolean;
  error: string | null;
  success: boolean;
}

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface TabItem {
  id: string;
  label: string;
  count?: number;
}

export interface StepItem {
  title: string;
  content: string;
  completed?: boolean;
}

export interface FAQItem {
  q: string;
  a: string;
}

export interface SEOLandingProps {
  title: string;
  description: string;
  h1: string;
  intro: string;
  steps?: StepItem[];
  lawRefs?: string[];
  faqs?: FAQItem[];
  ctaText?: string;
}