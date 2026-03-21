"use client";

import { useState } from "react";
import Link from "next/link";
import { LandingNav } from "../landing/components/LandingNav";
import { Footer } from "../landing/components/Footer";

// ─── Tipos ────────────────────────────────────────────────────────────────────

type TipoCalculo = "despido_improcedente" | "despido_procedente" | "fin_contrato_temporal";

interface TramoCalculo {
  desde: string;
  hasta: string;
  anios: number;
  diasIndemnizacion: number;
  importe: number;
  nota: string;
}

interface ResultadoCalculo {
  importeTotal: number;
  salarioDiario: number;
  tramos: TramoCalculo[];
  baseLegal: string;
  notaOrientativa: string;
}

// ─── Lógica de cálculo (TS, sin API) ─────────────────────────────────────────

const REFORMA_LABORAL = new Date("2012-02-12");

function anios(inicio: Date, fin: Date): number {
  return Math.max(0, (fin.getTime() - inicio.getTime()) / (1000 * 60 * 60 * 24 * 365));
}

function calcularDespidoImprocedente(
  salarioAnual: number,
  fechaInicio: Date,
  fechaFin: Date
): ResultadoCalculo {
  const sd = salarioAnual / 365;
  const tramos: TramoCalculo[] = [];

  if (fechaInicio >= REFORMA_LABORAL) {
    // 100% post-reforma: 33 días/año, máx 720 días (24 mensualidades)
    const a = anios(fechaInicio, fechaFin);
    const dias = Math.min(a * 33, 720);
    tramos.push({
      desde: fechaInicio.toLocaleDateString("es-ES"),
      hasta: fechaFin.toLocaleDateString("es-ES"),
      anios: Math.round(a * 100) / 100,
      diasIndemnizacion: Math.round(dias * 100) / 100,
      importe: Math.round(dias * sd * 100) / 100,
      nota: "33 días por año (Ley 3/2012)",
    });
    return {
      importeTotal: Math.round(dias * sd * 100) / 100,
      salarioDiario: Math.round(sd * 100) / 100,
      tramos,
      baseLegal: "ET art. 56 y Ley 3/2012, Disp. Transitoria 5.ª",
      notaOrientativa:
        "Cálculo orientativo basado en salario fijo anual. El importe real puede variar si existen variables, comisiones, complementos salariales o pagas adicionales.",
    };
  }

  // Contrato mixto
  const fin1 = new Date(Math.min(fechaFin.getTime(), new Date("2012-02-11").getTime()));
  const a1 = anios(fechaInicio, fin1);
  const diasInd1Raw = a1 * 45;
  const diasInd1 = Math.min(diasInd1Raw, 1260); // máx 42 mensualidades

  tramos.push({
    desde: fechaInicio.toLocaleDateString("es-ES"),
    hasta: fin1.toLocaleDateString("es-ES"),
    anios: Math.round(a1 * 100) / 100,
    diasIndemnizacion: Math.round(diasInd1 * 100) / 100,
    importe: Math.round(diasInd1 * sd * 100) / 100,
    nota: "45 días por año (contrato anterior al 12 feb 2012)",
  });

  let diasInd2 = 0;
  if (fechaFin > REFORMA_LABORAL) {
    const a2 = anios(REFORMA_LABORAL, fechaFin);
    diasInd2 = a2 * 33;
    tramos.push({
      desde: REFORMA_LABORAL.toLocaleDateString("es-ES"),
      hasta: fechaFin.toLocaleDateString("es-ES"),
      anios: Math.round(a2 * 100) / 100,
      diasIndemnizacion: Math.round(diasInd2 * 100) / 100,
      importe: Math.round(diasInd2 * sd * 100) / 100,
      nota: "33 días por año (Ley 3/2012)",
    });
  }

  // DT 5ª: tope = max(720, diasInd1Raw), nunca > 1260
  const tope = Math.min(Math.max(720, diasInd1Raw), 1260);
  const totalDias = Math.min(diasInd1 + diasInd2, tope);
  return {
    importeTotal: Math.round(totalDias * sd * 100) / 100,
    salarioDiario: Math.round(sd * 100) / 100,
    tramos,
    baseLegal: "ET art. 56 y Ley 3/2012, Disp. Transitoria 5.ª",
    notaOrientativa:
      "Cálculo orientativo basado en salario fijo anual. El importe real puede variar si existen variables, comisiones, complementos salariales o pagas adicionales.",
  };
}

function calcularDespidoProcedente(
  salarioAnual: number,
  fechaInicio: Date,
  fechaFin: Date
): ResultadoCalculo {
  const sd = salarioAnual / 365;
  const a = anios(fechaInicio, fechaFin);
  const dias = Math.min(a * 20, 360); // máx 12 mensualidades
  return {
    importeTotal: Math.round(dias * sd * 100) / 100,
    salarioDiario: Math.round(sd * 100) / 100,
    tramos: [
      {
        desde: fechaInicio.toLocaleDateString("es-ES"),
        hasta: fechaFin.toLocaleDateString("es-ES"),
        anios: Math.round(a * 100) / 100,
        diasIndemnizacion: Math.round(dias * 100) / 100,
        importe: Math.round(dias * sd * 100) / 100,
        nota: "20 días por año (causas objetivas)",
      },
    ],
    baseLegal: "ET art. 53.1.b",
    notaOrientativa:
      "Aplica a despidos por causas económicas, técnicas, organizativas o de producción. Si la empresa no cumple los requisitos formales, puede declararse improcedente (33 días/año).",
  };
}

function calcularFinContrato(
  salarioAnual: number,
  fechaInicio: Date,
  fechaFin: Date
): ResultadoCalculo {
  const sd = salarioAnual / 365;
  const a = anios(fechaInicio, fechaFin);
  const dias = a * 12;
  return {
    importeTotal: Math.round(dias * sd * 100) / 100,
    salarioDiario: Math.round(sd * 100) / 100,
    tramos: [
      {
        desde: fechaInicio.toLocaleDateString("es-ES"),
        hasta: fechaFin.toLocaleDateString("es-ES"),
        anios: Math.round(a * 100) / 100,
        diasIndemnizacion: Math.round(dias * 100) / 100,
        importe: Math.round(dias * sd * 100) / 100,
        nota: "12 días por año (contratos temporales)",
      },
    ],
    baseLegal: "ET art. 49.1.c",
    notaOrientativa:
      "No aplica si el contrato se convierte en indefinido o si la extinción es por baja voluntaria.",
  };
}

function calcular(
  tipo: TipoCalculo,
  salarioAnual: number,
  fechaInicio: Date,
  fechaFin: Date
): ResultadoCalculo {
  if (tipo === "despido_improcedente")
    return calcularDespidoImprocedente(salarioAnual, fechaInicio, fechaFin);
  if (tipo === "despido_procedente")
    return calcularDespidoProcedente(salarioAnual, fechaInicio, fechaFin);
  return calcularFinContrato(salarioAnual, fechaInicio, fechaFin);
}

// ─── Datos de los tipos ───────────────────────────────────────────────────────

const TIPOS: { id: TipoCalculo; label: string; descripcion: string; icono: string }[] = [
  {
    id: "despido_improcedente",
    label: "Despido improcedente",
    descripcion:
      "La empresa te despide sin causa justificada o sin cumplir los requisitos formales.",
    icono: "⚖️",
  },
  {
    id: "despido_procedente",
    label: "Despido procedente / objetivo",
    descripcion:
      "Despido por causas económicas, técnicas, organizativas o de producción.",
    icono: "📋",
  },
  {
    id: "fin_contrato_temporal",
    label: "Fin de contrato temporal",
    descripcion:
      "Tu contrato por obra, eventualidad o interinidad llega a su fecha de vencimiento.",
    icono: "📅",
  },
];

// ─── Componente principal ─────────────────────────────────────────────────────

export default function CalculadoraPage() {
  const [paso, setPaso] = useState<1 | 2 | 3>(1);
  const [tipo, setTipo] = useState<TipoCalculo>("despido_improcedente");
  const [salario, setSalario] = useState("");
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");
  const [resultado, setResultado] = useState<ResultadoCalculo | null>(null);
  const [errores, setErrores] = useState<Record<string, string>>({});

  const validarPaso2 = (): boolean => {
    const e: Record<string, string> = {};
    const s = parseFloat(salario.replace(",", "."));
    if (!salario || isNaN(s) || s <= 0)
      e.salario = "Introduce un salario bruto anual válido";
    if (!fechaInicio) e.fechaInicio = "Introduce la fecha de inicio del contrato";
    if (!fechaFin) e.fechaFin = "Introduce la fecha del despido o fin de contrato";
    if (fechaInicio && fechaFin && new Date(fechaFin) <= new Date(fechaInicio))
      e.fechaFin = "La fecha de fin debe ser posterior a la de inicio";
    setErrores(e);
    return Object.keys(e).length === 0;
  };

  const handleCalcular = () => {
    if (!validarPaso2()) return;
    const res = calcular(
      tipo,
      parseFloat(salario.replace(",", ".")),
      new Date(fechaInicio),
      new Date(fechaFin)
    );
    setResultado(res);
    setPaso(3);
  };

  const reset = () => {
    setPaso(1);
    setSalario("");
    setFechaInicio("");
    setFechaFin("");
    setResultado(null);
    setErrores({});
  };

  const tipoActual = TIPOS.find((t) => t.id === tipo)!;

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      <LandingNav />

      <main className="mx-auto max-w-2xl px-4 py-12">
        {/* Cabecera */}
        <div className="mb-8 text-center">
          <h1 className="font-display text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
            Calculadora de indemnizaciones
          </h1>
          <p className="mt-3 text-[var(--text-body)]">
            Calcula la indemnización que te corresponde según la ley española.
            Resultado instantáneo y gratuito.
          </p>
        </div>

        {/* Indicador de pasos */}
        <div className="mb-8 flex items-center justify-center gap-2">
          {[1, 2, 3].map((n) => (
            <div key={n} className="flex items-center gap-2">
              <div
                className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold transition-colors ${
                  paso === n
                    ? "bg-[var(--primary)] text-white"
                    : paso > n
                    ? "bg-emerald-500 text-white"
                    : "bg-slate-200 text-slate-500"
                }`}
              >
                {paso > n ? "✓" : n}
              </div>
              {n < 3 && (
                <div
                  className={`h-0.5 w-12 transition-colors ${
                    paso > n ? "bg-emerald-500" : "bg-slate-200"
                  }`}
                />
              )}
            </div>
          ))}
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">

          {/* ── PASO 1: Tipo de extinción ───────────────────────────────────── */}
          {paso === 1 && (
            <div>
              <h2 className="mb-1 text-lg font-semibold text-slate-800">
                ¿Cuál es tu situación?
              </h2>
              <p className="mb-6 text-sm text-slate-500">
                Elige el tipo de extinción del contrato para aplicar la fórmula correcta.
              </p>
              <div className="space-y-3">
                {TIPOS.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => setTipo(t.id)}
                    className={`w-full rounded-xl border-2 p-4 text-left transition-all ${
                      tipo === t.id
                        ? "border-[var(--primary)] bg-[var(--primary-light)]/10"
                        : "border-slate-200 hover:border-slate-300"
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-2xl">{t.icono}</span>
                      <div>
                        <p className="font-semibold text-slate-800">{t.label}</p>
                        <p className="mt-0.5 text-sm text-slate-500">{t.descripcion}</p>
                      </div>
                      {tipo === t.id && (
                        <div className="ml-auto mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[var(--primary)]">
                          <span className="text-xs text-white">✓</span>
                        </div>
                      )}
                    </div>
                  </button>
                ))}
              </div>
              <button
                onClick={() => setPaso(2)}
                className="mt-6 w-full rounded-xl bg-[var(--primary)] py-3.5 font-bold text-white hover:bg-[var(--primary-dark)] transition-colors"
              >
                Siguiente →
              </button>
            </div>
          )}

          {/* ── PASO 2: Datos ───────────────────────────────────────────────── */}
          {paso === 2 && (
            <div>
              <button
                onClick={() => setPaso(1)}
                className="mb-4 flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700"
              >
                ← Volver
              </button>
              <div className="mb-6 flex items-center gap-2 rounded-lg bg-slate-50 px-3 py-2">
                <span>{tipoActual.icono}</span>
                <span className="text-sm font-medium text-slate-700">{tipoActual.label}</span>
              </div>
              <h2 className="mb-6 text-lg font-semibold text-slate-800">
                Introduce tus datos
              </h2>

              <div className="space-y-5">
                <div>
                  <label className="mb-1.5 block text-sm font-medium text-slate-700">
                    Salario bruto anual (€)
                  </label>
                  <input
                    type="number"
                    placeholder="Ej: 28000"
                    value={salario}
                    onChange={(e) => setSalario(e.target.value)}
                    className={`w-full rounded-xl border px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-[var(--primary)] ${
                      errores.salario ? "border-red-400" : "border-slate-300"
                    }`}
                  />
                  {errores.salario && (
                    <p className="mt-1 text-xs text-red-600">{errores.salario}</p>
                  )}
                  <p className="mt-1 text-xs text-slate-400">
                    Incluye pagas extra si las cobras prorrateadas. Si no, suma las pagas al
                    salario anual.
                  </p>
                </div>

                <div>
                  <label className="mb-1.5 block text-sm font-medium text-slate-700">
                    Fecha de inicio del contrato
                  </label>
                  <input
                    type="date"
                    value={fechaInicio}
                    onChange={(e) => setFechaInicio(e.target.value)}
                    className={`w-full rounded-xl border px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-[var(--primary)] ${
                      errores.fechaInicio ? "border-red-400" : "border-slate-300"
                    }`}
                  />
                  {errores.fechaInicio && (
                    <p className="mt-1 text-xs text-red-600">{errores.fechaInicio}</p>
                  )}
                </div>

                <div>
                  <label className="mb-1.5 block text-sm font-medium text-slate-700">
                    Fecha del despido / fin de contrato
                  </label>
                  <input
                    type="date"
                    value={fechaFin}
                    onChange={(e) => setFechaFin(e.target.value)}
                    className={`w-full rounded-xl border px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-[var(--primary)] ${
                      errores.fechaFin ? "border-red-400" : "border-slate-300"
                    }`}
                  />
                  {errores.fechaFin && (
                    <p className="mt-1 text-xs text-red-600">{errores.fechaFin}</p>
                  )}
                </div>
              </div>

              <button
                onClick={handleCalcular}
                className="mt-8 w-full rounded-xl bg-[var(--primary)] py-3.5 font-bold text-white hover:bg-[var(--primary-dark)] transition-colors"
              >
                Calcular mi indemnización
              </button>
            </div>
          )}

          {/* ── PASO 3: Resultado ───────────────────────────────────────────── */}
          {paso === 3 && resultado && (
            <div>
              {/* Importe total */}
              <div className="mb-6 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 p-6 text-center text-white">
                <p className="text-sm font-medium opacity-90">
                  {tipoActual.icono} {tipoActual.label}
                </p>
                <p className="mt-2 text-5xl font-extrabold">
                  {resultado.importeTotal.toLocaleString("es-ES", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })} €
                </p>
                <p className="mt-1 text-sm opacity-80">
                  indemnización estimada bruta
                </p>
              </div>

              {/* Desglose */}
              <div className="mb-5">
                <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
                  Desglose del cálculo
                </h3>
                <div className="space-y-3">
                  {resultado.tramos.map((t, i) => (
                    <div
                      key={i}
                      className="rounded-xl border border-slate-100 bg-slate-50 p-4"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <p className="text-xs text-slate-500">
                            {t.desde} → {t.hasta}
                          </p>
                          <p className="mt-0.5 text-sm font-medium text-slate-700">
                            {t.anios} años × {t.nota.split(" ")[0]} días/año
                          </p>
                          <p className="text-xs text-slate-400">{t.nota}</p>
                        </div>
                        <div className="shrink-0 text-right">
                          <p className="text-xs text-slate-500">
                            {t.diasIndemnizacion.toFixed(1)} días
                          </p>
                          <p className="font-bold text-slate-800">
                            {t.importe.toLocaleString("es-ES", {
                              minimumFractionDigits: 2,
                              maximumFractionDigits: 2,
                            })} €
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                  <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-4 py-3">
                    <span className="text-sm text-slate-600">
                      Salario diario base: {resultado.salarioDiario.toFixed(2)} €
                    </span>
                  </div>
                </div>
              </div>

              {/* Base legal */}
              <div className="mb-5 rounded-lg bg-blue-50 px-4 py-3 text-sm text-blue-800">
                <span className="font-semibold">Base legal: </span>
                {resultado.baseLegal}
              </div>

              {/* Nota orientativa */}
              <div className="mb-6 rounded-lg bg-amber-50 px-4 py-3 text-xs text-amber-800">
                ⚠️ {resultado.notaOrientativa}
              </div>

              {/* CTAs */}
              <div className="space-y-3">
                <Link
                  href="/chat"
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 py-3.5 font-bold text-white shadow-lg hover:from-[var(--primary-dark)] hover:to-blue-700 transition-all"
                >
                  💬 Consultar mi caso con el asistente
                </Link>
                <button
                  onClick={reset}
                  className="w-full rounded-xl border border-slate-300 py-3 text-sm font-medium text-slate-600 hover:bg-slate-50 transition-colors"
                >
                  Hacer otro cálculo
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Disclaimer legal */}
        <p className="mt-6 text-center text-xs text-slate-400">
          TramitUp ofrece información basada en normativa pública. Este resultado es orientativo
          y no constituye asesoramiento jurídico. Consulta con un abogado para tu situación concreta.
        </p>
      </main>

      <Footer />
    </div>
  );
}
