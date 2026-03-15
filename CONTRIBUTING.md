# Guía de Contribución

¡Gracias por tu interés en contribuir a TramitUp! Esta guía te ayudará a entender cómo participar en el desarrollo del proyecto.

## 🚀 Comenzando

### Configuración del Entorno

1. **Fork** el repositorio en GitHub
2. **Clona** tu fork localmente:
   ```bash
   git clone https://github.com/tu-usuario/tramitup.git
   cd tramitup
   ```
3. **Configura** el upstream:
   ```bash
   git remote add upstream https://github.com/original/tramitup.git
   ```
4. **Instala** las dependencias siguiendo el README principal

### Estructura del Proyecto

```
TramitUp/
├── frontend/           # Next.js 14 App Router
├── backend/           # FastAPI
├── docs/              # Documentación
├── .github/           # GitHub workflows
└── scripts/           # Scripts de utilidad
```

## 📝 Estándares de Código

### TypeScript/JavaScript (Frontend)

- **Strict mode** habilitado
- **ESLint** + **Prettier** configurados
- **Convenciones de nombres**:
  - Componentes: `PascalCase`
  - Hooks: `camelCase` con prefijo `use`
  - Archivos: `kebab-case` o `camelCase`
  - Constantes: `UPPER_SNAKE_CASE`

### Python (Backend)

- **PEP 8** compliance
- **Type hints** obligatorios
- **Docstrings** para funciones públicas
- **Pydantic** para validación de datos

### Ejemplo de Código

#### Frontend (React Component)
```typescript
interface UserProfileProps {
  user: User;
  onUpdate: (user: User) => void;
}

export function UserProfile({ user, onUpdate }: UserProfileProps) {
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (data: FormData) => {
    setLoading(true);
    try {
      const updatedUser = await updateUser(data);
      onUpdate(updatedUser);
    } catch (error) {
      console.error('Error updating user:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="user-profile">
      {/* Component JSX */}
    </div>
  );
}
```

#### Backend (FastAPI Endpoint)
```python
from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import require_auth
from app.schemas.user import UserUpdate, UserResponse

router = APIRouter()

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    data: UserUpdate,
    user_id: str = Depends(require_auth)
) -> UserResponse:
    """
    Update user profile information.
    
    Args:
        data: User update data
        user_id: Authenticated user ID
        
    Returns:
        Updated user profile
        
    Raises:
        HTTPException: If update fails
    """
    try:
        updated_user = await update_user_profile(user_id, data)
        return UserResponse.from_orm(updated_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## 🧪 Testing

### Requisitos de Testing

- **Cobertura mínima**: 80%
- **Tests unitarios** para lógica de negocio
- **Tests de integración** para endpoints críticos
- **Tests de componentes** para UI crítica

### Frontend Tests

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('should render user information', () => {
    const mockUser = { id: '1', name: 'John Doe' };
    render(<UserProfile user={mockUser} onUpdate={jest.fn()} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  it('should handle form submission', async () => {
    const mockOnUpdate = jest.fn();
    render(<UserProfile user={mockUser} onUpdate={mockOnUpdate} />);
    
    fireEvent.click(screen.getByText('Update'));
    
    await waitFor(() => {
      expect(mockOnUpdate).toHaveBeenCalled();
    });
  });
});
```

### Backend Tests

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_update_profile_success():
    """Test successful profile update."""
    response = client.put(
        "/api/v1/profile",
        json={"name": "New Name"},
        headers={"Authorization": "Bearer valid-token"}
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

def test_update_profile_unauthorized():
    """Test profile update without authentication."""
    response = client.put("/api/v1/profile", json={"name": "New Name"})
    
    assert response.status_code == 401
```

## 🔄 Workflow de Desarrollo

### 1. Crear una Rama

```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/corregir-bug
# o
git checkout -b docs/actualizar-documentacion
```

### 2. Desarrollar

- Escribe código siguiendo los estándares
- Añade tests para nueva funcionalidad
- Actualiza documentación si es necesario

### 3. Commit

Usamos **Conventional Commits**:

```bash
git commit -m "feat: añadir validación de email en registro"
git commit -m "fix: corregir error en cálculo de plazos"
git commit -m "docs: actualizar guía de instalación"
git commit -m "test: añadir tests para autenticación"
```

Tipos de commit:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `test`: Tests
- `refactor`: Refactoring
- `style`: Cambios de formato
- `chore`: Tareas de mantenimiento

### 4. Push y Pull Request

```bash
git push origin feature/nueva-funcionalidad
```

Crear Pull Request con:
- **Título descriptivo**
- **Descripción detallada** de los cambios
- **Screenshots** si hay cambios visuales
- **Referencias** a issues relacionados

## 📋 Checklist para Pull Requests

- [ ] El código sigue los estándares del proyecto
- [ ] Se han añadido tests para nueva funcionalidad
- [ ] Todos los tests pasan
- [ ] La documentación está actualizada
- [ ] No hay console.log o prints de debug
- [ ] Las variables de entorno están documentadas
- [ ] Los commits siguen Conventional Commits

## 🐛 Reportar Bugs

### Información Necesaria

1. **Descripción clara** del problema
2. **Pasos para reproducir**
3. **Comportamiento esperado** vs **comportamiento actual**
4. **Entorno**:
   - OS (Windows/Mac/Linux)
   - Navegador y versión
   - Node.js y Python versions
5. **Screenshots** o **logs** si es relevante

### Template de Issue

```markdown
## Descripción
Descripción clara del bug.

## Pasos para Reproducir
1. Ir a '...'
2. Hacer click en '...'
3. Ver error

## Comportamiento Esperado
Descripción de lo que debería pasar.

## Comportamiento Actual
Descripción de lo que pasa actualmente.

## Entorno
- OS: [Windows 11]
- Navegador: [Chrome 120]
- Node.js: [20.10.0]
- Python: [3.12.0]

## Información Adicional
Screenshots, logs, etc.
```

## 💡 Solicitar Funcionalidades

### Template para Feature Request

```markdown
## Resumen
Descripción breve de la funcionalidad.

## Motivación
¿Por qué es necesaria esta funcionalidad?

## Descripción Detallada
Descripción completa de cómo debería funcionar.

## Alternativas Consideradas
¿Qué otras opciones has considerado?

## Información Adicional
Mockups, referencias, etc.
```

## 🎯 Áreas de Contribución

### Para Principiantes
- Corrección de typos en documentación
- Mejoras en mensajes de error
- Tests adicionales
- Traducción de contenido

### Nivel Intermedio
- Nuevos componentes de UI
- Optimizaciones de performance
- Mejoras en UX/UI
- Integración de APIs

### Nivel Avanzado
- Nuevas funcionalidades core
- Optimizaciones de base de datos
- Mejoras en arquitectura
- Implementación de nuevos modelos de IA

## 📚 Recursos Útiles

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Python Style Guide](https://pep8.org/)

## 🤝 Código de Conducta

- Sé respetuoso y constructivo
- Acepta feedback de manera positiva
- Ayuda a otros contribuyentes
- Mantén un ambiente inclusivo y acogedor

## ❓ Preguntas

Si tienes preguntas sobre cómo contribuir:

1. Revisa la documentación existente
2. Busca en issues cerrados
3. Abre un nuevo issue con la etiqueta "question"
4. Únete a nuestras discusiones en GitHub

---

¡Gracias por contribuir a TramitUp! 🚀