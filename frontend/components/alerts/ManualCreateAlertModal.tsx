"use client";

import React, { useState } from 'react';
import { XMarkIcon, ExclamationTriangleIcon, CalendarIcon } from '@heroicons/react/24/outline';

interface ManualCreateAlertModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreateAlert: (alertData: {
    description: string;
    deadline_date: string;
    law_reference?: string;
    manual_priority: 'high' | 'medium' | 'low';
    notify_days_before: number[];
  }) => Promise<void>;
}

const ManualCreateAlertModal: React.FC<ManualCreateAlertModalProps> = ({
  isOpen,
  onClose,
  onCreateAlert
}) => {
  const [formData, setFormData] = useState({
    description: '',
    deadline_date: '',
    law_reference: '',
    manual_priority: 'medium' as 'high' | 'medium' | 'low',
    notify_days_before: [7, 3, 1]
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.description.trim()) {
      setError('La descripción es obligatoria');
      return;
    }
    
    if (!formData.deadline_date) {
      setError('La fecha límite es obligatoria');
      return;
    }

    // Validar que la fecha no sea en el pasado
    const selectedDate = new Date(formData.deadline_date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (selectedDate < today) {
      setError('La fecha límite no puede ser en el pasado');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await onCreateAlert(formData);
      
      // Resetear formulario
      setFormData({
        description: '',
        deadline_date: '',
        law_reference: '',
        manual_priority: 'medium',
        notify_days_before: [7, 3, 1]
      });
      
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error creando la alerta');
    } finally {
      setLoading(false);
    }
  };

  const handleNotificationChange = (days: number, checked: boolean) => {
    if (checked) {
      setFormData(prev => ({
        ...prev,
        notify_days_before: [...prev.notify_days_before, days].sort((a, b) => b - a)
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        notify_days_before: prev.notify_days_before.filter(d => d !== days)
      }));
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Nueva Alerta</h2>
          <button
            onClick={onClose}
            className="p-1 text-gray-400 hover:text-gray-600 rounded"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Descripción *
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              placeholder="Ej: Presentar recurso de multa de tráfico"
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>

          {/* Deadline Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Fecha límite *
            </label>
            <div className="relative">
              <input
                type="date"
                value={formData.deadline_date}
                onChange={(e) => setFormData(prev => ({ ...prev, deadline_date: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
              <CalendarIcon className="absolute right-3 top-2.5 h-5 w-5 text-gray-400 pointer-events-none" />
            </div>
          </div>

          {/* Law Reference */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Referencia legal (opcional)
            </label>
            <input
              type="text"
              value={formData.law_reference}
              onChange={(e) => setFormData(prev => ({ ...prev, law_reference: e.target.value }))}
              placeholder="Ej: Art. 94 Ley 39/2015"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Priority */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Prioridad
            </label>
            <div className="grid grid-cols-3 gap-2">
              {(['high', 'medium', 'low'] as const).map((priority) => (
                <button
                  key={priority}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, manual_priority: priority }))}
                  className={`px-3 py-2 text-sm font-medium rounded-lg border transition-colors ${
                    formData.manual_priority === priority
                      ? getPriorityColor(priority)
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {priority === 'high' ? 'Alta' : priority === 'medium' ? 'Media' : 'Baja'}
                </button>
              ))}
            </div>
          </div>

          {/* Notification Settings */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Notificar con antelación
            </label>
            <div className="space-y-2">
              {[30, 15, 7, 3, 1].map((days) => (
                <label key={days} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.notify_days_before.includes(days)}
                    onChange={(e) => handleNotificationChange(days, e.target.checked)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">
                    {days === 1 ? '1 día antes' : `${days} días antes`}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="flex items-start space-x-2 p-3 bg-red-50 border border-red-200 rounded-lg">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-red-900">Error</p>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="inline-block animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                  Creando...
                </>
              ) : (
                'Crear Alerta'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export { ManualCreateAlertModal };
export default ManualCreateAlertModal;