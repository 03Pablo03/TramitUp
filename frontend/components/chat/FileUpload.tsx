"use client";

import React, { useState, useRef, useCallback } from 'react';
import { 
  CloudArrowUpIcon, 
  DocumentIcon, 
  XMarkIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline';

export interface AttachedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  file: File;
  preview?: string;
}

interface FileUploadProps {
  onFilesSelected: (files: AttachedFile[]) => void;
  onFileRemoved: (fileId: string) => void;
  attachedFiles: AttachedFile[];
  maxFiles?: number;
  maxSizeBytes?: number;
  acceptedTypes?: string[];
  disabled?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFilesSelected,
  onFileRemoved,
  attachedFiles,
  maxFiles = 5,
  maxSizeBytes = 10 * 1024 * 1024, // 10MB
  acceptedTypes = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/png',
    'image/jpg'
  ],
  disabled = false
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): string | null => {
    if (file.size > maxSizeBytes) {
      return `El archivo "${file.name}" es demasiado grande. Máximo ${Math.round(maxSizeBytes / 1024 / 1024)}MB.`;
    }

    if (!acceptedTypes.includes(file.type)) {
      return `El tipo de archivo "${file.type}" no está permitido.`;
    }

    return null;
  };

  const processFiles = useCallback(async (files: FileList) => {
    if (disabled || uploading) return;

    setError(null);
    setUploading(true);

    const newFiles: AttachedFile[] = [];
    const errors: string[] = [];

    // Verificar límite de archivos
    if (attachedFiles.length + files.length > maxFiles) {
      setError(`Máximo ${maxFiles} archivos permitidos.`);
      setUploading(false);
      return;
    }

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      
      // Validar archivo
      const validationError = validateFile(file);
      if (validationError) {
        errors.push(validationError);
        continue;
      }

      // Verificar duplicados
      const isDuplicate = attachedFiles.some(
        existing => existing.name === file.name && existing.size === file.size
      );
      
      if (isDuplicate) {
        errors.push(`El archivo "${file.name}" ya está adjunto.`);
        continue;
      }

      // Crear objeto de archivo adjunto
      const attachedFile: AttachedFile = {
        id: `${Date.now()}-${i}`,
        name: file.name,
        size: file.size,
        type: file.type,
        file: file
      };

      // Generar preview para imágenes
      if (file.type.startsWith('image/')) {
        try {
          const preview = await createImagePreview(file);
          attachedFile.preview = preview;
        } catch (err) {
          console.warn('Error creating image preview:', err);
        }
      }

      newFiles.push(attachedFile);
    }

    if (errors.length > 0) {
      setError(errors.join(' '));
    }

    if (newFiles.length > 0) {
      onFilesSelected(newFiles);
    }

    setUploading(false);
  }, [attachedFiles, maxFiles, maxSizeBytes, acceptedTypes, disabled, uploading, onFilesSelected]);

  const createImagePreview = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled && !uploading) {
      setIsDragOver(true);
    }
  }, [disabled, uploading]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    if (disabled || uploading) return;

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      processFiles(files);
    }
  }, [disabled, uploading, processFiles]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      processFiles(files);
    }
    
    // Limpiar input para permitir seleccionar el mismo archivo nuevamente
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, [processFiles]);

  const handleRemoveFile = (fileId: string) => {
    onFileRemoved(fileId);
    setError(null);
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (fileType: string) => {
    if (fileType.includes('pdf')) {
      return <DocumentIcon className="h-8 w-8 text-red-500" />;
    } else if (fileType.includes('word') || fileType.includes('document')) {
      return <DocumentIcon className="h-8 w-8 text-blue-500" />;
    } else if (fileType.startsWith('image/')) {
      return <DocumentIcon className="h-8 w-8 text-green-500" />;
    }
    return <DocumentIcon className="h-8 w-8 text-gray-500" />;
  };

  return (
    <div className="space-y-4">
      {/* Área de carga */}
      <div
        className={`
          relative border-2 border-dashed rounded-lg p-6 text-center transition-colors
          ${isDragOver 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
          }
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !disabled && !uploading && fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={acceptedTypes.join(',')}
          onChange={handleFileSelect}
          className="hidden"
          disabled={disabled || uploading}
        />

        <div className="space-y-2">
          <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
          
          {uploading ? (
            <div className="space-y-2">
              <div className="animate-spin rounded-full h-6 w-6 border-2 border-blue-600 border-t-transparent mx-auto"></div>
              <p className="text-sm text-gray-600">Procesando archivos...</p>
            </div>
          ) : (
            <>
              <p className="text-lg font-medium text-gray-900">
                {isDragOver ? 'Suelta los archivos aquí' : 'Arrastra archivos o haz clic para seleccionar'}
              </p>
              <p className="text-sm text-gray-600">
                PDF, DOCX, JPG, PNG hasta {Math.round(maxSizeBytes / 1024 / 1024)}MB
              </p>
              <p className="text-xs text-gray-500">
                Máximo {maxFiles} archivos
              </p>
            </>
          )}
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

      {/* Lista de archivos adjuntos */}
      {attachedFiles.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium text-gray-900">
            Archivos adjuntos ({attachedFiles.length}/{maxFiles})
          </h4>
          
          <div className="space-y-2">
            {attachedFiles.map((file) => (
              <div
                key={file.id}
                className="flex items-center space-x-3 p-3 bg-gray-50 border border-gray-200 rounded-lg"
              >
                {/* Icono o preview */}
                <div className="flex-shrink-0">
                  {file.preview ? (
                    <img
                      src={file.preview}
                      alt={file.name}
                      className="h-10 w-10 rounded object-cover"
                    />
                  ) : (
                    getFileIcon(file.type)
                  )}
                </div>

                {/* Información del archivo */}
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {file.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {formatFileSize(file.size)}
                  </p>
                </div>

                {/* Botón eliminar */}
                <button
                  onClick={() => handleRemoveFile(file.id)}
                  className="flex-shrink-0 p-1 text-gray-400 hover:text-red-600 rounded transition-colors"
                  title="Eliminar archivo"
                >
                  <XMarkIcon className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export { FileUpload };
export default FileUpload;