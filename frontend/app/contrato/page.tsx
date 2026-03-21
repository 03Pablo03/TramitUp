"use client";

import { useCallback, useRef, useState } from "react";
import Link from "next/link";
import { LandingNav } from "../landing/components/LandingNav";
import { Footer } from "../landing/components/Footer";
import { ContractAnalysisResult } from "@/components/ContractAnalysisResult";

const ACCEPTED_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "image/jpeg",
  "image/jpg",
  "image/png",
];

const ACCEPTED_EXT = ".pdf,.docx,.jpg,.jpeg,.png";
const MAX_MB = 10;

interface AnalysisResult {
  tipo_contrato: string;
  resumen: string;
  clausulas: {
    id: string;
    titulo: string;
    fragmento: string;
    riesgo: "alto" | "medio" | "bajo";
    problema: string;
    base_legal: string;
    accion: string;
  }[];
  recomendacion_general: string;
}

export default function ContratoPage() {
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateAndSet = (f: File) => {
    setError("");
    setResult(null);
    if (!ACCEPTED_TYPES.includes(f.type)) {
      setError("Formato no admitido. Sube un PDF, DOCX o imagen (JPG/PNG).");
      return;
    }
    if (f.size > MAX_MB * 1024 * 1024) {
      setError(`El archivo supera el límite de ${MAX_MB} MB.`);
      return;
    }
    setFile(f);
  };

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) validateAndSet(dropped);
  }, []);

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) validateAndSet(f);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/backend/contract-analysis", {
        method: "POST",
        credentials: "include",
        body: formData,
      });

      if (!res.ok) {
        let msg = `Error ${res.status}`;
        try {
          const body = await res.json();
          msg = body.detail || body.error || msg;
        } catch { /* ignore */ }
        setError(msg);
        return;
      }

      const data: AnalysisResult = await res.json();
      setResult(data);
    } catch {
      setError("No se pudo conectar con el servidor. Inténtalo de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setError("");
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      <LandingNav />

      <main className="mx-auto max-w-2xl px-4 py-12">
        {/* Cabecera */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-[var(--primary)] to-blue-600 text-3xl text-white shadow-lg">
            📋
          </div>
          <h1 className="text-3xl font-bold text-slate-900">Analiza tu contrato</h1>
          <p className="mt-2 text-slate-500">
            Sube tu contrato de alquiler o laboral y detectamos cláusulas abusivas o ilegales según el
            derecho español.
          </p>
        </div>

        {/* Zona de subida */}
        {!result && (
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div
              onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
              onDragLeave={() => setDragging(false)}
              onDrop={onDrop}
              onClick={() => inputRef.current?.click()}
              className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-10 transition-colors
                ${dragging ? "border-[var(--primary)] bg-blue-50" : "border-slate-300 hover:border-[var(--primary)] hover:bg-blue-50/50"}`}
            >
              <input
                ref={inputRef}
                type="file"
                accept={ACCEPTED_EXT}
                className="hidden"
                onChange={onInputChange}
              />
              <div className="text-4xl">{file ? "📄" : "📁"}</div>
              {file ? (
                <div className="mt-3 text-center">
                  <p className="font-semibold text-slate-800">{file.name}</p>
                  <p className="text-sm text-slate-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                  <button
                    onClick={(e) => { e.stopPropagation(); handleReset(); }}
                    className="mt-2 text-xs text-slate-400 hover:text-slate-600 underline"
                  >
                    Cambiar archivo
                  </button>
                </div>
              ) : (
                <div className="mt-3 text-center">
                  <p className="font-medium text-slate-700">
                    Arrastra tu contrato aquí o{" "}
                    <span className="text-[var(--primary)]">selecciona un archivo</span>
                  </p>
                  <p className="mt-1 text-sm text-slate-400">PDF, DOCX o imagen · máx. {MAX_MB} MB</p>
                </div>
              )}
            </div>

            {error && (
              <div className="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={!file || loading}
              className={`mt-4 w-full rounded-xl py-3 text-sm font-bold text-white transition-all
                ${file && !loading
                  ? "bg-gradient-to-r from-[var(--primary)] to-blue-600 hover:from-[var(--primary-dark)] hover:to-blue-700 shadow-md hover:shadow-lg"
                  : "cursor-not-allowed bg-slate-200 text-slate-400"
                }`}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                  </svg>
                  Analizando contrato…
                </span>
              ) : (
                "Analizar contrato"
              )}
            </button>

            <p className="mt-3 text-center text-xs text-slate-400">
              El análisis tarda entre 10 y 30 segundos según la longitud del contrato.
            </p>
          </div>
        )}

        {/* Resultado */}
        {result && (
          <>
            <div className="mb-4 flex justify-end">
              <button
                onClick={handleReset}
                className="text-sm text-[var(--primary)] hover:underline"
              >
                ← Analizar otro contrato
              </button>
            </div>
            <ContractAnalysisResult data={result} />
          </>
        )}

        {/* Info */}
        {!result && (
          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
            {[
              {
                icon: "🏠",
                title: "Contrato de alquiler",
                desc: "Detectamos fianzas ilegales, renuncias de prórroga, gastos indebidos y más según la LAU.",
              },
              {
                icon: "💼",
                title: "Contrato laboral",
                desc: "Identificamos periodos de prueba excesivos, salarios ilegales, cláusulas de no competencia sin compensación.",
              },
              {
                icon: "📑",
                title: "Otros contratos",
                desc: "Análisis general de cláusulas abusivas según el Código Civil y la normativa de consumo.",
              },
            ].map((item) => (
              <div
                key={item.title}
                className="rounded-xl border border-slate-200 bg-white p-4 text-center shadow-sm"
              >
                <div className="text-3xl">{item.icon}</div>
                <p className="mt-2 text-sm font-semibold text-slate-800">{item.title}</p>
                <p className="mt-1 text-xs text-slate-500">{item.desc}</p>
              </div>
            ))}
          </div>
        )}

        {/* Nota legal */}
        {!result && (
          <p className="mt-8 text-center text-xs text-slate-400">
            Análisis orientativo. No sustituye el asesoramiento de un abogado colegiado.{" "}
            <Link href="/chat" className="underline">
              Consulta con nuestro asistente
            </Link>{" "}
            para más detalles.
          </p>
        )}
      </main>

      <Footer />
    </div>
  );
}
