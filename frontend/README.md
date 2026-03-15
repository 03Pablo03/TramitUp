# TramitUp Frontend

Frontend de TramitUp desarrollado con Next.js 14, TypeScript y Tailwind CSS.

## 🚀 Desarrollo

### Instalación

```bash
npm install
```

### Variables de Entorno

Copia `.env.example` a `.env.local` y configura:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

### Comandos

```bash
npm run dev          # Servidor de desarrollo
npm run build        # Build de producción
npm run start        # Servidor de producción
npm run lint         # Linting
npm test             # Tests
npm run test:watch   # Tests en modo watch
npm run test:coverage # Tests con cobertura
```

## 🏗️ Arquitectura

### Estructura de Carpetas

```
frontend/
├── app/                    # Next.js 14 App Router
│   ├── (auth)/            # Grupo de rutas de autenticación
│   ├── api/               # API Routes
│   ├── chat/              # Páginas de chat
│   ├── globals.css        # Estilos globales
│   ├── layout.tsx         # Layout principal
│   └── page.tsx           # Página de inicio
├── components/            # Componentes React
│   ├── auth/              # Componentes de autenticación
│   ├── chat/              # Componentes de chat
│   ├── ui/                # Componentes de UI base
│   └── ...
├── context/               # Context Providers
├── hooks/                 # Custom Hooks
├── lib/                   # Utilidades y configuración
├── types/                 # Tipos TypeScript
└── __tests__/             # Tests
```

### Patrones de Arquitectura

#### 1. App Router (Next.js 14)
- Rutas basadas en carpetas
- Server Components por defecto
- Client Components marcados con "use client"

#### 2. Context + Hooks
```typescript
// Context para estado global
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Hook personalizado
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

#### 3. API Routes como Proxy
```typescript
// app/api/backend/[[...path]]/route.ts
export async function POST(request: Request) {
  const supabase = await createServerSupabaseClient();
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    return NextResponse.json({ error: "No autorizado" }, { status: 401 });
  }
  
  // Proxy al backend con autenticación
  return fetch(`${BACKEND_URL}/api/v1/${path}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
    body: await request.text(),
  });
}
```

## 🧩 Componentes Principales

### AuthProvider
Maneja el estado de autenticación global:
- Sesión de Supabase
- Perfil de usuario
- Estados de carga
- Métodos de autenticación

### ChatWindow
Componente principal del chat:
- Streaming de mensajes SSE
- Manejo de estados de envío
- Detección de plazos
- Generación de documentos

### NotificationProvider
Sistema de notificaciones toast:
- Diferentes tipos (success, error, warning, info)
- Auto-dismiss configurable
- Acciones personalizadas

### ErrorBoundary
Captura errores de React:
- Fallback UI personalizable
- Logging de errores
- Información de debug en desarrollo

## 🎨 Estilos y UI

### Tailwind CSS
Configuración personalizada con:
- Colores de marca
- Tipografía (Fraunces + DM Sans)
- Componentes reutilizables
- Responsive design

### Componentes de UI
```typescript
// Ejemplo de componente base
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  children: React.ReactNode;
}

export function Button({ variant = 'primary', size = 'md', loading, children, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-lg font-medium transition-colors',
        variants[variant],
        sizes[size],
        loading && 'opacity-50 cursor-not-allowed'
      )}
      disabled={loading}
      {...props}
    >
      {loading && <Spinner className="mr-2" />}
      {children}
    </button>
  );
}
```

## 🔐 Autenticación

### Flujo de Autenticación
1. **Login**: Google OAuth o Magic Link
2. **Callback**: Procesamiento en `/auth/callback`
3. **Middleware**: Protección de rutas
4. **Proxy**: Inyección de tokens en API calls

### Supabase Integration
```typescript
// Configuración del cliente
export const createClient = () =>
  createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );

// Cliente para server-side
export const createServerSupabaseClient = async () => {
  const cookieStore = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          );
        },
      },
    }
  );
};
```

## 📡 Comunicación con Backend

### API Client
```typescript
// lib/api.ts
export async function apiFetch(path: string, options: RequestInit = {}) {
  const url = `/api/backend${path.startsWith("/") ? path : `/${path}`}`;
  return fetch(url, { ...options, credentials: "include" });
}
```

### Server-Sent Events (SSE)
```typescript
// Streaming de chat
const response = await fetch("/api/backend/chat", {
  method: "POST",
  body: JSON.stringify({ message, conversation_id }),
});

const reader = response.body?.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  // Procesar eventos SSE
}
```

## 🧪 Testing

### Configuración
- **Jest** + **React Testing Library**
- **MSW** para mocking de APIs
- **@testing-library/user-event** para interacciones

### Ejemplos de Tests

#### Componente
```typescript
import { render, screen } from '@testing-library/react';
import { AuthProvider } from '@/context/AuthContext';
import { LoginForm } from './LoginForm';

const MockedLoginForm = () => (
  <AuthProvider>
    <LoginForm />
  </AuthProvider>
);

test('renders login form', () => {
  render(<MockedLoginForm />);
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/contraseña/i)).toBeInTheDocument();
});
```

#### Hook
```typescript
import { renderHook, act } from '@testing-library/react';
import { useFormState } from '@/hooks/useFormState';

test('useFormState manages form state correctly', () => {
  const { result } = renderHook(() => useFormState());
  
  expect(result.current.loading).toBe(false);
  expect(result.current.error).toBe(null);
  
  act(() => {
    result.current.setLoading(true);
  });
  
  expect(result.current.loading).toBe(true);
});
```

## 🚀 Deployment

### Vercel (Recomendado)
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Variables de Entorno en Producción
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Build Optimization
- **Bundle Analyzer**: `npm run analyze`
- **Tree Shaking**: Automático con Next.js
- **Code Splitting**: Por rutas y componentes

## 🔧 Herramientas de Desarrollo

### ESLint + Prettier
```json
// .eslintrc.json
{
  "extends": ["next/core-web-vitals", "@typescript-eslint/recommended"],
  "rules": {
    "prefer-const": "error",
    "no-unused-vars": "warn"
  }
}
```

### TypeScript
- Strict mode habilitado
- Path mapping configurado (`@/`)
- Tipos centralizados en `/types`

### Tailwind CSS
```javascript
// tailwind.config.js
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#1A56DB',
        secondary: '#6B7280',
      },
    },
  },
};
```

## 📊 Performance

### Core Web Vitals
- **LCP**: < 2.5s
- **FID**: < 100ms
- **CLS**: < 0.1

### Optimizaciones
- **Image Optimization**: `next/image`
- **Font Optimization**: `next/font`
- **Static Generation**: Para páginas de contenido
- **Streaming**: Para componentes pesados

## 🐛 Debugging

### Development Tools
```typescript
// Logging condicional
if (process.env.NODE_ENV === 'development') {
  console.log('Debug info:', data);
}

// Error Boundary con detalles
{process.env.NODE_ENV === 'development' && error && (
  <details>
    <summary>Error Details</summary>
    <pre>{error.stack}</pre>
  </details>
)}
```

### Browser DevTools
- React Developer Tools
- Network tab para API calls
- Console para logs y errores

---

Para más información, consulta la documentación principal del proyecto.