"use client";

import { useState } from "react";

type FieldDef = {
  name: string;
  label: string;
  type: string;
  required?: boolean;
  placeholder?: string;
  options?: string[];
};

interface WizardStepFormProps {
  fields: FieldDef[];
  onSubmit: (data: Record<string, string | number>) => void;
  loading?: boolean;
}

export function WizardStepForm({ fields, onSubmit, loading }: WizardStepFormProps) {
  const [values, setValues] = useState<Record<string, string>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (name: string, value: string) => {
    setValues((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: "" }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};

    for (const field of fields) {
      if (field.required && !values[field.name]?.trim()) {
        newErrors[field.name] = "Este campo es obligatorio";
      }
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSubmit(values);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {fields.map((field) => (
        <div key={field.name}>
          <label className="mb-1 block text-sm font-medium text-slate-700">
            {field.label}
            {field.required && <span className="ml-1 text-red-400">*</span>}
          </label>

          {field.type === "select" && field.options ? (
            <select
              value={values[field.name] || ""}
              onChange={(e) => handleChange(field.name, e.target.value)}
              className={`w-full rounded-xl border bg-white px-4 py-2.5 text-sm text-slate-800 transition-colors focus:border-[var(--primary)] focus:outline-none focus:ring-2 focus:ring-blue-500/20 ${
                errors[field.name] ? "border-red-300" : "border-slate-200"
              }`}
            >
              <option value="">Selecciona una opción</option>
              {field.options.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
          ) : field.type === "date" ? (
            <input
              type="date"
              value={values[field.name] || ""}
              onChange={(e) => handleChange(field.name, e.target.value)}
              className={`w-full rounded-xl border bg-white px-4 py-2.5 text-sm text-slate-800 transition-colors focus:border-[var(--primary)] focus:outline-none focus:ring-2 focus:ring-blue-500/20 ${
                errors[field.name] ? "border-red-300" : "border-slate-200"
              }`}
            />
          ) : field.type === "number" ? (
            <input
              type="number"
              value={values[field.name] || ""}
              onChange={(e) => handleChange(field.name, e.target.value)}
              placeholder={field.placeholder}
              className={`w-full rounded-xl border bg-white px-4 py-2.5 text-sm text-slate-800 transition-colors focus:border-[var(--primary)] focus:outline-none focus:ring-2 focus:ring-blue-500/20 ${
                errors[field.name] ? "border-red-300" : "border-slate-200"
              }`}
            />
          ) : (
            <input
              type="text"
              value={values[field.name] || ""}
              onChange={(e) => handleChange(field.name, e.target.value)}
              placeholder={field.placeholder}
              className={`w-full rounded-xl border bg-white px-4 py-2.5 text-sm text-slate-800 transition-colors focus:border-[var(--primary)] focus:outline-none focus:ring-2 focus:ring-blue-500/20 ${
                errors[field.name] ? "border-red-300" : "border-slate-200"
              }`}
            />
          )}

          {errors[field.name] && (
            <p className="mt-1 text-xs text-red-500">{errors[field.name]}</p>
          )}
        </div>
      ))}

      <button
        type="submit"
        disabled={loading}
        className="mt-6 w-full rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700 disabled:opacity-50"
      >
        {loading ? "Procesando..." : "Continuar"}
      </button>
    </form>
  );
}
