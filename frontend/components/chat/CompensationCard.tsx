import React from 'react';
import { Euro, CheckCircle, XCircle, Info } from 'lucide-react';
import { Plane } from '@/lib/icons';

interface CompensationCardProps {
  amountEur?: number;
  reducedAmountEur?: number;
  applies: boolean;
  reason: string;
}

export default function CompensationCard({
  amountEur,
  reducedAmountEur,
  applies,
  reason,
}: CompensationCardProps) {
  return (
    <div className={`border-l-4 rounded-xl p-5 shadow-sm ${
      applies 
        ? 'bg-green-50 border-green-500' 
        : 'bg-red-50 border-red-500'
    }`}>
      <div className="flex items-start gap-3">
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          applies ? 'bg-green-100' : 'bg-red-100'
        }`}>
          <Euro className={`w-5 h-5 ${applies ? 'text-green-600' : 'text-red-600'}`} />
        </div>
        
        <div className="flex-1 space-y-3">
          <div>
            <h3 className={`font-semibold text-sm mb-1 ${applies ? 'text-green-900' : 'text-red-900'}`}>
              <Plane className="inline h-4 w-4 mr-1" /> Compensación por vuelo
            </h3>
            
            <div className="flex items-center gap-2">
              {applies ? (
                <>
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span className="font-medium text-green-800 text-sm">
                    Tienes derecho a compensación
                  </span>
                </>
              ) : (
                <>
                  <XCircle className="w-4 h-4 text-red-600" />
                  <span className="font-medium text-red-800 text-sm">
                    No hay derecho a compensación
                  </span>
                </>
              )}
            </div>
          </div>

          {/* Importe */}
          {applies && amountEur && (
            <div className="bg-green-100 border border-green-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-green-800 font-medium text-sm">Importe estimado:</span>
                <span className="text-2xl font-bold text-green-900">
                  {amountEur}€
                </span>
              </div>
              {reducedAmountEur && reducedAmountEur !== amountEur && (
                <div className="text-sm text-green-700">
                  <span className="font-medium">Importe reducido:</span> {reducedAmountEur}€
                  <div className="text-xs mt-1 opacity-80">
                    Si la aerolínea ofrece transporte alternativo con menos retraso
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Razón */}
          <div className={`rounded-lg p-3 border ${
            applies 
              ? 'bg-green-100 border-green-200' 
              : 'bg-red-100 border-red-200'
          }`}>
            <div className="flex items-start gap-2">
              <Info className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                applies ? 'text-green-600' : 'text-red-600'
              }`} />
              <p className={`text-sm leading-relaxed ${
                applies ? 'text-green-800' : 'text-red-800'
              }`}>
                {reason}
              </p>
            </div>
          </div>

          {/* Información legal */}
          {applies && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p className="text-xs text-blue-700 leading-relaxed">
                <span className="font-medium">Reglamento (CE) 261/2004:</span> Esta compensación es independiente 
                del reembolso del billete y otros gastos. Tienes hasta 1 año para reclamar.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}