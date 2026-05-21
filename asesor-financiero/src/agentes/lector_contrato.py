from langchain_core.messages import HumanMessage, SystemMessage
from src.prompts.lector_contrato import SISTEMA, USUARIO


def crear_nodo_lector(llm):
    """Retorna el nodo LangGraph que extrae información estructurada de un contrato."""
    def nodo(estado: dict) -> dict:
        texto = estado["texto_documento"]
        mensajes = [
            SystemMessage(content=SISTEMA),
            HumanMessage(content=USUARIO.format(texto_contrato=texto)),
        ]
        respuesta = llm.invoke(mensajes)
        return {"datos_contrato": respuesta.content}

    return nodo
