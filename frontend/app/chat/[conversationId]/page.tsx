"use client";

import { useEffect } from "react";
import { useRouter, useParams } from "next/navigation";

export default function ConversationPage() {
  const router = useRouter();
  const params = useParams();
  const conversationId = params.conversationId as string;

  useEffect(() => {
    if (conversationId) {
      router.replace(`/chat?conv=${conversationId}`);
    }
  }, [conversationId, router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#F9FAFB]">
      <div className="text-slate-500">Cargando conversación...</div>
    </div>
  );
}
