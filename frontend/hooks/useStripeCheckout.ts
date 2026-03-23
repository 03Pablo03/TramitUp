"use client";
import { useState, useRef } from "react";
import { apiFetch } from "@/lib/api";

export function useStripeCheckout() {
  const [loading, setLoading] = useState(false);
  // useRef for synchronous guard — useState updates are async and don't
  // prevent a second call that fires before the first re-render.
  const inFlight = useRef(false);

  const startCheckout = async () => {
    if (inFlight.current) return;
    inFlight.current = true;
    setLoading(true);
    try {
      const res = await apiFetch("/stripe/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          price_type: "pro",
          trial_days: 3,
        }),
      });
      const data = await res.json();
      if (data.url) {
        window.location.href = data.url;
      }
    } finally {
      inFlight.current = false;
      setLoading(false);
    }
  };

  return { startCheckout, loading };
}
