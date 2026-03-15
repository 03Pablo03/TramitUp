"use client";

import { useState, useEffect, useCallback } from "react";
import { apiFetch } from "@/lib/api";

export type Alert = {
  alert_id: string;
  conversation_id: string | null;
  description: string;
  deadline_date: string;
  law_reference: string | null;
  days_remaining: number;
  urgency: string;
  status: string;
  notifications_sent: string[];
  created_at: string;
};

export type CreateAlertData = {
  conversation_id?: string;
  description: string;
  deadline_date: string;
  law_reference?: string;
  notify_days_before?: number[];
};

export function useAlerts(enabled = true) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchAlerts = useCallback(async () => {
    try {
      const res = await apiFetch("/alerts");
      if (res.status === 403) {
        // Plan free — alertas no disponibles, silencioso
        setAlerts([]);
        return;
      }
      const data = await res.json();
      setAlerts(Array.isArray(data) ? data : []);
    } catch {
      setAlerts([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (enabled) {
      fetchAlerts();
    } else {
      setAlerts([]);
      setIsLoading(false);
    }
  }, [enabled, fetchAlerts]);

  const urgentCount = alerts.filter(
    (a) => a.status === "active" && a.days_remaining <= 3
  ).length;

  const createAlert = async (data: CreateAlertData) => {
    const res = await apiFetch("/alerts/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Error al crear alerta");
    }
    await fetchAlerts();
  };

  const dismissAlert = async (alertId: string) => {
    await apiFetch(`/alerts/${alertId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: "dismissed" }),
    });
    await fetchAlerts();
  };

  const deleteAlert = async (alertId: string) => {
    await apiFetch(`/alerts/${alertId}`, { method: "DELETE" });
    await fetchAlerts();
  };

  return {
    alerts,
    urgentCount,
    isLoading,
    createAlert,
    dismissAlert,
    deleteAlert,
    refresh: fetchAlerts,
  };
}
