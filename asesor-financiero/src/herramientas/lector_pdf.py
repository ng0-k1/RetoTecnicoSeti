import pdfplumber
from langchain_core.tools import tool


@tool
def leer_pdf(ruta_archivo: str) -> str:
    """Extrae el texto plano de un archivo PDF dada su ruta."""
    try:
        with pdfplumber.open(ruta_archivo) as pdf:
            texto = "\n".join(
                pagina.extract_text() or ""
                for pagina in pdf.pages
            )
        texto = texto.strip()
        if not texto:
            return "El PDF no contiene texto extraíble. Puede ser un archivo escaneado."
        return texto
    except Exception as error:
        return f"No se pudo leer el archivo: {error}"
