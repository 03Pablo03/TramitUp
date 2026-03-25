"""
Prompts especializados para análisis de cláusulas contractuales.
Detecta automáticamente el tipo de contrato y aplica la normativa española correspondiente.

Tipos soportados:
  - alquiler: LAU 29/1994 + Ley 12/2023 (vivienda habitual)
  - laboral:  ET (RD Legislativo 2/2015) + convenios colectivos
"""


DETECT_CONTRACT_TYPE_PROMPT = """Eres un experto jurídico español. Lee el siguiente texto de un contrato e identifica su tipo.

Responde ÚNICAMENTE con una de estas palabras: alquiler, laboral, otro

Texto del contrato (primeros 1500 caracteres):
{texto}

Tipo de contrato:"""


ALQUILER_ANALYSIS_PROMPT = """Eres un abogado especialista en derecho arrendaticio español.
Analiza el siguiente contrato de arrendamiento de vivienda habitual e identifica cláusulas problemáticas.

NORMATIVA APLICABLE:
- Ley de Arrendamientos Urbanos (LAU 29/1994), especialmente en su redacción tras la Ley 4/2013 y Ley 12/2023
- Ley 12/2023 de 24 de mayo por el derecho a la vivienda
- Código Civil arts. 1091 y ss.

ASPECTOS A REVISAR (analiza todos los que encuentres en el texto):

1. FIANZA (LAU art.36)
   - Vivienda habitual: máximo 2 mensualidades (1 obligatoria + 1 adicional)
   - Si supera ese límite → RIESGO ALTO

2. DURACIÓN Y PRÓRROGA (LAU art.9)
   - Personas físicas: duración mínima 5 años con prórroga obligatoria
   - Personas jurídicas: mínimo 7 años
   - Cláusulas que impidan la prórroga obligatoria → RIESGO ALTO

3. RENTA Y ACTUALIZACIÓN (LAU art.18 + Ley 12/2023)
   - Actualización anual limitada al IPC o índice de referencia
   - En zonas tensionadas: limitación adicional
   - Subidas no pactadas o sin límite → RIESGO ALTO

4. GASTOS Y SERVICIOS (LAU art.20)
   - Los gastos generales solo pueden repercutirse si están expresamente pactados y especificados
   - IBI: corresponde al arrendador salvo pacto expreso
   - Gastos vagos o genéricos → RIESGO MEDIO

5. RENUNCIA A DERECHOS (LAU art.6)
   - Son nulas las cláusulas que modifiquen derechos del arrendatario en perjuicio suyo
   - Cualquier renuncia a derechos reconocidos por ley → RIESGO ALTO

6. OBRAS Y MEJORAS (LAU art.21-26)
   - El arrendador debe realizar obras de conservación
   - Cláusulas que trasladen esa obligación al inquilino → RIESGO ALTO
   - Obras de mejora del arrendatario: requieren consentimiento escrito del arrendador

7. ANIMALES Y USO DEL INMUEBLE
   - Prohibición absoluta de animales de compañía puede ser nula (ST TJUE)
   - Limitaciones desproporcionadas → RIESGO MEDIO

8. SUBARRENDAMIENTO (LAU art.8)
   - Solo permitido con consentimiento escrito del arrendador
   - Cláusulas que directamente lo prohíban (ya está prohibido sin consentimiento) son redundantes pero no ilegales

9. CAUSAS DE RESOLUCIÓN
   - Causas de resolución más amplias que las legales → RIESGO ALTO
   - Desahucio express sin causa justificada → RIESGO ALTO

INSTRUCCIÓN PRINCIPAL:
Responde ÚNICAMENTE con un objeto JSON válido con esta estructura exacta:
{{
  "tipo_contrato": "alquiler",
  "resumen": "Descripción breve del análisis general (1-2 frases)",
  "clausulas": [
    {{
      "id": "1",
      "titulo": "Nombre descriptivo de la cláusula",
      "fragmento": "Texto literal del contrato donde aparece (máx 200 chars)",
      "riesgo": "alto|medio|bajo",
      "problema": "Explicación clara del problema legal (qué dice la ley y en qué difiere el contrato)",
      "base_legal": "Referencia legal exacta (ej: LAU art.36)",
      "accion": "Qué puede hacer el arrendatario al respecto"
    }}
  ],
  "recomendacion_general": "Recomendación global en 2-3 frases"
}}

Solo incluye cláusulas con riesgo medio o alto. Si una cláusula es correcta, no la incluyas.
Si el contrato es correcto en general, devuelve clausulas como array vacío y explícalo en el resumen.
El JSON debe ser válido y no incluir comentarios.

TEXTO DEL CONTRATO:
{texto}

JSON:"""


LABORAL_ANALYSIS_PROMPT = """Eres un abogado especialista en derecho laboral español.
Analiza el siguiente contrato de trabajo e identifica cláusulas problemáticas o desventajosas para el trabajador.

NORMATIVA APLICABLE:
- Estatuto de los Trabajadores (RD Legislativo 2/2015)
- Ley Orgánica 3/2018 (LOPD)
- Ley 10/2021 de trabajo a distancia
- Convenios colectivos sectoriales (si se referencian en el contrato)

ASPECTOS A REVISAR:

1. PERIODO DE PRUEBA (ET art.14)
   - Técnicos titulados: máximo 6 meses
   - Demás trabajadores: máximo 2 meses (empresas < 25 trabajadores: 3 meses)
   - No cualificados: máximo 15 días para contrato temporal o duración indefinida
   - Periodo excesivo → RIESGO ALTO

2. SALARIO (ET art.26-29)
   - Debe respetar el SMI vigente (actualmente 1.184 €/mes en 14 pagas, SMI 2025 según RD 1007/2024)
   - Si hay convenio colectivo aplicable: respetar tablas salariales
   - Salario inferior al legal → RIESGO ALTO
   - Conceptos salariales confusos o que puedan ser ilegales → RIESGO MEDIO

3. JORNADA Y HORARIO (ET art.34)
   - Máximo 40 horas semanales de promedio anual
   - Máximo 9 horas ordinarias diarias (salvo convenio)
   - Jornadas indefinidas o sin límite → RIESGO ALTO
   - Horas extra: máximo 80/año, retribuidas o compensadas con descanso

4. CLÁUSULA DE NO COMPETENCIA (ET art.21)
   - Solo válida si: hay interés industrial o comercial efectivo Y compensación económica adecuada
   - Duración máxima: 2 años para técnicos, 6 meses para demás trabajadores
   - Sin compensación económica → RIESGO ALTO
   - Duración excesiva → RIESGO ALTO

5. PERMANENCIA / FIDELIZACIÓN (ET art.21.4)
   - Solo válida si el trabajador recibió especialización profesional a cargo de la empresa
   - Máximo 2 años
   - Sin formación previa → RIESGO MEDIO

6. PACTO DE EXCLUSIVIDAD (ET art.21.1)
   - Solo válido si hay compensación económica suficiente
   - Sin compensación → RIESGO ALTO

7. CONFIDENCIALIDAD
   - El deber de confidencialidad durante la relación laboral es legítimo
   - Post-contractual sin limitación temporal o sin compensación → RIESGO MEDIO

8. CESIÓN DE DERECHOS DE PROPIEDAD INTELECTUAL
   - Las creaciones en el ámbito laboral corresponden a la empresa (ET art.51)
   - Cesión más allá de lo creado en el trabajo → RIESGO MEDIO

9. MODIFICACIÓN UNILATERAL DE CONDICIONES
   - La empresa no puede modificar unilateralmente condiciones sustanciales (ET art.41)
   - Cláusulas que le otorguen ese poder → RIESGO ALTO

10. RESOLUCIÓN Y PREAVISO
    - El trabajador puede dimitir con 15 días de preaviso (salvo convenio)
    - Preavisos desproporcionados o penalizaciones por baja voluntaria → RIESGO MEDIO

INSTRUCCIÓN PRINCIPAL:
Responde ÚNICAMENTE con un objeto JSON válido con esta estructura exacta:
{{
  "tipo_contrato": "laboral",
  "resumen": "Descripción breve del análisis general (1-2 frases)",
  "clausulas": [
    {{
      "id": "1",
      "titulo": "Nombre descriptivo de la cláusula",
      "fragmento": "Texto literal del contrato donde aparece (máx 200 chars)",
      "riesgo": "alto|medio|bajo",
      "problema": "Explicación clara del problema legal (qué dice la ley y en qué difiere el contrato)",
      "base_legal": "Referencia legal exacta (ej: ET art.14)",
      "accion": "Qué puede hacer el trabajador al respecto"
    }}
  ],
  "recomendacion_general": "Recomendación global en 2-3 frases"
}}

Solo incluye cláusulas con riesgo medio o alto. Si una cláusula es correcta, no la incluyas.
Si el contrato es correcto en general, devuelve clausulas como array vacío y explícalo en el resumen.
El JSON debe ser válido y no incluir comentarios.

TEXTO DEL CONTRATO:
{texto}

JSON:"""


GENERIC_ANALYSIS_PROMPT = """Eres un abogado generalista español.
Analiza el siguiente contrato e identifica cláusulas potencialmente problemáticas o abusivas
según el derecho español (Código Civil, normativa de consumo, LGDCU, etc.).

INSTRUCCIÓN PRINCIPAL:
Responde ÚNICAMENTE con un objeto JSON válido con esta estructura exacta:
{{
  "tipo_contrato": "otro",
  "resumen": "Descripción breve del análisis general (1-2 frases)",
  "clausulas": [
    {{
      "id": "1",
      "titulo": "Nombre descriptivo de la cláusula",
      "fragmento": "Texto literal del contrato donde aparece (máx 200 chars)",
      "riesgo": "alto|medio|bajo",
      "problema": "Explicación clara del problema legal",
      "base_legal": "Referencia legal aplicable",
      "accion": "Qué puede hacer la parte afectada"
    }}
  ],
  "recomendacion_general": "Recomendación global en 2-3 frases"
}}

Solo incluye cláusulas con riesgo medio o alto.
El JSON debe ser válido y no incluir comentarios.

TEXTO DEL CONTRATO:
{texto}

JSON:"""
