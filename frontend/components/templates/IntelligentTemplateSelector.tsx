"use client";

import React, { useState, useEffect } from 'react';
import {
  DocumentTextIcon,
  SparklesIcon,
  EyeIcon,
  ArrowDownTrayIcon,
  CheckCircleIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline';

interface Template {
  id: string;
  name: string;
  description: string;
  document_type: string;
  sections_count: number;
  ai_enhanced: boolean;
}

interface TemplatePreview {
  template_name: string;
  sections: Array<{
    title: string;
    content_preview: string;
    required: boolean;
    order: number;
  }>;
  total_sections: number;
  ai_enhancement: boolean;
}

interface IntelligentTemplateSelectorProps {
  conversationContext?: string;
  attachmentIds?: string[];
  onTemplateGenerated?: (result: any) => void;
}

const IntelligentTemplateSelector: React.FC<IntelligentTemplateSelectorProps> = ({
  conversationContext = '',
  attachmentIds = [],
  onTemplateGenerated
}) => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const [preview, setPreview] = useState<TemplatePreview | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<any>(null);

  useEffect(() => {
    loadTemplates();
    if (conversationContext || attachmentIds.length > 0) {
      analyzeContext();
    }
  }, []);

  const loadTemplates = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/backend/templates/templates');
      
      if (response.ok) {
        const data = await response.json();
        setTemplates(data);
      } else {
        throw new Error('Error cargando plantillas');
      }
    } catch (err) {
      console.error('Error loading templates:', err);
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  const analyzeContext = async () => {
    try {
      const response = await fetch('/api/backend/templates/analyze-context', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_context: conversationContext,
          attachment_ids: attachmentIds
        })
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysis(data);
        
        // Auto-seleccionar plantilla sugerida si tiene alta confianza
        if (data.suggested_template?.confidence > 0.7) {
          setSelectedTemplate(data.suggested_template.template_id);
          await loadPreview(data.suggested_template.template_id, data.suggested_fields);
        }
      }
    } catch (err) {
      console.error('Error analyzing context:', err);
    }
  };

  const loadPreview = async (templateId: string, sampleFields: Record<string, any> = {}) => {
    try {
      const response = await fetch('/api/backend/templates/preview', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template_id: templateId,
          sample_fields: sampleFields
        })
      });

      if (response.ok) {
        const data = await response.json();
        setPreview(data);
      } else {
        throw new Error('Error cargando vista previa');
      }
    } catch (err) {
      console.error('Error loading preview:', err);
    }
  };

  const generateDocument = async () => {
    if (!selectedTemplate) return;

    try {
      setGenerating(true);
      setError(null);

      const response = await fetch('/api/backend/templates/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template_id: selectedTemplate,
          conversation_context: conversationContext,
          attachment_ids: attachmentIds,
          custom_fields: analysis?.suggested_fields || {}
        })
      });

      if (response.ok) {
        const result = await response.json();
        
        if (onTemplateGenerated) {
          onTemplateGenerated(result);
        }

        // Mostrar mensaje de éxito
        setError(null);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error generando documento');
      }
    } catch (err) {
      console.error('Error generating document:', err);
      setError(err instanceof Error ? err.message : 'Error generando documento');
    } finally {
      setGenerating(false);
    }
  };

  const handleTemplateSelect = async (templateId: string) => {
    setSelectedTemplate(templateId);
    setPreview(null);
    
    // Cargar vista previa con campos sugeridos si están disponibles
    const sampleFields = analysis?.suggested_fields || {};
    await loadPreview(templateId, sampleFields);
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="flex items-center space-x-2 mb-4">
            <div className="h-6 w-6 bg-gray-300 rounded"></div>
            <div className="h-5 w-40 bg-gray-300 rounded"></div>
          </div>
          <div className="grid gap-4">
            {[1, 2].map(i => (
              <div key={i} className="border border-gray-200 rounded-lg p-4">
                <div className="h-4 w-3/4 bg-gray-300 rounded mb-2"></div>
                <div className="h-3 w-full bg-gray-300 rounded"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <SparklesIcon className="h-6 w-6 text-purple-600" />
          <h3 className="text-lg font-semibold text-gray-900">
            Plantillas Inteligentes
          </h3>
        </div>
        <p className="text-sm text-gray-600 mt-1">
          Genera documentos adaptativos basados en tu contexto y documentos adjuntos
        </p>
      </div>

      <div className="p-6">
        {/* Análisis de contexto */}
        {analysis && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start space-x-2">
              <CheckCircleIcon className="h-5 w-5 text-blue-600 mt-0.5" />
              <div>
                <h4 className="text-sm font-medium text-blue-900">
                  Análisis Completado
                </h4>
                <p className="text-sm text-blue-700 mt-1">
                  {analysis.analysis_summary}
                </p>
                {analysis.suggested_template && (
                  <div className="mt-2">
                    <span className="text-sm text-blue-600">
                      Plantilla recomendada: <strong>{analysis.suggested_template.template_id}</strong>
                    </span>
                    <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                      {Math.round(analysis.suggested_template.confidence * 100)}% confianza
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Lista de plantillas */}
        <div className="grid gap-4 mb-6">
          {templates.map((template) => (
            <div
              key={template.id}
              className={`border rounded-lg p-4 cursor-pointer transition-all ${
                selectedTemplate === template.id
                  ? 'border-purple-300 bg-purple-50 ring-1 ring-purple-300'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }`}
              onClick={() => handleTemplateSelect(template.id)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <DocumentTextIcon className="h-5 w-5 text-gray-600" />
                    <h4 className="font-medium text-gray-900">{template.name}</h4>
                    {template.ai_enhanced && (
                      <SparklesIcon className="h-4 w-4 text-purple-500" />
                    )}
                    {analysis?.suggested_template?.template_id === template.id && (
                      <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                        Recomendada
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{template.description}</p>
                  <div className="flex items-center space-x-4 text-xs text-gray-500">
                    <span>{template.sections_count} secciones</span>
                    <span className="capitalize">{template.document_type}</span>
                    {template.ai_enhanced && (
                      <span className="text-purple-600">IA mejorada</span>
                    )}
                  </div>
                </div>
                
                {selectedTemplate === template.id && (
                  <CheckCircleIcon className="h-5 w-5 text-purple-600" />
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Vista previa */}
        {preview && selectedTemplate && (
          <div className="mb-6 border border-gray-200 rounded-lg">
            <div className="px-4 py-3 border-b border-gray-200 bg-gray-50">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <EyeIcon className="h-5 w-5 text-gray-600" />
                  <h4 className="font-medium text-gray-900">Vista Previa</h4>
                </div>
                <span className="text-sm text-gray-600">
                  {preview.total_sections} secciones activas
                </span>
              </div>
            </div>
            
            <div className="p-4 max-h-64 overflow-y-auto">
              <div className="space-y-3">
                {preview.sections.map((section, index) => (
                  <div key={index} className="border-l-2 border-gray-200 pl-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <h5 className="text-sm font-medium text-gray-900">
                        {section.title}
                      </h5>
                      {section.required && (
                        <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full">
                          Requerida
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-gray-600 whitespace-pre-wrap">
                      {section.content_preview}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <ExclamationCircleIcon className="h-5 w-5 text-red-600" />
              <span className="text-sm font-medium text-red-900">Error</span>
            </div>
            <p className="text-sm text-red-700 mt-1">{error}</p>
          </div>
        )}

        {/* Botones de acción */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-200">
          <div className="text-sm text-gray-600">
            {selectedTemplate ? (
              <span>Plantilla seleccionada: <strong>{templates.find(t => t.id === selectedTemplate)?.name}</strong></span>
            ) : (
              <span>Selecciona una plantilla para continuar</span>
            )}
          </div>
          
          <div className="flex space-x-3">
            {selectedTemplate && preview && (
              <button
                onClick={generateDocument}
                disabled={generating}
                className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {generating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                    <span>Generando...</span>
                  </>
                ) : (
                  <>
                    <ArrowDownTrayIcon className="h-4 w-4" />
                    <span>Generar Documento</span>
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntelligentTemplateSelector;