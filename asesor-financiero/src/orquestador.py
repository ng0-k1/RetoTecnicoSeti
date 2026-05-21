from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END, START
from src.agentes.lector_contrato import crear_nodo_lector
from src.agentes.asesor_vivienda import crear_nodo_asesor_vivienda
from src.agentes.asesor_vehiculo import crear_nodo_asesor_vehiculo
from src.agentes.generador_reporte import crear_nodo_reporte


class EstadoAsesor(TypedDict):
    texto_documento: Optional[str]
    tipo_activo: str
    ingreso_mensual: float
    datos_contrato: Optional[str]
    analisis: Optional[str]
    reporte_final: Optional[str]


def decidir_entrada(estado: EstadoAsesor) -> str:
    """Si hay documento va al lector; si no, va directo al asesor del tipo de activo."""
    if estado.get("texto_documento"):
        return "lector_contrato"
    return f"asesor_{estado['tipo_activo']}"


def decidir_tipo_activo(estado: EstadoAsesor) -> str:
    """Despues de leer el contrato, enruta al asesor especializado segun el tipo de activo."""
    return f"asesor_{estado['tipo_activo']}"


def crear_grafo(llm):
    """Construye y compila el grafo con cuatro nodos: lector, dos asesores especializados y reporte."""
    grafo = StateGraph(EstadoAsesor)

    grafo.add_node("lector_contrato", crear_nodo_lector(llm))
    grafo.add_node("asesor_vivienda", crear_nodo_asesor_vivienda(llm))
    grafo.add_node("asesor_vehiculo", crear_nodo_asesor_vehiculo(llm))
    grafo.add_node("generador_reporte", crear_nodo_reporte(llm))

    grafo.add_conditional_edges(
        START,
        decidir_entrada,
        {
            "lector_contrato": "lector_contrato",
            "asesor_vivienda": "asesor_vivienda",
            "asesor_vehiculo": "asesor_vehiculo",
        },
    )

    grafo.add_conditional_edges(
        "lector_contrato",
        decidir_tipo_activo,
        {
            "asesor_vivienda": "asesor_vivienda",
            "asesor_vehiculo": "asesor_vehiculo",
        },
    )

    grafo.add_edge("asesor_vivienda", "generador_reporte")
    grafo.add_edge("asesor_vehiculo", "generador_reporte")
    grafo.add_edge("generador_reporte", END)

    return grafo.compile()
