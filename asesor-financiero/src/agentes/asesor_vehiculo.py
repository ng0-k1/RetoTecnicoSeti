import logging
from langchain_core.messages import HumanMessage, SystemMessage
from src.prompts.asesor_vehiculo import (
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


def crear_nodo_asesor_vehiculo(llm):
    """Retorna el nodo LangGraph especializado en analisis de credito vehicular."""
    def nodo(estado: dict) -> dict:
        ingreso_original = estado.get("ingreso_mensual", 0.0)
        datos_contrato = estado.get("datos_contrato")

        ingreso_asumido = not ingreso_original
        ingreso = ingreso_original if ingreso_original else SMMLV_2026

        logger.info(
            "[vehiculo] ingreso_original=%s ingreso_asumido=%s contrato=%s",
            ingreso_original, ingreso_asumido, bool(datos_contrato),
        )

        nota_smmlv = (
            "\nNOTA: El usuario no indico su ingreso. Se asume el SMMLV 2026 ($1.423.500 COP)."
            if ingreso_asumido
            else ""
        )

        tasas_raw = buscar_web.invoke("tasas credito vehicular Colombia 2026")
        logger.info("[vehiculo] busqueda_mercado preview=%r", tasas_raw[:100])
        tasas_mercado = escapar_llaves(tasas_raw[:500])

        instituciones_raw = buscar_web.invoke(
            "tasas credito vehicular Bancolombia Davivienda BBVA Scotiabank Colombia 2026"
        )
        logger.info("[vehiculo] busqueda_instituciones preview=%r", instituciones_raw[:100])
        tasas_instituciones = escapar_llaves(instituciones_raw[:500])

        if datos_contrato and ingreso_asumido:
            ruta = "SIN_INGRESO_CON_CONTRATO"
            prompt_usuario = SIN_INGRESO_CON_CONTRATO.format(
                datos_contrato=escapar_llaves(datos_contrato),
                tasas_actuales=tasas_mercado,
                tasas_instituciones=tasas_instituciones,
            )
        elif datos_contrato:
            ruta = "CON_CONTRATO"
            prompt_usuario = CON_CONTRATO.format(
                ingreso_mensual=ingreso,
                nota_smmlv=nota_smmlv,
                datos_contrato=escapar_llaves(datos_contrato),
                tasas_actuales=tasas_mercado,
                tasas_instituciones=tasas_instituciones,
            )
        elif ingreso_asumido:
            ruta = "SIN_INGRESO"
            prompt_usuario = SIN_INGRESO.format(
                tasas_actuales=tasas_mercado,
                tasas_instituciones=tasas_instituciones,
            )
        else:
            ruta = "SIN_CONTRATO"
            prompt_usuario = SIN_CONTRATO.format(
                ingreso_mensual=ingreso,
                nota_smmlv=nota_smmlv,
                cuota_maxima=ingreso * 0.3,
                tasas_actuales=tasas_mercado,
                tasas_instituciones=tasas_instituciones,
            )

        logger.info("[vehiculo] ruta=%s prompt_chars=%d", ruta, len(prompt_usuario))

        mensajes = [
            SystemMessage(content=SISTEMA),
            HumanMessage(content=prompt_usuario),
        ]

        try:
            respuesta = llm.invoke(mensajes)
            logger.info(
                "[vehiculo] respuesta_chars=%d finish_reason=%s",
                len(respuesta.content),
                respuesta.response_metadata.get("finish_reason"),
            )
            return {"analisis": respuesta.content}
        except Exception as exc:
            logger.exception("[vehiculo] error al invocar LLM: %s", exc)
            raise

    return nodo
