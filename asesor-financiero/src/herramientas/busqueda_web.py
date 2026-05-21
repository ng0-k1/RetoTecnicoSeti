from ddgs import DDGS
from langchain_core.tools import tool


@tool
def buscar_web(consulta: str) -> str:
    """Busca información actualizada en la web y retorna los primeros resultados relevantes."""
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(consulta, max_results=3))
        if not resultados:
            return "No se encontraron resultados para la consulta."
        return "\n\n".join(
            f"{r['title']}\n{r['body']}"
            for r in resultados
        )
    except Exception as error:
        return f"Error en la búsqueda: {error}"
