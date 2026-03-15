"use client";

import { useEffect, useState } from "react";
import { X, AlertTriangle, Wifi, Clock, Server } from "lucide-react";

interface ErrorToastProps {
  error: string;
  onClose: () => void;
  autoClose?: boolean;
  duration?: number;
}

const getErrorDetails = (error: string) => {
  const errorLower = error.toLowerCase();
  
  if (errorLower.includes('network') || errorLower.includes('conexión') || errorLower.includes('internet')) {
    return {
      icon: <Wifi className="w-5 h-5" />,
      title: "Sin conexión",
      message: "Verifica tu internet e inténtalo de nuevo."
    };
  }
  
  if (errorLower.includes('rate limit') || errorLower.includes('límite')) {
    return {
      icon: <Clock className="w-5 h-5" />,
      title: "Límite alcanzado",
      message: "Has alcanzado el límite diario. Actualiza a PRO para continuar."
    };
  }
  
  if (errorLower.includes('server') || errorLower.includes('500') || errorLower.includes('502')) {
    return {
      icon: <Server className="w-5 h-5" />,
      title: "Error del servidor",
      message: "Algo salió mal. Estamos en ello. Inténtalo en unos segundos."
    };
  }
  
  return {
    icon: <AlertTriangle className="w-5 h-5" />,
    title: "Error",
    message: error
  };
};

export function ErrorToast({ 
  error, 
  onClose, 
  autoClose = true, 
  duration = 4000 
}: ErrorToastProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isLeaving, setIsLeaving] = useState(false);
  
  const { icon, title, message } = getErrorDetails(error);

  useEffect(() => {
    // Entrada con delay para animación
    const enterTimer = setTimeout(() => setIsVisible(true), 100);
    
    // Auto-close
    let autoCloseTimer: NodeJS.Timeout;
    if (autoClose) {
      autoCloseTimer = setTimeout(() => {
        handleClose();
      }, duration);
    }

    return () => {
      clearTimeout(enterTimer);
      if (autoCloseTimer) clearTimeout(autoCloseTimer);
    };
  }, [autoClose, duration]);

  const handleClose = () => {
    setIsLeaving(true);
    setTimeout(() => {
      onClose();
    }, 200); // Tiempo para animación de salida
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div
        className={`
          bg-red-50 border border-red-200 rounded-lg shadow-lg p-4 max-w-sm w-full
          transform transition-all duration-200 ease-out
          ${isVisible && !isLeaving 
            ? 'translate-y-0 opacity-100 scale-100' 
            : 'translate-y-2 opacity-0 scale-95'
          }
        `}
      >
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 text-red-600">
            {icon}
          </div>
          
          <div className="flex-1 min-w-0">
            <h4 className="text-sm font-medium text-red-900 mb-1">
              {title}
            </h4>
            <p className="text-sm text-red-700 leading-relaxed">
              {message}
            </p>
          </div>
          
          <button
            onClick={handleClose}
            className="flex-shrink-0 text-red-400 hover:text-red-600 transition-colors p-1 rounded-md hover:bg-red-100"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
        
        {/* Progress bar para auto-close */}
        {autoClose && (
          <div className="mt-3 h-1 bg-red-100 rounded-full overflow-hidden">
            <div 
              className="h-full bg-red-300 rounded-full transition-all ease-linear"
              style={{
                width: '100%',
                animation: `shrink ${duration}ms linear`
              }}
            />
          </div>
        )}
      </div>

      <style jsx>{`
        @keyframes shrink {
          from { width: 100%; }
          to { width: 0%; }
        }
      `}</style>
    </div>
  );
}