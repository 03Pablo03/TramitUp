"use client";

import React, { useState, useEffect } from 'react';
import { 
  LightBulbIcon, 
  ClockIcon, 
  DocumentTextIcon, 
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XMarkIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline';

interface ProactiveSuggestion {
  id: string;
  type: string;
  priority: string;
  title: string;
  description: string;
  action_text: string;
  action_data: Record<string, any>;
  context: Record<string, any>;
  expires_at?: string;
  created_at: string;
}

interface ProactiveSuggestionsPanelProps {
  userId: string;
  conversationContext?: string;
  attachmentIds?: string[];
  onSuggestionAction?: (suggestionId: string, actionData: Record<string, any>) => void;
}

const ProactiveSuggestionsPanel: React.FC<ProactiveSuggestionsPanelProps> = ({
  userId,
  conversationContext,
  attachmentIds = [],
  onSuggestionAction
}) => {
  const [suggestions, setSuggestions] = useState<ProactiveSuggestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dismissedSuggestions, setDismissedSuggestions] = useState<Set<string>>(new Set());

  useEffect(() => {
    loadSuggestions();
  }, [userId, conversationContext, attachmentIds]);

  const loadSuggestions = async () => {
    try {
      setLoading(true);
      setError(null);

      let endpoint = '/api/backend/suggestions/suggestions?limit=10';
      
      // Si hay contexto de conversación, usar endpoint contextual
      if (conversationContext || attachmentIds.length > 0) {
        const response = await fetch('/api/backend/suggestions/contextual', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            conversation_context: conversationContext || '',
            attachment_ids: attachmentIds
          })
        });

        if (response.ok) {
          const data = await response.json();
          setSuggestions(data.suggestions || []);
        } else {
          throw new Error('Error obteniendo sugerencias contextuales');
        }
      } else {
        // Usar endpoint general
        const response = await fetch(endpoint);
        
        if (response.ok) {
          const data = await response.json();
          setSuggestions(data || []);
        } else {
          throw new Error('Error obteniendo sugerencias');
        }
      }
    } catch (err) {
      console.error('Error loading suggestions:', err);
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionAction = async (suggestion: ProactiveSuggestion) => {
    try {
      // Marcar como ejecutada
      await fetch('/api/backend/suggestions/interact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          suggestion_id: suggestion.id,
          action: 'acted',
          action_data: suggestion.action_data
        })
      });

      // Ejecutar acción personalizada si se proporciona
      if (onSuggestionAction) {
        onSuggestionAction(suggestion.id, suggestion.action_data);
      }

      // Remover sugerencia de la lista
      setSuggestions(prev => prev.filter(s => s.id !== suggestion.id));
    } catch (err) {
      console.error('Error executing suggestion action:', err);
    }
  };

  const handleDismissSuggestion = async (suggestionId: string) => {
    try {
      await fetch('/api/backend/suggestions/interact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          suggestion_id: suggestionId,
          action: 'dismissed'
        })
      });

      // Añadir a dismissed localmente
      setDismissedSuggestions(prev => {
        const newSet = new Set(prev);
        newSet.add(suggestionId);
        return newSet;
      });
    } catch (err) {
      console.error('Error dismissing suggestion:', err);
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'critical':
        return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />;
      case 'high':
        return <ExclamationTriangleIcon className="h-5 w-5 text-orange-500" />;
      case 'medium':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />;
      case 'low':
        return <InformationCircleIcon className="h-5 w-5 text-blue-500" />;
      case 'info':
        return <InformationCircleIcon className="h-5 w-5 text-gray-500" />;
      default:
        return <LightBulbIcon className="h-5 w-5 text-blue-500" />;
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'document_template':
        return <DocumentTextIcon className="h-4 w-4" />;
      case 'legal_deadline':
        return <ClockIcon className="h-4 w-4" />;
      default:
        return <LightBulbIcon className="h-4 w-4" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical':
        return 'border-red-200 bg-red-50';
      case 'high':
        return 'border-orange-200 bg-orange-50';
      case 'medium':
        return 'border-yellow-200 bg-yellow-50';
      case 'low':
        return 'border-blue-200 bg-blue-50';
      case 'info':
        return 'border-gray-200 bg-gray-50';
      default:
        return 'border-gray-200 bg-white';
    }
  };

  // Filtrar sugerencias descartadas
  const visibleSuggestions = suggestions.filter(s => !dismissedSuggestions.has(s.id));

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="animate-pulse">
          <div className="flex items-center space-x-2 mb-3">
            <div className="h-5 w-5 bg-gray-300 rounded"></div>
            <div className="h-4 w-32 bg-gray-300 rounded"></div>
          </div>
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="border border-gray-200 rounded-lg p-3">
                <div className="h-4 w-3/4 bg-gray-300 rounded mb-2"></div>
                <div className="h-3 w-full bg-gray-300 rounded"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-red-200 p-4">
        <div className="flex items-center space-x-2 text-red-600">
          <ExclamationTriangleIcon className="h-5 w-5" />
          <span className="text-sm font-medium">Error cargando sugerencias</span>
        </div>
        <p className="text-sm text-red-500 mt-1">{error}</p>
        <button
          onClick={loadSuggestions}
          className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
        >
          Reintentar
        </button>
      </div>
    );
  }

  if (visibleSuggestions.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="flex items-center space-x-2 text-gray-500">
          <LightBulbIcon className="h-5 w-5" />
          <span className="text-sm font-medium">Sugerencias Inteligentes</span>
        </div>
        <p className="text-sm text-gray-400 mt-2">
          No hay sugerencias disponibles en este momento.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="px-4 py-3 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <LightBulbIcon className="h-5 w-5 text-blue-600" />
            <h3 className="text-sm font-medium text-gray-900">
              Sugerencias Inteligentes
            </h3>
          </div>
          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
            {visibleSuggestions.length}
          </span>
        </div>
      </div>

      <div className="p-4 space-y-3 max-h-96 overflow-y-auto">
        {visibleSuggestions.map((suggestion) => (
          <div
            key={suggestion.id}
            className={`border rounded-lg p-3 transition-all hover:shadow-sm ${getPriorityColor(suggestion.priority)}`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  {getPriorityIcon(suggestion.priority)}
                  <div className="flex items-center space-x-1">
                    {getTypeIcon(suggestion.type)}
                    <h4 className="text-sm font-medium text-gray-900">
                      {suggestion.title}
                    </h4>
                  </div>
                </div>
                
                <p className="text-sm text-gray-600 mb-3">
                  {suggestion.description}
                </p>

                <div className="flex items-center justify-between">
                  <button
                    onClick={() => handleSuggestionAction(suggestion)}
                    className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-800 font-medium"
                  >
                    <span>{suggestion.action_text}</span>
                    <ChevronRightIcon className="h-4 w-4" />
                  </button>

                  {suggestion.expires_at && (
                    <span className="text-xs text-gray-400">
                      Expira: {new Date(suggestion.expires_at).toLocaleDateString()}
                    </span>
                  )}
                </div>
              </div>

              <button
                onClick={() => handleDismissSuggestion(suggestion.id)}
                className="ml-2 p-1 text-gray-400 hover:text-gray-600 rounded"
                title="Descartar sugerencia"
              >
                <XMarkIcon className="h-4 w-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="px-4 py-2 border-t border-gray-200 bg-gray-50 rounded-b-lg">
        <p className="text-xs text-gray-500 text-center">
          Sugerencias basadas en tu actividad y patrones de uso
        </p>
      </div>
    </div>
  );
};

export default ProactiveSuggestionsPanel;