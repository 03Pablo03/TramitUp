"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { ChatLayout } from "./components/ChatLayout";
import { useAlerts } from "@/hooks/useAlerts";
import { ChatWindow } from "./components/ChatWindow";
import { RateLimitModal } from "./components/RateLimitModal";
import { apiFetch } from "@/lib/api";
import { AttachedFile } from "@/components/chat/FileUpload";

type DetectedDeadline = {
  description: string;
  days: number;
  business_days: boolean;
  reference_date: string | null;
  law_reference: string;
  urgency: string;
};

type CompensationEstimate = {
  amount_eur?: number;
  reduced_amount_eur?: number;
  applies: boolean;
  reason: string;
};

type PortalInfo = {
  portal_key: string;
  name: string;
  url: string;
  needs_digital_cert: boolean;
  also_by_post: boolean;
  notes?: string;
  official_form_url?: string | null;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  category?: string;
  subcategory?: string;
  detectedDeadlines?: DetectedDeadline[];
  portalInfo?: PortalInfo;
  compensationEstimate?: CompensationEstimate;
  attachments?: { name: string; type: string }[];
  followUpSuggestions?: string[];
};

type Conversation = { id: string; title: string; category?: string; created_at: string };

function ChatPageContent() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [remainingChats, setRemainingChats] = useState<number | null>(null);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [showRateLimitModal, setShowRateLimitModal] = useState(false);
  const [showProModal, setShowProModal] = useState(false);
  const [currentCategory, setCurrentCategory] = useState<string>("");
  const [currentSubcategory, setCurrentSubcategory] = useState<string>("");
  const [userPlan, setUserPlan] = useState<string>("free");
  const [showCalculatorBanner, setShowCalculatorBanner] = useState(false);
  const [feedbackMap, setFeedbackMap] = useState<Record<number, "positive" | "negative">>({});
  const searchParams = useSearchParams();

  useEffect(() => {
    if (!authLoading && !user) router.push("/login");
  }, [user, authLoading, router]);

  const convParam = searchParams.get("conv");
  useEffect(() => {
    if (convParam && user) {
      setConversationId(convParam);
      apiFetch(`/conversations/${convParam}/messages`)
        .then((r) => r.json())
        .then((data) => {
          const msgs: Message[] = (data.messages || []).map((m: { role: string; content: string }) => ({
            role: m.role as "user" | "assistant",
            content: m.content,
          }));
          setMessages(msgs);
        })
        .catch(() => {
          // Silently ignore — user will just start a fresh conversation
        });
    }
  }, [convParam, user]);

  useEffect(() => {
    if (!user || authLoading) return;
    apiFetch("/history")
      .then((r) => r.json())
      .then((data) => setConversations(data.conversations || []))
      .catch(() => setConversations([]));
    apiFetch("/me")
      .then((r) => r.json())
      .then((data) => {
        setRemainingChats(data.remaining_chats_today ?? null);
        setUserPlan(data.plan || "free");
      })
      .catch(() => {
        setRemainingChats(null);
        setUserPlan("free");
      });
  }, [user?.id, authLoading]);

  const handleSend = async (text: string, attachments?: AttachedFile[]) => {
    if (!user) return;
    
    // Validar longitud del mensaje
    if (text.trim().length < 10 && (!attachments || attachments.length === 0)) {
      setError("Por favor, escribe una consulta más detallada (mínimo 10 caracteres) o adjunta un documento.");
      return;
    }
    
    if (text.length > 2000) {
      setError("Tu consulta es demasiado larga. Por favor, acórtala a menos de 2000 caracteres.");
      return;
    }
    
    setSending(true);
    setError("");
    setShowRateLimitModal(false);
    
    // Subir archivos adjuntos si los hay
    let attachmentIds: string[] = [];
    if (attachments && attachments.length > 0) {
      try {
        for (const attachment of attachments) {
          const formData = new FormData();
          formData.append('file', attachment.file);
          formData.append('conversation_id', conversationId || '');
          
          const uploadRes = await fetch('/api/backend/attachments/upload', {
            method: 'POST',
            credentials: 'include',
            body: formData
          });
          
          if (uploadRes.ok) {
            const uploadData = await uploadRes.json();
            attachmentIds.push(uploadData.attachment_id);
          }
        }
      } catch {
        setError("Error subiendo archivos adjuntos. Inténtalo de nuevo.");
        setSending(false);
        return;
      }
    }
    
    setMessages((m) => [...m, {
      role: "user",
      content: text,
      attachments: attachments?.map(a => ({ name: a.name, type: a.type }))
    }]);
    setMessages((m) => [...m, { role: "assistant", content: "", category: "", subcategory: "" }]);
    const idx = messages.length + 1;

    try {
      const res = await fetch("/api/backend/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ 
          message: text, 
          conversation_id: conversationId,
          attachment_ids: attachmentIds
        }),
      });
      if (!res.ok || !res.body) throw new Error("Error al enviar");
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let full = "";
      let newConvId = conversationId;
      let cat = "";
      let subcat = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));
              if (Array.isArray(data)) {
                for (const item of data) {
                  if (item.type === "conversation_id") {
                    newConvId = item.id;
                    setConversationId(item.id);
                  }
                  if (item.type === "classification") {
                    cat = item.category || "";
                    subcat = item.subcategory || "";
                    setCurrentCategory(cat);
                    setCurrentSubcategory(subcat);
                    setMessages((prev) => {
                      const next = [...prev];
                      if (next[idx]) next[idx] = { ...next[idx], category: cat, subcategory: subcat };
                      return next;
                    });
                    // Sugerir calculadora si la consulta es sobre despido laboral
                    const keywords: string[] = item.keywords || [];
                    const esDespido =
                      cat === "laboral" &&
                      (subcat?.includes("despido") ||
                        keywords.some((k: string) =>
                          ["despido", "despedir", "indemnización", "finiquito", "extinción"].includes(
                            k.toLowerCase()
                          )
                        ));
                    if (esDespido) setShowCalculatorBanner(true);
                  }
                  if (item.type === "chunk") {
                    full += item.content;
                    setMessages((prev) => {
                      const next = [...prev];
                      if (next[idx]) next[idx] = { ...next[idx], content: full, category: cat, subcategory: subcat };
                      return next;
                    });
                  }
                  if (item.type === "detected_deadlines" && item.deadlines?.length) {
                    setMessages((prev) => {
                      const next = [...prev];
                      if (next[idx]) next[idx] = { ...next[idx], detectedDeadlines: item.deadlines };
                      return next;
                    });
                  }
                  if (item.type === "portal_info" && item.portal_key && item.portal_summary) {
                    setMessages((prev) => {
                      const next = [...prev];
                      if (next[idx]) {
                        next[idx] = {
                          ...next[idx],
                          portalInfo: {
                            portal_key: item.portal_key,
                            ...item.portal_summary,
                          },
                        };
                      }
                      return next;
                    });
                  }
                  if (item.type === "compensation_estimate" && item.compensation) {
                    setMessages((prev) => {
                      const next = [...prev];
                      if (next[idx]) next[idx] = { ...next[idx], compensationEstimate: item.compensation };
                      return next;
                    });
                  }
                  if (item.type === "follow_up_suggestions" && item.suggestions?.length) {
                    setMessages((prev) => {
                      const next = [...prev];
                      if (next[idx]) next[idx] = { ...next[idx], followUpSuggestions: item.suggestions };
                      return next;
                    });
                  }
                  if (item.type === "error") {
                    setError(item.message);
                    setShowRateLimitModal(true);
                  }
                }
              }
            } catch {
              /* ignore */
            }
          }
        }
      }
      if (newConvId && !conversations.find((c) => c.id === newConvId)) {
        setConversations((c) => [
          { id: newConvId, title: text.slice(0, 40), created_at: new Date().toISOString() },
          ...c,
        ]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error de conexión");
      setMessages((m) => m.slice(0, -1));
    } finally {
      setSending(false);
      setCurrentCategory("");
      setCurrentSubcategory("");
    }
  };

  const handleCopy = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  const hasDocumentAccess = userPlan === "pro" || userPlan === "document";
  const { urgentCount } = useAlerts(!!user && !authLoading && hasDocumentAccess);

  const handleNewChat = () => {
    setMessages([]);
    setConversationId(null);
    setShowCalculatorBanner(false);
    setFeedbackMap({});
  };

  const handleSelectConversation = async (id: string) => {
    setConversationId(id);
    setMessages([]);
    setFeedbackMap({});
    try {
      const res = await apiFetch(`/conversations/${id}/messages`);
      const data = await res.json();
      const msgs: Message[] = (data.messages || []).map((m: { role: string; content: string }) => ({
        role: m.role as "user" | "assistant",
        content: m.content,
      }));
      setMessages(msgs);
    } catch {
      setMessages([]);
    }
  };

  const handleRenameConversation = async (conversationId: string, newTitle: string) => {
    try {
      const res = await apiFetch(`/conversations/${conversationId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTitle })
      });
      
      if (res.ok) {
        // Actualizar la lista de conversaciones
        setConversations(prev => 
          prev.map(conv => 
            conv.id === conversationId 
              ? { ...conv, title: newTitle }
              : conv
          )
        );
      }
    } catch {
      // Silently ignore rename errors — conversation is still usable
    }
  };

  const handleDeleteConversation = async (idToDelete: string) => {
    try {
      const res = await apiFetch(`/conversations/${idToDelete}`, {
        method: 'DELETE'
      });
      
      if (res.ok) {
        setConversations(prev => prev.filter(conv => conv.id !== idToDelete));
        if (conversationId === idToDelete) {
          setConversationId(null);
          setMessages([]);
        }
      }
    } catch {
      // Silently ignore — conversation list will be stale until refresh
    }
  };

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F9FAFB]">
        <div className="text-slate-500">Cargando...</div>
      </div>
    );
  }

  return (
    <>
      <ChatLayout
        conversations={conversations}
        currentConversationId={conversationId}
        onSelectConversation={handleSelectConversation}
        onNewChat={handleNewChat}
        remainingChats={remainingChats}
        urgentAlertsCount={urgentCount}
        userPlan={userPlan}
        onRenameConversation={handleRenameConversation}
        onDeleteConversation={handleDeleteConversation}
      >
        <ChatWindow
          messages={messages}
          sending={sending}
          currentCategory={currentCategory}
          currentSubcategory={currentSubcategory}
          onSend={handleSend}
          onCopy={handleCopy}
          conversationId={conversationId}
          hasDocumentAccess={hasDocumentAccess}
          hasAlertAccess={userPlan === "pro" || userPlan === "document"}
          onProRequired={() => setShowProModal(true)}
          error={error}
          feedbackMap={feedbackMap}
          onFeedback={async (messageIndex, rating) => {
            setFeedbackMap((prev) => ({ ...prev, [messageIndex]: rating }));
            if (conversationId) {
              try {
                await apiFetch("/feedback", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    conversation_id: conversationId,
                    message_index: messageIndex,
                    rating,
                  }),
                });
              } catch { /* silent */ }
            }
          }}
        />
      </ChatLayout>
      <RateLimitModal
        open={showRateLimitModal}
        onClose={() => setShowRateLimitModal(false)}
        message="Has usado tus 2 consultas gratuitas de hoy. Con PRO tienes consultas ilimitadas."
      />
      {showCalculatorBanner && (
        <div className="fixed bottom-6 right-6 z-40 w-72 rounded-2xl border border-blue-200 bg-white p-4 shadow-xl">
          <button
            onClick={() => setShowCalculatorBanner(false)}
            className="absolute right-3 top-3 text-slate-400 hover:text-slate-600"
            aria-label="Cerrar"
          >
            ✕
          </button>
          <p className="text-lg">⚖️</p>
          <p className="mt-1 text-sm font-semibold text-slate-800">
            ¿Sabes cuánto te deben?
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Calcula tu indemnización exacta según la ley en menos de 1 minuto.
          </p>
          <Link
            href="/calculadora"
            className="mt-3 flex w-full items-center justify-center rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 py-2 text-sm font-bold text-white hover:from-[var(--primary-dark)] hover:to-blue-700 transition-all"
          >
            Calcular ahora →
          </Link>
        </div>
      )}
      {showProModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
            <h2 className="mb-4 text-lg font-semibold">Plan PRO</h2>
            <p className="mb-4 text-sm text-slate-600">
              Las alertas de plazos son exclusivas del plan PRO. Actualiza para no perder ningún plazo legal.
            </p>
            <button
              onClick={() => {
                setShowProModal(false);
                router.push("/pricing");
              }}
              className="rounded-lg bg-[#1A56DB] px-4 py-2 text-sm font-medium text-white"
            >
              Ver planes
            </button>
            <button
              onClick={() => setShowProModal(false)}
              className="ml-2 text-sm text-slate-500"
            >
              Cerrar
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="flex min-h-screen items-center justify-center bg-[#FAFAF9]"><div className="text-slate-500">Cargando...</div></div>}>
      <ChatPageContent />
    </Suspense>
  );
}
