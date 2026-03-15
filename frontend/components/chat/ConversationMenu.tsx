"use client";

import React, { useState, useRef, useEffect } from 'react';
import { 
  EllipsisVerticalIcon, 
  PencilIcon, 
  TrashIcon,
  CheckIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';

interface ConversationMenuProps {
  conversationId: string;
  conversationTitle: string;
  onRename: (id: string, newTitle: string) => void;
  onDelete: (id: string) => void;
  disabled?: boolean;
}

const ConversationMenu: React.FC<ConversationMenuProps> = ({
  conversationId,
  conversationTitle,
  onRename,
  onDelete,
  disabled = false
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isRenaming, setIsRenaming] = useState(false);
  const [newTitle, setNewTitle] = useState(conversationTitle);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  
  const menuRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Cerrar menú al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setShowDeleteConfirm(false);
        if (isRenaming) {
          setIsRenaming(false);
          setNewTitle(conversationTitle);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isRenaming, conversationTitle]);

  // Enfocar input cuando se activa el renombrado
  useEffect(() => {
    if (isRenaming && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [isRenaming]);

  const handleRename = () => {
    if (newTitle.trim() && newTitle.trim() !== conversationTitle) {
      onRename(conversationId, newTitle.trim());
    }
    setIsRenaming(false);
    setIsOpen(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleRename();
    } else if (e.key === 'Escape') {
      setIsRenaming(false);
      setNewTitle(conversationTitle);
      setIsOpen(false);
    }
  };

  const handleDelete = () => {
    onDelete(conversationId);
    setShowDeleteConfirm(false);
    setIsOpen(false);
  };

  if (isRenaming) {
    return (
      <div className="flex items-center space-x-1 px-2 py-1">
        <input
          ref={inputRef}
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          onKeyDown={handleKeyDown}
          className="flex-1 text-xs bg-white border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
          maxLength={100}
        />
        <button
          onClick={handleRename}
          className="p-1 text-green-600 hover:text-green-800 rounded"
          title="Guardar"
        >
          <CheckIcon className="h-3 w-3" />
        </button>
        <button
          onClick={() => {
            setIsRenaming(false);
            setNewTitle(conversationTitle);
          }}
          className="p-1 text-gray-400 hover:text-gray-600 rounded"
          title="Cancelar"
        >
          <XMarkIcon className="h-3 w-3" />
        </button>
      </div>
    );
  }

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={disabled}
        className="p-1 text-gray-400 hover:text-gray-600 rounded opacity-0 group-hover:opacity-100 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
        title="Opciones"
      >
        <EllipsisVerticalIcon className="h-4 w-4" />
      </button>

      {isOpen && (
        <div className="absolute right-0 top-6 bg-white border border-gray-200 rounded-lg shadow-lg z-10 min-w-[140px]">
          {!showDeleteConfirm ? (
            <>
              <button
                onClick={() => {
                  setIsRenaming(true);
                  setIsOpen(false);
                }}
                className="flex items-center space-x-2 w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-t-lg"
              >
                <PencilIcon className="h-4 w-4" />
                <span>Renombrar</span>
              </button>
              <button
                onClick={() => setShowDeleteConfirm(true)}
                className="flex items-center space-x-2 w-full px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-b-lg"
              >
                <TrashIcon className="h-4 w-4" />
                <span>Eliminar</span>
              </button>
            </>
          ) : (
            <div className="p-3">
              <p className="text-sm text-gray-900 mb-3">
                ¿Eliminar esta conversación?
              </p>
              <div className="flex justify-end space-x-2">
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  className="px-2 py-1 text-xs text-gray-600 hover:text-gray-800 rounded"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleDelete}
                  className="px-2 py-1 text-xs text-white bg-red-600 hover:bg-red-700 rounded"
                >
                  Eliminar
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export { ConversationMenu };
export default ConversationMenu;