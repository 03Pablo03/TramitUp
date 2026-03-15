import { useState, useCallback } from 'react';
import { FormState } from '@/types';

export function useFormState(initialState: Partial<FormState> = {}) {
  const [state, setState] = useState<FormState>({
    loading: false,
    error: null,
    success: false,
    ...initialState,
  });

  const setLoading = useCallback((loading: boolean) => {
    setState(prev => ({ ...prev, loading, error: null }));
  }, []);

  const setError = useCallback((error: string | null) => {
    setState(prev => ({ ...prev, error, loading: false, success: false }));
  }, []);

  const setSuccess = useCallback((success: boolean) => {
    setState(prev => ({ ...prev, success, loading: false, error: null }));
  }, []);

  const reset = useCallback(() => {
    setState({ loading: false, error: null, success: false });
  }, []);

  const handleAsync = useCallback(async <T>(
    asyncFn: () => Promise<T>,
    onSuccess?: (result: T) => void,
    onError?: (error: Error) => void
  ): Promise<T | undefined> => {
    try {
      setLoading(true);
      const result = await asyncFn();
      setSuccess(true);
      onSuccess?.(result);
      return result;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
      setError(errorMessage);
      onError?.(error instanceof Error ? error : new Error(errorMessage));
      return undefined;
    }
  }, [setLoading, setSuccess, setError]);

  return {
    ...state,
    setLoading,
    setError,
    setSuccess,
    reset,
    handleAsync,
  };
}