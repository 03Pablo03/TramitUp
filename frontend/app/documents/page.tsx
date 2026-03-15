"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { DocumentDownloadCard } from "@/components/DocumentDownloadCard";

type DocumentItem = {
  document_id: string;
  conversation_id: string | null;
  document_type: string;
  created_at: string;
  has_pdf: boolean;
  has_docx: boolean;
};

export default function DocumentsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [userPlan, setUserPlan] = useState<string>("free");

  useEffect(() => {
    if (!authLoading && !user) router.push("/login");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    apiFetch("/me")
      .then((r) => r.json())
      .then((data) => setUserPlan(data?.plan || "free"));
  }, [user]);

  useEffect(() => {
    if (!user || (userPlan !== "pro" && userPlan !== "document")) return;
    apiFetch("/document/history")
      .then((r) => {
        if (r.status === 403) {
          setUserPlan("free");
          return [];
        }
        return r.json();
      })
      .then((data: DocumentItem[] | []) => setDocuments(Array.isArray(data) ? data : []))
      .catch(() => setDocuments([]));
  }, [user, userPlan]);

  const handleGetDownloadUrl = async (
    documentId: string,
    format: "pdf" | "docx"
  ): Promise<string | null> => {
    try {
      const res = await apiFetch(`/document/${documentId}/download`);
      const data = await res.json();
      if (res.ok && data) {
        return format === "pdf" ? data.pdf_url : data.docx_url;
      }
    } catch {
      /* ignore */
    }
    return null;
  };

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-slate-500">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white px-6 py-4">
        <div className="mx-auto flex max-w-4xl items-center justify-between">
          <div className="flex items-center gap-6">
            <span className="font-display text-lg font-bold tracking-tight text-[var(--primary)]">
              TramitUp
            </span>
            <span className="text-sm text-slate-500">Mis modelos de escritos</span>
          </div>
          <div className="flex items-center gap-4">
            {userPlan !== "pro" && userPlan !== "document" && (
              <Link
                href="/account"
                className="inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-2 text-sm font-bold text-white shadow-md hover:from-[var(--primary-dark)] hover:to-blue-700"
              >
                ★ Hazte PRO
              </Link>
            )}
            <Link href="/chat" className="text-slate-600 hover:text-slate-800">
              Chat
            </Link>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-4xl p-6">
        <p className="mb-4 text-sm text-slate-500">
          Modelos orientativos generados por Tramitup. Revisa y adapta antes de presentarlos. No
          prestamos asesoramiento jurídico.
        </p>
        {documents.length === 0 ? (
          <div className="rounded-xl border border-dashed border-slate-300 bg-white p-12 text-center">
            {userPlan !== "pro" && userPlan !== "document" ? (
              <>
                <p className="mb-4 text-slate-600">Los modelos de escritos son exclusivos del plan PRO.</p>
                <Link
                  href="/account"
                  className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-2 text-sm font-bold text-white shadow-md hover:from-[var(--primary-dark)] hover:to-blue-700"
                >
                  ★ Hazte PRO para generar modelos
                </Link>
              </>
            ) : (
              <>
                <p className="mb-4 text-slate-600">No tienes modelos de escritos todavía.</p>
                <Link
                  href="/chat"
                  className="inline-flex items-center gap-2 rounded-lg bg-[#1A56DB] px-4 py-2 text-sm font-medium text-white hover:bg-[#1545a8]"
                >
                  Ir al chat para generar uno
                </Link>
              </>
            )}
          </div>
        ) : (
          <ul className="space-y-4">
            {documents.map((d) => (
              <li key={d.document_id}>
                <DocumentDownloadCard
                  documentId={d.document_id}
                  documentType={d.document_type}
                  createdAt={d.created_at}
                  pdfUrl={null}
                  docxUrl={null}
                  onGetDownloadUrl={(format) => handleGetDownloadUrl(d.document_id, format)}
                />
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
