import React from 'react';
import { ExternalLink, Building2, Shield, Mail } from 'lucide-react';
import { ClipboardList, CheckCircle, Info } from '@/lib/icons';

interface PortalCardProps {
  portalKey: string;
  name: string;
  url: string;
  needsDigitalCert: boolean;
  alsoByPost: boolean;
  notes?: string;
  officialFormUrl?: string | null;
}

export default function PortalCard({
  portalKey,
  name,
  url,
  needsDigitalCert,
  alsoByPost,
  notes,
  officialFormUrl,
}: PortalCardProps) {
  return (
    <div className="bg-green-50 border-l-4 border-green-500 rounded-xl p-5 shadow-sm">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
          <Building2 className="w-5 h-5 text-green-600" />
        </div>
        
        <div className="flex-1 space-y-3">
          <div>
            <h3 className="font-semibold text-green-900 text-sm mb-1">
              <ClipboardList className="inline h-4 w-4 mr-1" />
              Donde presentar tu reclamacion
            </h3>
            <p className="font-bold text-gray-900">{name}</p>
          </div>
          
          <div className="flex flex-wrap gap-2">
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
            >
              <span>Ir al portal oficial</span>
              <ExternalLink className="w-4 h-4" />
            </a>
            {officialFormUrl && officialFormUrl !== url && (
              <a
                href={officialFormUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 border border-green-600 text-green-700 hover:bg-green-50 px-4 py-2 rounded-lg font-medium text-sm transition-colors"
              >
                <span className="inline-flex items-center gap-1"><ClipboardList className="h-4 w-4" /> Formulario oficial</span>
                <ExternalLink className="w-4 h-4" />
              </a>
            )}
          </div>

          <div className="flex flex-wrap gap-2">
            {needsDigitalCert ? (
              <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800 border border-orange-200">
                <Shield className="w-3 h-3" />
                <span>Requiere Cl@ve</span>
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200">
                <CheckCircle className="w-3 h-3" />
                <span>Sin certificado digital</span>
              </span>
            )}

            {alsoByPost && (
              <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 border border-gray-200">
                <Mail className="w-3 h-3" />
                <span>También por correo postal</span>
              </span>
            )}
          </div>

          {notes && (
            <div className="bg-green-100 border border-green-200 rounded-lg p-3">
              <p className="text-sm text-green-800 leading-relaxed">
                <span className="font-medium inline-flex items-center gap-1"><Info className="h-4 w-4" /> Nota importante:</span> {notes}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}