Crea una migración de base de datos para Supabase en TramitUp.

**Pasos:**

1. Lee el esquema actual de las tablas relevantes consultando `backend/app/services/` para entender las queries existentes
2. Lee `backend/app/core/supabase_client.py` para entender el cliente
3. Define el SQL de la migración:
   ```sql
   -- Migración: descripción_cambio
   -- Fecha: YYYY-MM-DD

   -- 1. Crear nueva tabla (si aplica)
   CREATE TABLE IF NOT EXISTS nombre_tabla (
     id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
     user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
     ...
     created_at TIMESTAMPTZ DEFAULT NOW()
   );

   -- 2. Añadir columna (si aplica)
   ALTER TABLE tabla_existente ADD COLUMN IF NOT EXISTS nueva_columna TEXT;

   -- 3. RLS policies (SIEMPRE para tablas con user_id)
   ALTER TABLE nombre_tabla ENABLE ROW LEVEL SECURITY;
   CREATE POLICY "users_own_data" ON nombre_tabla
     FOR ALL USING (auth.uid() = user_id);

   -- 4. Índices necesarios
   CREATE INDEX IF NOT EXISTS idx_tabla_user_id ON nombre_tabla(user_id);
   ```
4. Verifica que la migración es reversible (documenta el rollback)
5. Actualiza el agente `db-specialist.md` con el nuevo esquema
6. Actualiza los servicios Python que usan la tabla modificada
7. Si añades nueva tabla, verificar que aparece en el checklist de `deploy-check.md`

**Cambio de base de datos:** $ARGUMENTS
