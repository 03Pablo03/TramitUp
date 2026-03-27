"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { ToolHeader } from "@/components/ToolHeader";
import { WizardProgress } from "@/components/wizard/WizardProgress";
import { WizardStepForm } from "@/components/wizard/WizardStepForm";
import { WizardStepAnalysis } from "@/components/wizard/WizardStepAnalysis";
import { WizardStepDocument } from "@/components/wizard/WizardStepDocument";
import { apiFetch } from "@/lib/api";
import { X, CheckCircle, Bell, AlertTriangle } from "@/lib/icons";

type StepDef = {
  id: string;
  title: string;
  type: string;
  fields?: Array<{
    name: string;
    label: string;
    type: string;
    required?: boolean;
    placeholder?: string;
    options?: string[];
  }>;
  prompt_context?: string;
  description?: string;
  content?: string;
  auto_alert_days?: number;
  auto_alert_description?: string;
};

type Template = {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: string;
  estimated_time: string;
  steps: StepDef[];
};

type StepResult = {
  step_id: string;
  step_result: Record<string, unknown>;
  next_step: string;
  status: string;
};

export default function WizardPage() {
  const params = useParams();
  const router = useRouter();
  const templateId = params.templateId as string;
  const { user, loading: authLoading } = useAuth();

  // Auth guard — redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !user) router.push("/login");
  }, [user, authLoading, router]);

  const [template, setTemplate] = useState<Template | null>(null);
  const [wizardId, setWizardId] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState<string>("");
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);
  const [stepResults, setStepResults] = useState<Record<string, Record<string, unknown>>>({});
  const [loading, setLoading] = useState(true);
  const [stepLoading, setStepLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [wizardComplete, setWizardComplete] = useState(false);

  // Initialize: fetch template and start wizard (only when authenticated)
  useEffect(() => {
    if (!user || authLoading) return;
    let cancelled = false;

    async function init() {
      try {
        // Get template
        const tmplRes = await apiFetch(`/wizard/templates/${templateId}`);
        const tmplData = await tmplRes.json();
        if (!tmplRes.ok || !tmplData.data) {
          setError("Trámite no encontrado");
          setLoading(false);
          return;
        }
        if (cancelled) return;
        setTemplate(tmplData.data);

        // Start wizard
        const startRes = await apiFetch("/wizard/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ template_id: templateId }),
        });
        const startData = await startRes.json();
        if (!startRes.ok) {
          setError(startData.detail || "Error al iniciar el trámite");
          setLoading(false);
          return;
        }
        if (cancelled) return;

        setWizardId(startData.data.wizard_id);
        setCurrentStep(startData.data.current_step);
      } catch {
        if (!cancelled) setError("Error de conexión. Inténtalo de nuevo.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    init();
    return () => { cancelled = true; };
  }, [templateId, user, authLoading]);

  const submitStep = useCallback(
    async (stepId: string, data: Record<string, unknown> = {}) => {
      if (!wizardId) return;
      setStepLoading(true);
      setError(null);

      try {
        const res = await apiFetch(`/wizard/${wizardId}/step/${stepId}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ data }),
        });
        const result = await res.json();

        if (!res.ok) {
          setError(result.detail || "Error al procesar el paso");
          setStepLoading(false);
          return;
        }

        const stepResult: StepResult = result.data;

        setStepResults((prev) => ({ ...prev, [stepId]: stepResult.step_result }));
        setCompletedSteps((prev) => [...prev, stepId]);

        if (stepResult.status === "completed") {
          setWizardComplete(true);
        } else {
          setCurrentStep(stepResult.next_step);
        }
      } catch {
        setError("Error de conexión. Inténtalo de nuevo.");
      } finally {
        setStepLoading(false);
      }
    },
    [wizardId],
  );

  // Auto-submit non-interactive steps (ai_analysis, document_generation, follow_up)
  const currentStepDef = template?.steps.find((s) => s.id === currentStep);
  useEffect(() => {
    if (!currentStepDef || stepLoading || !wizardId) return;
    const autoTypes = ["ai_analysis", "document_generation", "follow_up"];
    if (autoTypes.includes(currentStepDef.type) && !stepResults[currentStep]) {
      submitStep(currentStep);
    }
  }, [currentStep, currentStepDef, stepLoading, wizardId, stepResults, submitStep]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F9FAFB]">
        <ToolHeader title="Cargando trámite..." backHref="/wizard" backLabel="Trámites" />
        <div className="mx-auto max-w-2xl px-4 py-16 text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-slate-200 border-t-[var(--primary)]" />
          <p className="mt-4 text-sm text-slate-500">Preparando tu trámite guiado...</p>
        </div>
      </div>
    );
  }

  if (error && !template) {
    return (
      <div className="min-h-screen bg-[#F9FAFB]">
        <ToolHeader title="Error" backHref="/wizard" backLabel="Trámites" />
        <div className="mx-auto max-w-2xl px-4 py-16 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-red-50"><X className="h-7 w-7 text-red-600" /></div>
          <h2 className="text-lg font-semibold text-slate-800">No se pudo cargar el trámite</h2>
          <p className="mt-2 text-sm text-slate-500">{error}</p>
          <Link
            href="/wizard"
            className="mt-6 inline-block rounded-xl bg-[var(--primary)] px-6 py-2.5 text-sm font-semibold text-white"
          >
            Volver a trámites
          </Link>
        </div>
      </div>
    );
  }

  if (!template) return null;

  // Completion screen
  if (wizardComplete) {
    return (
      <div className="min-h-screen bg-[#F9FAFB]">
        <ToolHeader title={template.title} backHref="/wizard" backLabel="Trámites" />
        <div className="mx-auto max-w-2xl px-4 py-12">
          <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-green-400 to-emerald-500 shadow-lg shadow-green-500/20">
              <CheckCircle className="h-8 w-8 text-white" />
            </div>
            <h2 className="text-xl font-bold text-slate-800">¡Trámite completado!</h2>
            <p className="mt-2 text-sm text-slate-500">
              Has completado todos los pasos de &quot;{template.title}&quot;.
              Revisa los documentos generados y sigue las instrucciones proporcionadas.
            </p>

            <div className="mt-8 grid gap-3 sm:grid-cols-2">
              <Link
                href="/casos"
                className="rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-700 transition-all hover:bg-slate-50"
              >
                Ir a mis expedientes
              </Link>
              <Link
                href="/chat"
                className="rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700"
              >
                Consultar al asistente
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const steps = template.steps;

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      <ToolHeader
        title={template.title}
        backHref="/wizard"
        backLabel="Trámites"
      />
      <div className="mx-auto max-w-2xl px-4 py-8">
        <WizardProgress
          steps={steps}
          currentStep={currentStep}
          completedSteps={completedSteps}
        />

        {error && (
          <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4">
            <div className="flex items-start gap-3">
              <AlertTriangle className="h-5 w-5 text-red-600 shrink-0" />
              <div>
                <p className="text-sm font-medium text-red-800">Error</p>
                <p className="text-xs text-red-600">{error}</p>
              </div>
              <button onClick={() => setError(null)} className="ml-auto text-red-400 hover:text-red-600">
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}

        <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8">
          {currentStepDef && (
            <div className="mb-6">
              <h2 className="text-lg font-bold text-slate-800">{currentStepDef.title}</h2>
              {currentStepDef.description && (
                <p className="mt-1 text-sm text-slate-500">{currentStepDef.description}</p>
              )}
            </div>
          )}

          {/* Form step */}
          {currentStepDef?.type === "form" && currentStepDef.fields && (
            <WizardStepForm
              fields={currentStepDef.fields}
              onSubmit={(data) => submitStep(currentStep, data)}
              loading={stepLoading}
            />
          )}

          {/* AI Analysis step */}
          {currentStepDef?.type === "ai_analysis" && (
            <WizardStepAnalysis
              analysis={(stepResults[currentStep]?.analysis as string) || null}
              loading={stepLoading}
              onContinue={() => {
                // Mark analysis as viewed and move to next
                const idx = steps.findIndex((s) => s.id === currentStep);
                if (idx + 1 < steps.length) {
                  setCompletedSteps((prev) => [...prev, currentStep]);
                  setCurrentStep(steps[idx + 1].id);
                }
              }}
            />
          )}

          {/* Document generation step */}
          {currentStepDef?.type === "document_generation" && (
            <WizardStepDocument
              title={currentStepDef.title}
              content={(stepResults[currentStep]?.document_content as string) || null}
              loading={stepLoading}
              legalNotice={stepResults[currentStep]?.legal_notice as string}
              onContinue={() => {
                const idx = steps.findIndex((s) => s.id === currentStep);
                if (idx + 1 < steps.length) {
                  setCompletedSteps((prev) => [...prev, currentStep]);
                  setCurrentStep(steps[idx + 1].id);
                }
              }}
            />
          )}

          {/* Instructions step */}
          {currentStepDef?.type === "instructions" && currentStepDef.content && (
            <div className="space-y-6">
              <div className="rounded-xl border border-slate-200 bg-slate-50/50 p-6">
                {currentStepDef.content.split("\n").map((line, i) => {
                  const match = line.match(/^(\d+)\.\s(.+)$/);
                  if (match) {
                    return (
                      <div key={i} className="flex gap-3 py-2">
                        <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[var(--primary)] text-xs font-bold text-white">
                          {match[1]}
                        </span>
                        <p className="text-sm text-slate-700">{match[2]}</p>
                      </div>
                    );
                  }
                  if (line.trim()) {
                    return <p key={i} className="text-sm text-slate-600 py-1">{line}</p>;
                  }
                  return null;
                })}
              </div>
              <button
                onClick={() => submitStep(currentStep)}
                disabled={stepLoading}
                className="w-full rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700 disabled:opacity-50"
              >
                {steps.findIndex((s) => s.id === currentStep) === steps.length - 1
                  ? "Finalizar trámite"
                  : "Continuar"}
              </button>
            </div>
          )}

          {/* Follow-up step */}
          {currentStepDef?.type === "follow_up" && (
            <div className="space-y-6">
              <div className="rounded-xl border border-blue-100 bg-blue-50 p-6 text-center">
                <Bell className="h-8 w-8 text-blue-600" />
                <h3 className="mt-3 font-semibold text-blue-800">Seguimiento automático</h3>
                <p className="mt-2 text-sm text-blue-600">
                  {stepResults[currentStep]?.alert_created
                    ? `Se ha creado una alerta automática: "${currentStepDef.auto_alert_description}". Te recordaremos ${currentStepDef.auto_alert_days} días antes del vencimiento.`
                    : stepLoading
                    ? "Configurando seguimiento..."
                    : `Crearemos una alerta para dentro de ${currentStepDef.auto_alert_days} días: "${currentStepDef.auto_alert_description}".`}
                </p>
              </div>
              {!stepLoading && stepResults[currentStep] && (
                <button
                  onClick={() => submitStep(currentStep)}
                  className="w-full rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700"
                >
                  Finalizar trámite
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
