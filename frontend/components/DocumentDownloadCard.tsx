"use client";

const DOCUMENT_TYPE_LABELS: Record<string, string> = {
  reclamacion_aerolinea: "Reclamación a aerolínea",
  reclamacion_banco: "Reclamación a banco",
  reclamacion_seguro: "Reclamación a aseguradora",
  reclamacion_suministro_luz: "Reclamación suministro luz",
  reclamacion_suministro_internet: "Reclamación suministro internet",
  reclamacion_comercio: "Reclamación a comercio",
  recurso_multa_trafico: "Recurso multa tráfico",
  carta_disconformidad_finiquito: "Carta disconformidad finiquito",
  solicitud_certificado_empresa: "Solicitud certificado empresa",
  reclamacion_salarios: "Reclamación de salarios",
  solicitud_prestacion_desempleo: "Solicitud prestación desempleo",
  reclamacion_fianza: "Reclamación devolución fianza",
  burofax_arrendador: "Burofax arrendador",
  solicitud_informacion_comunidad: "Solicitud información comunidad",
  impugnacion_acuerdo_junta: "Impugnación acuerdo junta",
  recurso_reposicion_hacienda: "Recurso reposición Hacienda",
  solicitud_aplazamiento_hacienda: "Solicitud aplazamiento Hacienda",
  reclamacion_seguridad_social: "Reclamación Seguridad Social",
  solicitud_informacion_administrativa: "Solicitud información administrativa",
};

function formatDate(iso: string): string {
  try {
    const d = new Date(iso);
    return d.toLocaleDateString("es-ES", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  } catch {
    return iso;
  }
}

export type DocumentDownloadCardProps = {
  documentId: string;
  documentType: string;
  createdAt: string;
  pdfUrl?: string | null;
  docxUrl?: string | null;
  onRefreshUrls?: () => Promise<void>;
  /** Si se proporciona, se usa para obtener la URL al hacer clic cuando no hay URL en caché */
  onGetDownloadUrl?: (format: "pdf" | "docx") => Promise<string | null>;
};

export function DocumentDownloadCard({
  documentId,
  documentType,
  createdAt,
  pdfUrl,
  docxUrl,
  onRefreshUrls,
  onGetDownloadUrl,
}: DocumentDownloadCardProps) {
  const title = DOCUMENT_TYPE_LABELS[documentType] || documentType.replace(/_/g, " ");

  const handleDownload = async (format: "pdf" | "docx", url: string | null | undefined) => {
    if (url) {
      window.open(url, "_blank", "noopener");
      return;
    }
    if (onGetDownloadUrl) {
      const fetched = await onGetDownloadUrl(format);
      if (fetched) window.open(fetched, "_blank", "noopener");
    } else if (onRefreshUrls) {
      await onRefreshUrls();
    }
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-3 flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-100 text-slate-600">
            <span className="text-lg">📄</span>
          </div>
          <div>
            <h3 className="font-medium text-slate-800">{title}</h3>
            <p className="text-xs text-slate-500">{formatDate(createdAt)}</p>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap gap-2">
        {pdfUrl ? (
          <a
            href={pdfUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            Descargar PDF
          </a>
        ) : (
          <button
            onClick={() => handleDownload("pdf", pdfUrl)}
            className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
          >
            Obtener PDF
          </button>
        )}
        {docxUrl ? (
          <a
            href={docxUrl}
            target="_blank"
            rel="noopener noreferrer"
            download
            className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            Descargar Word
          </a>
        ) : (
          <button
            onClick={() => handleDownload("docx", docxUrl)}
            className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
          >
            Obtener Word
          </button>
        )}
      </div>
      <p className="mt-3 text-xs text-slate-500">
        Modelo orientativo generado por Tramitup. Revisa y adapta antes de presentar.
      </p>
    </div>
  );
}
