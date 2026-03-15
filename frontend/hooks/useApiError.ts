import { useCallback } from 'react';
import { useNotifications } from '@/context/NotificationContext';

export interface ApiError {
  message: string;
  status?: number;
  code?: string;
}

export function useApiError() {
  const { showError, showWarning } = useNotifications();

  const handleError = useCallback((error: unknown, context?: string) => {
    let title = 'Error';
    let message = 'Ha ocurrido un error inesperado';

    if (error instanceof Error) {
      message = error.message;
    } else if (typeof error === 'string') {
      message = error;
    } else if (error && typeof error === 'object' && 'message' in error) {
      message = String((error as any).message);
    }

    // Personalizar mensajes según el contexto
    if (context) {
      switch (context) {
        case 'auth':
          title = 'Error de autenticación';
          break;
        case 'chat':
          title = 'Error en el chat';
          break;
        case 'api':
          title = 'Error de conexión';
          break;
        case 'validation':
          title = 'Error de validación';
          showWarning(title, message);
          return;
        default:
          title = `Error en ${context}`;
      }
    }

    // Logging en desarrollo
    if (process.env.NODE_ENV === 'development') {
      console.error(`[${context || 'Unknown'}] Error:`, error);
    }

    showError(title, message);
  }, [showError, showWarning]);

  const handleApiError = useCallback(async (response: Response, context?: string) => {
    let errorMessage = `Error ${response.status}`;
    
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorData.message || errorMessage;
    } catch {
      // Si no se puede parsear el JSON, usar el status text
      errorMessage = response.statusText || errorMessage;
    }

    // Personalizar mensajes según el código de estado
    switch (response.status) {
      case 401:
        errorMessage = 'No tienes autorización. Por favor, inicia sesión de nuevo.';
        break;
      case 403:
        errorMessage = 'No tienes permisos para realizar esta acción.';
        break;
      case 404:
        errorMessage = 'El recurso solicitado no fue encontrado.';
        break;
      case 429:
        errorMessage = 'Has superado el límite de solicitudes. Inténtalo más tarde.';
        break;
      case 500:
        errorMessage = 'Error interno del servidor. Inténtalo más tarde.';
        break;
      case 502:
        errorMessage = 'El servidor no está disponible. Comprueba tu conexión.';
        break;
      case 503:
        errorMessage = 'El servicio no está disponible temporalmente.';
        break;
    }

    handleError(errorMessage, context);
  }, [handleError]);

  const withErrorHandling = useCallback(<T extends any[], R>(
    fn: (...args: T) => Promise<R>,
    context?: string
  ) => {
    return async (...args: T): Promise<R | undefined> => {
      try {
        return await fn(...args);
      } catch (error) {
        handleError(error, context);
        return undefined;
      }
    };
  }, [handleError]);

  return {
    handleError,
    handleApiError,
    withErrorHandling,
  };
}