Analiza y optimiza el rendimiento de una parte específica de TramitUp.

**Análisis de performance:**

### Backend — identifica cuellos de botella

1. Lee `backend/app/core/monitoring.py` para ver métricas existentes
2. Busca queries lentas:
   ```python
   # Señales de alerta:
   # - SELECT * sin filtros o sin índices
   # - N+1 queries en bucles
   # - Sin .range() en listas grandes
   # - Llamadas síncronas en endpoints async
   ```
3. Identifica oportunidades de caché:
   - Templates estáticos (TRAMITE_TEMPLATES, WORKFLOW_TEMPLATES) → caché indefinida
   - Datos de perfil del usuario → caché con TTL corto (60s)
   - Resultados de clasificación repetidos → caché con TTL 5min

### Frontend — identifica re-renders y bundle issues

1. Revisa componentes con muchos re-renders:
   - Estados que se actualizan frecuentemente (`messages[]`, `sending`)
   - Listas largas sin virtualización
   - Funciones recreadas en cada render sin `useCallback`
2. Busca imports pesados:
   ```typescript
   // MAL: importa toda la librería
   import * as lodash from 'lodash';
   // BIEN: import específico
   import debounce from 'lodash/debounce';
   ```
3. Identifica fetches no paralelos que podrían ser `Promise.all()`

### Optimizaciones a implementar

Para cada bottleneck encontrado:
1. Describe el problema y su impacto estimado
2. Propone la solución concreta con código
3. Implementa la optimización
4. Verifica que el comportamiento es idéntico
5. Estima la mejora de rendimiento

### Métricas objetivo
- API endpoints principales: < 200ms p95
- SSE primer chunk: < 1s
- Dashboard load: < 1.5s
- Bundle JS: < 200KB gzip para la página principal

**Área a optimizar:** $ARGUMENTS
