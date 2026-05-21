from langchain_core.messages import HumanMessage, SystemMessage
from src.prompts.generador_reporte import SISTEMA, USUARIO


def crear_nodo_reporte(llm):
    """Retorna el nodo LangGraph que convierte el análisis en un reporte Markdown descargable."""
    def nodo(estado: dict) -> dict:
        analisis = estado.get("analisis") or ""
        if not analisis.strip():
            return {"reporte_final": None}

        mensajes = [
            SystemMessage(content=SISTEMA),
            HumanMessage(content=USUARIO.format(analisis=analisis)),
        ]
        respuesta = llm.invoke(mensajes)
        return {"reporte_final": respuesta.content}

    return nodo
