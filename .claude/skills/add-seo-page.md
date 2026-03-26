Añade una nueva página de landing SEO a TramitUp.

**Pasos:**

1. Lee una página SEO existente como referencia:
   - `frontend/app/reclamar-vuelo-cancelado/page.tsx`
   - `frontend/app/calcular-finiquito/page.tsx`
2. Lee los componentes de landing en `frontend/app/landing/components/`:
   - `SEOLandingTemplate.tsx` — template base reutilizable
   - `Hero.tsx`, `HowItWorks.tsx`, `FAQ.tsx`, etc.
3. Crea la nueva página en `frontend/app/{slug}/page.tsx`:
   ```typescript
   import { Metadata } from "next";

   export const metadata: Metadata = {
     title: "Título SEO optimizado — TramitUp",
     description: "Descripción meta de 150-160 chars con keyword principal",
     keywords: ["keyword1", "keyword2"],
     openGraph: {
       title: "...",
       description: "...",
     }
   };

   export default function NuevaPaginaPage() {
     return <SEOLandingTemplate ... />;
   }
   ```
4. La página debe incluir:
   - H1 con keyword principal
   - Sección de beneficios/pasos
   - FAQ con preguntas frecuentes sobre el trámite
   - CTA prominente hacia `/chat` o el wizard relevante
   - Schema markup (JSON-LD) si aplica (HowTo, FAQ, etc.)
5. Añade la página al sitemap si existe (`frontend/app/sitemap.ts`)
6. Verifica que la ruta funciona y el metadata es correcto
7. La página NO debe requerir autenticación — es pública y para SEO

**Página a crear:** $ARGUMENTS
