import { useLocalStorage } from './useLocalStorage';

export interface OnboardingProgress {
  step: number;
  categories: string[];
  completedAt?: string;
}

export function useOnboardingProgress() {
  const [progress, setProgress, clearProgress] = useLocalStorage<OnboardingProgress>('onboarding_progress', {
    step: 1,
    categories: [],
  });

  const updateStep = (step: number) => {
    setProgress(prev => ({ ...prev, step }));
  };

  const updateCategories = (categories: string[]) => {
    setProgress(prev => ({ ...prev, categories }));
  };

  const markCompleted = () => {
    setProgress(prev => ({ 
      ...prev, 
      completedAt: new Date().toISOString() 
    }));
  };

  const resetProgress = () => {
    clearProgress();
  };

  const isCompleted = Boolean(progress.completedAt);

  return {
    progress,
    updateStep,
    updateCategories,
    markCompleted,
    resetProgress,
    isCompleted,
  };
}