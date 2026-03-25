"""
BOT 3: Community Response Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Genera respuestas para participar en grupos de Facebook de forma organica.

Estrategia:
  - Responder preguntas legales comunes con valor real
  - Posicionar TramitUp como recurso util (sin spam)
  - Generar confianza antes de mencionar la app

Grupos objetivo:
  - Inquilinos y problemas de alquiler
  - Derechos laborales y despidos
  - Consumidores y reclamaciones
  - Tramites y burocracia en España

USO:
  python -m marketing.bots.community_bot --topic alquiler --question "Mi casero quiere subir el alquiler un 20%"
  python -m marketing.bots.community_bot --topic laboral --question "Me han despedido sin preaviso"
  python -m marketing.bots.community_bot --templates
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from marketing.config import BRAND, VOICE, CONTENT_BANK


# ─── Preguntas frecuentes por tema ──────────────────────────────────────────

FAQ_TEMPLATES = {
    "alquiler": [
        {"q": "Mi casero quiere subir el alquiler, ¿puede?",
         "context": "subida_alquiler"},
        {"q": "No me devuelven la fianza, ¿que hago?",
         "context": "fianza"},
        {"q": "Mi casero quiere entrar al piso sin avisar",
         "context": "inviolabilidad"},
        {"q": "Me quieren echar del piso, ¿pueden?",
         "context": "desahucio"},
        {"q": "¿Cuanto puede durar mi contrato de alquiler?",
         "context": "duracion_contrato"},
    ],
    "laboral": [
        {"q": "Me han despedido, ¿que plazo tengo para demandar?",
         "context": "despido_plazo"},
        {"q": "No me pagan las horas extra, ¿que hago?",
         "context": "horas_extra"},
        {"q": "¿Me pueden despedir estando de baja?",
         "context": "despido_baja"},
        {"q": "Mi empresa no me da el finiquito",
         "context": "finiquito"},
        {"q": "¿Cuantos dias de vacaciones me corresponden?",
         "context": "vacaciones"},
    ],
    "consumo": [
        {"q": "He comprado algo online y quiero devolverlo",
         "context": "devolucion_online"},
        {"q": "Me han cobrado de mas en la factura del telefono",
         "context": "factura_incorrecta"},
        {"q": "La tienda no quiere darme hoja de reclamaciones",
         "context": "hoja_reclamaciones"},
        {"q": "He comprado un producto defectuoso",
         "context": "producto_defectuoso"},
    ],
    "multas": [
        {"q": "Me han puesto una multa injusta, ¿como recurro?",
         "context": "recurrir_multa"},
        {"q": "¿Puedo pagar la multa con descuento?",
         "context": "descuento_multa"},
        {"q": "No he pagado una multa y me llega un recargo",
         "context": "recargo_multa"},
    ],
    "herencias": [
        {"q": "¿Cuanto cuesta heredar una casa?",
         "context": "coste_herencia"},
        {"q": "¿Puedo renunciar a una herencia?",
         "context": "renuncia_herencia"},
        {"q": "Mi familiar fallecio sin testamento",
         "context": "sin_testamento"},
    ],
    "vuelos": [
        {"q": "Mi vuelo se ha retrasado 4 horas, ¿me compensan?",
         "context": "retraso_vuelo"},
        {"q": "Me han cancelado el vuelo, ¿que hago?",
         "context": "cancelacion_vuelo"},
    ],
}

# ─── Respuestas por contexto ────────────────────────────────────────────────

RESPONSE_BANK = {
    "subida_alquiler": {
        "legal_points": [
            "La subida de alquiler esta regulada por la LAU (art. 18).",
            "Solo puede subirse segun el indice de referencia oficial.",
            "Si tu contrato no dice nada sobre subida, no puede subirlo libremente.",
        ],
        "actionable": "Revisa tu contrato y comprueba si hay clausula de actualizacion. Si no la hay, la subida del 20% no es legal.",
    },
    "fianza": {
        "legal_points": [
            "La fianza solo puede retenerse por daños reales, no por desgaste normal.",
            "El casero tiene 30 dias para devolver la fianza tras la entrega de llaves.",
            "Puedes reclamar intereses si tarda mas de 30 dias.",
        ],
        "actionable": "Haz fotos del estado del piso al irte. Si no te devuelven, reclama por escrito con burofax.",
    },
    "inviolabilidad": {
        "legal_points": [
            "Art. 18 de la Constitucion: inviolabilidad del domicilio.",
            "Tu casero NO puede entrar sin tu permiso, ni con llaves propias.",
            "Si entra sin permiso, es allanamiento de morada.",
        ],
        "actionable": "Comunica por escrito que no autorizas la entrada. Si insiste, denuncia.",
    },
    "desahucio": {
        "legal_points": [
            "No pueden echarte sin orden judicial.",
            "El desahucio express requiere proceso judicial.",
            "Si llevas menos de 5 años, el contrato no puede rescindirse sin causa.",
        ],
        "actionable": "No abandones el piso. Busca asesoria legal inmediata si te amenazan.",
    },
    "duracion_contrato": {
        "legal_points": [
            "Contrato minimo: 5 años si el casero es persona fisica.",
            "7 años si el casero es empresa (LAU 2019).",
            "Prorroga tacita de 3 años adicionales tras el periodo minimo.",
        ],
        "actionable": "Revisa la fecha de tu contrato. Si es posterior a 2019, aplica la nueva LAU.",
    },
    "despido_plazo": {
        "legal_points": [
            "Plazo para demandar por despido: 20 dias habiles.",
            "Empieza a contar desde que te entregan la carta de despido.",
            "Si no demandas en plazo, pierdes el derecho.",
        ],
        "actionable": "No firmes la carta como 'conforme'. Acude a un abogado laboralista o al SMAC urgentemente.",
    },
    "horas_extra": {
        "legal_points": [
            "Las horas extra son voluntarias (salvo pacto).",
            "Maximo 80 horas extra al año.",
            "La empresa debe registrar tu jornada (obligatorio desde 2019).",
        ],
        "actionable": "Pide copia de tu registro horario. Si no lo tienen, denuncia a Inspeccion de Trabajo.",
    },
    "despido_baja": {
        "legal_points": [
            "Desde la reforma laboral 2022, el despido durante IT es nulo si no hay causa.",
            "Si te despiden estando de baja, se presume discriminacion.",
            "Despido nulo = readmision obligatoria + salarios de tramitacion.",
        ],
        "actionable": "Guarda la carta de despido y el parte de baja. Demanda inmediatamente.",
    },
    "finiquito": {
        "legal_points": [
            "El finiquito es obligatorio al finalizar cualquier relacion laboral.",
            "Incluye: salario pendiente, vacaciones no disfrutadas, parte proporcional de pagas.",
            "Plazo para reclamar: 1 año desde que te lo deben.",
        ],
        "actionable": "Reclama por escrito. Si no responden, papeleta de conciliacion en el SMAC.",
    },
    "vacaciones": {
        "legal_points": [
            "Minimo legal: 30 dias naturales por año trabajado (art. 38 ET).",
            "Si trabajas medio año, te corresponde la parte proporcional.",
            "Las vacaciones no disfrutadas se pagan en el finiquito.",
        ],
        "actionable": "Calcula tus dias proporcionales y comparalo con lo que te ofrecen.",
    },
    "devolucion_online": {
        "legal_points": [
            "14 dias para devolver sin dar explicaciones (RD 1/2007).",
            "El plazo empieza desde que recibes el producto.",
            "Te deben devolver el dinero en 14 dias desde la devolucion.",
        ],
        "actionable": "Comunica la devolucion por escrito (email vale). Guarda el tracking del envio.",
    },
    "factura_incorrecta": {
        "legal_points": [
            "Tienes derecho a factura desglosada.",
            "Plazo para reclamar: 3 meses ante la operadora, luego Telecomunicaciones.",
            "Puedes reclamar ante la OMIC de tu ayuntamiento gratuitamente.",
        ],
        "actionable": "Reclama primero por escrito a la empresa. Si no responden en 30 dias, escala a consumo.",
    },
    "hoja_reclamaciones": {
        "legal_points": [
            "Todo establecimiento DEBE tener hojas de reclamaciones.",
            "Negarse a darla es infraccion sancionable.",
            "Puedes llamar a la policia local si se niegan.",
        ],
        "actionable": "Insiste firmemente. Si se niegan, apunta nombre del empleado y llama a policia local.",
    },
    "producto_defectuoso": {
        "legal_points": [
            "Garantia legal: 3 años para productos nuevos (desde 2022).",
            "Los primeros 2 años, se presume que el defecto era de origen.",
            "Puedes elegir entre reparacion o sustitucion.",
        ],
        "actionable": "Reclama al vendedor (no al fabricante). Guarda el ticket de compra.",
    },
    "recurrir_multa": {
        "legal_points": [
            "Plazo para recurrir: 20 dias habiles desde la notificacion.",
            "Puedes alegar defectos de forma, señalizacion incorrecta, etc.",
            "El recurso es gratuito, no necesitas abogado.",
        ],
        "actionable": "Redacta un escrito de alegaciones con tus argumentos y presentalo en el registro del organismo.",
    },
    "descuento_multa": {
        "legal_points": [
            "50% de descuento si pagas en los 20 dias naturales siguientes.",
            "Si pagas con descuento, renuncias al derecho a recurrir.",
            "Valora si merece mas la pena recurrir o pagar con descuento.",
        ],
        "actionable": "Analiza la multa. Si tienes argumentos solidos, recurre. Si no, paga con descuento.",
    },
    "recargo_multa": {
        "legal_points": [
            "Recargos: 5% (primer mes), 10% (segundo mes), 20% (despues).",
            "Ultimo paso: embargo de cuentas o nomina.",
            "Puedes pedir aplazamiento o fraccionamiento del pago.",
        ],
        "actionable": "Paga cuanto antes para evitar mas recargos. Puedes solicitar fraccionamiento.",
    },
    "coste_herencia": {
        "legal_points": [
            "Impuesto de sucesiones: varia mucho por comunidad autonoma.",
            "Plusvalia municipal si heredas un inmueble.",
            "Gastos de notaria, registro y gestoria.",
        ],
        "actionable": "Pide presupuesto a una gestoria antes de aceptar. Valora aceptar a beneficio de inventario.",
    },
    "renuncia_herencia": {
        "legal_points": [
            "La renuncia se hace ante notario y es irrevocable.",
            "Si renuncias, pasa a los siguientes herederos.",
            "No puedes renunciar parcialmente (o todo o nada).",
        ],
        "actionable": "Valora primero si hay mas deudas que bienes. La renuncia es la opcion segura si hay dudas.",
    },
    "sin_testamento": {
        "legal_points": [
            "Sin testamento: herencia se reparte por ley (sucesion intestada).",
            "Orden: hijos > padres > conyuge > hermanos > sobrinos.",
            "Necesitas declaracion de herederos ante notario.",
        ],
        "actionable": "Acude al notario con certificado de defuncion y de ultimas voluntades.",
    },
    "retraso_vuelo": {
        "legal_points": [
            "Mas de 3 horas de retraso: compensacion de 250-600€.",
            "Regulado por el Reglamento CE 261/2004.",
            "Plazo para reclamar en España: hasta 5 años.",
        ],
        "actionable": "Guarda tarjeta de embarque y cualquier comunicacion. Reclama primero a la aerolinea.",
    },
    "cancelacion_vuelo": {
        "legal_points": [
            "Si te avisan con menos de 14 dias: compensacion obligatoria.",
            "Ademas de compensacion, deben ofrecerte vuelo alternativo o reembolso.",
            "La aerolinea debe cubrir comidas y hotel si es necesario.",
        ],
        "actionable": "No aceptes solo un vuelo alternativo sin preguntar por la compensacion economica.",
    },
}


def generate_response(topic: str, question: str = None) -> dict:
    """Genera una respuesta para un grupo de Facebook."""
    faqs = FAQ_TEMPLATES.get(topic, [])
    if question:
        # Find closest match or use first
        matched = None
        for faq in faqs:
            if any(word in question.lower() for word in faq["q"].lower().split()):
                matched = faq
                break
        if not matched:
            matched = faqs[0] if faqs else {"q": question, "context": list(RESPONSE_BANK.keys())[0]}
    else:
        matched = random.choice(faqs) if faqs else {"q": f"Pregunta sobre {topic}", "context": "subida_alquiler"}

    context = matched.get("context", "subida_alquiler")
    data = RESPONSE_BANK.get(context, {"legal_points": ["Consulta con un profesional."], "actionable": "Busca asesoria."})

    # Build natural response
    intro_options = [
        "¡Buena pregunta!",
        "Esto es algo que mucha gente no sabe.",
        "Te cuento lo que dice la ley:",
        "Es una situacion mas comun de lo que crees.",
    ]

    bridge_to_app = [
        f"Si quieres revisar tu caso concreto, hay una app que se llama {BRAND['name']} donde puedes consultar gratis.",
        f"Para tu caso especifico, puedes probar {BRAND['name']} (es gratuita) y te dice exactamente que hacer paso a paso.",
        f"Yo uso {BRAND['name']} para este tipo de consultas, te explica tus derechos de forma sencilla.",
    ]

    response_text = random.choice(intro_options) + "\n\n"
    for point in data["legal_points"]:
        response_text += f"• {point}\n"
    response_text += f"\n👉 {data['actionable']}\n"
    response_text += f"\n{random.choice(bridge_to_app)}"

    return {
        "metadata": {
            "topic": topic,
            "question": matched["q"],
            "context": context,
            "generated_at": datetime.now().isoformat(),
        },
        "response": {
            "text": response_text,
            "legal_points": data["legal_points"],
            "actionable": data["actionable"],
            "app_mention": True,
        },
        "guidelines": {
            "tone": VOICE["tone"],
            "dont": "No ser spam. No enlazar directamente a la app en la primera respuesta.",
            "do": "Dar valor real primero. Solo mencionar la app si es relevante.",
            "frequency": "1-2 respuestas por grupo por semana maximo.",
        },
    }


def generate_all_templates() -> list:
    """Genera respuestas para todas las preguntas frecuentes."""
    all_responses = []
    for topic, faqs in FAQ_TEMPLATES.items():
        for faq in faqs:
            resp = generate_response(topic, faq["q"])
            all_responses.append(resp)
    return all_responses


def format_response_readable(resp: dict) -> str:
    m = resp["metadata"]
    r = resp["response"]
    g = resp["guidelines"]

    lines = []
    lines.append("=" * 70)
    lines.append(f"💬 RESPUESTA COMUNIDAD — {m['topic'].upper()}")
    lines.append(f"   Pregunta: {m['question']}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("📝 RESPUESTA:")
    for line in r["text"].split("\n"):
        lines.append(f"   {line}")
    lines.append("")
    lines.append("⚠️ DIRECTRICES:")
    lines.append(f"   Tono: {g['tone']}")
    lines.append(f"   Hacer: {g['do']}")
    lines.append(f"   No hacer: {g['dont']}")
    lines.append(f"   Frecuencia: {g['frequency']}")
    lines.append("")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Community Response Bot")
    parser.add_argument("--topic", choices=list(FAQ_TEMPLATES.keys()), help="Tema")
    parser.add_argument("--question", type=str, help="Pregunta a responder")
    parser.add_argument("--templates", action="store_true", help="Genera todas las plantillas de respuesta")
    parser.add_argument("--json", action="store_true", help="Output en JSON")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if args.templates:
        responses = generate_all_templates()
        if args.json:
            out_file = output_dir / f"community_templates_{datetime.now().strftime('%Y%m%d')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(responses, f, ensure_ascii=False, indent=2)
            print(f"✅ {len(responses)} plantillas guardadas en {out_file}")
        else:
            full_text = ""
            for resp in responses:
                full_text += format_response_readable(resp) + "\n"
            out_file = output_dir / f"community_templates_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(full_text)
            print(f"✅ {len(responses)} plantillas guardadas en {out_file}")
    elif args.topic:
        resp = generate_response(args.topic, args.question)
        if args.json:
            print(json.dumps(resp, ensure_ascii=False, indent=2))
        else:
            print(format_response_readable(resp))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
