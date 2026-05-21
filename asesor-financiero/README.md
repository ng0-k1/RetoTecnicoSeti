# Asesor de Contratos y Financiación

Sistema multiagente para analizar contratos de compra de vivienda o vehículo y generar recomendaciones financieras personalizadas en Colombia.

## Qué hace

- Lee contratos en PDF o texto plano y extrae las condiciones clave
- Busca tasas de crédito actuales en la web según el tipo de activo
- Compara opciones de entidades reales (FNA, Bancolombia, Davivienda, BBVA, entre otras)
- Recomienda la opción más adecuada según el ingreso del usuario (asume SMMLV 2026 si no se indica)
- Genera un reporte descargable en Markdown

## Arquitectura

Cuatro agentes orquestados con LangGraph:

1. **Lector de contrato** — extrae cláusulas clave del documento PDF o texto
2. **Asesor de vivienda** — especializado en crédito hipotecario: UVR, pesos fijos, leasing habitacional, FNA, Banco Agrario, Bancolombia, Davivienda, BBVA, Scotiabank, AV Villas
3. **Asesor de vehículo** — especializado en crédito vehicular: Bancolombia, Davivienda, BBVA, Scotiabank, Banco de Bogotá, Fincomercio (sin FNA ni UVR)
4. **Generador de reporte** — formatea el análisis como reporte descargable

El orquestador enruta en dos puntos de decisión:

- Desde el inicio: si hay documento va al lector; si no, va directo al asesor del tipo de activo
- Desde el lector: enruta al asesor de vivienda o vehículo según el tipo seleccionado

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Cuenta en [OpenRouter](https://openrouter.ai/) con API key (capa gratuita funciona)

## Instalación

```bash
git clone <url-del-repositorio>
cd asesor-financiero
uv sync
cp .env.example .env
```

Edita `.env` y agrega tu `OPENROUTER_API_KEY`.

## Ejecución

```bash
uv run streamlit run app.py
```

La aplicación abre en `http://localhost:8501`.

## Variables de entorno

| Variable | Descripción |
|---|---|
| `OPENROUTER_API_KEY` | API key de OpenRouter |

## Modelos utilizados

| Rol | Modelo |
|---|---|
| Principal | `z-ai/glm-4.5-air:free` |
| Fallback 1 | `deepseek/deepseek-v4-flash:free` |
| Fallback 2 | `nvidia/nemotron-3-super-120b-a12b:free` |

## Estructura del proyecto

```
src/
  agentes/
    lector_contrato.py      — extrae texto y condiciones del documento
    asesor_vivienda.py      — analisis hipotecario (FNA, Banco Agrario, etc.)
    asesor_vehiculo.py      — analisis vehicular (Bancolombia, Davivienda, etc.)
    generador_reporte.py    — genera reporte Markdown descargable
  prompts/
    lector_contrato.py
    asesor_vivienda.py
    asesor_vehiculo.py
    generador_reporte.py
  herramientas/
    busqueda_web.py         — busqueda DuckDuckGo sin API key
  utilidades/
    llm.py                  — cadena de modelos con fallbacks
    texto.py                — utilidades de texto compartidas
  orquestador.py            — grafo LangGraph con enrutamiento condicional
app.py                      — interfaz Streamlit
```
