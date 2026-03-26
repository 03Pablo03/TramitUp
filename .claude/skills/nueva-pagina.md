Crea una nueva página en el frontend de TramitUp siguiendo los patrones del proyecto.

**Pasos a seguir:**

1. **Lee** antes de crear:
   - Una página similar existente (dashboard, casos, wizard)
   - `frontend/app/layout.tsx` para entender el layout global

2. **Estructura base de página autenticada:**
```tsx
"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { ToolHeader } from "@/components/ToolHeader";

export default function NuevaPagina() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!authLoading && !user) router.push("/login");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || authLoading) return;
    apiFetch("/ruta")
      .then(r => r.json())
      .then(d => setData(d))
      .catch(() => setError("Error al cargar."))
      .finally(() => setLoading(false));
  }, [user?.id, authLoading]);
  // ...
}
```

3. **Loading/error states obligatorios**
4. **ToolHeader** como encabezado con `title` y `backHref`
5. **Responsive**: probar que funciona en móvil (max-w-3xl mx-auto px-4)

Ahora crea la página: $ARGUMENTS
