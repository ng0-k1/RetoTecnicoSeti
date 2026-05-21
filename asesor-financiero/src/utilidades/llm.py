import os
from langchain_openai import ChatOpenAI


def crear_llm() -> ChatOpenAI:
    """Crea el LLM principal con dos fallbacks automáticos para mayor resiliencia.

    Cadena de modelos:
    1. GLM-4.5 Air (Z.ai) - rápido, gratuito
    2. DeepSeek V4 Flash - 1M contexto, gratuito
    3. Nemotron 3 Super (NVIDIA) - 1M contexto, activa si los anteriores alcanzan límite
    """
    api_key = os.environ["OPENROUTER_API_KEY"]
    url_base = "https://openrouter.ai/api/v1"

    opciones = dict(api_key=api_key, base_url=url_base, temperature=0.1, max_tokens=6000)

    principal = ChatOpenAI(model="z-ai/glm-4.5-air:free", **opciones)
    secundario = ChatOpenAI(model="deepseek/deepseek-v4-flash:free", **opciones)
    terciario = ChatOpenAI(model="nvidia/nemotron-3-super-120b-a12b:free", **opciones)

    return principal.with_fallbacks([secundario, terciario])
