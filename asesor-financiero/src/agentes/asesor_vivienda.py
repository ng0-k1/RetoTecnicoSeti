import logging
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from src.prompts.asesor_vivienda import (
    SMMLV_2026,
    SISTEMA,
    CON_CONTRATO,
    SIN_CONTRATO,
    SIN_INGRESO,
    SIN_INGRESO_CON_CONTRATO,
)
from src.herramientas.busqueda_web import buscar_web
from src.utilidades.texto import escapar_llaves

logger = logging.getLogger(__name__)


def crear_nodo_asesor_vivienda(llm):
    """Retorna el nodo LangGraph especializado en análisis de crédito hipotecario.

    El LLM decide cuándo y qué buscar en la web usando la herramienta buscar_web.
    """
    agente = create_agent(llm, tools=[buscar_web], system_prompt=SISTEMA)

    def nodo(estado: dict) -> dict:
        ingreso_original = estado.get("ingreso_mensual", 0.0)
        datos_contrato = estado.get("datos_contrato")

        ingreso_asumido = not ingreso_original
        ingreso = ingreso_original if ingreso_original else SMMLV_2026

        logger.info(
            "[vivienda] ingreso_original=%s ingreso_asumido=%s contrato=%s",
            ingreso_original, ingreso_asumido, bool(datos_contrato),
        )

        nota_smmlv = (
            "\nNOTA: El usuario no indicó su ingreso. Se asume el SMMLV 2026 ($1.423.500 COP)."
            if ingreso_asumido
            else ""
        )

        if datos_contrato and ingreso_asumido:
            ruta = "SIN_INGRESO_CON_CONTRATO"
            prompt = SIN_INGRESO_CON_CONTRATO.format(
                datos_contrato=escapar_llaves(datos_contrato),
            )
        elif datos_contrato:
            ruta = "CON_CONTRATO"
            prompt = CON_CONTRATO.format(
                ingreso_mensual=ingreso,
                nota_smmlv=nota_smmlv,
                datos_contrato=escapar_llaves(datos_contrato),
            )
        elif ingreso_asumido:
            ruta = "SIN_INGRESO"
            prompt = SIN_INGRESO
        else:
            ruta = "SIN_CONTRATO"
            prompt = SIN_CONTRATO.format(
                ingreso_mensual=ingreso,
                nota_smmlv=nota_smmlv,
                cuota_maxima=ingreso * 0.3,
            )

        logger.info("[vivienda] ruta=%s prompt_chars=%d", ruta, len(prompt))

        try:
            resultado = agente.invoke({
                "messages": [HumanMessage(content=prompt)]
            })
            contenido = resultado["messages"][-1].content
            logger.info("[vivienda] respuesta_chars=%d", len(contenido))
            return {"analisis": contenido}
        except Exception as exc:
            logger.exception("[vivienda] error en el agente: %s", exc)
            raise

    return nodo
