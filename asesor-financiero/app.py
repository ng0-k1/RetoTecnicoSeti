import io
import logging
import pdfplumber
import streamlit as st
from dotenv import load_dotenv
from src.orquestador import crear_grafo
from src.utilidades.llm import crear_llm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)

load_dotenv()

st.set_page_config(
    page_title="Asesor Financiero Colombia",
    page_icon="💰",
    layout="centered",
)

st.markdown(
    """
    <style>
    .bloque-info {
        background-color: #f0f4ff;
        border-left: 4px solid #4a6cf7;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 16px;
    }
    .etiqueta-peso {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a7f4b;
        margin-top: -8px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Asesor de Contratos y Financiación")
st.markdown(
    '<div class="bloque-info">Analiza contratos de vivienda o vehículo, '
    "compara opciones de crédito y recibe una recomendación personalizada "
    "según tu ingreso y las tasas actuales del mercado colombiano.</div>",
    unsafe_allow_html=True,
)

st.divider()

col_modo, col_tipo = st.columns(2)

with col_modo:
    modo = st.radio(
        "Tipo de consulta",
        ["Tengo un contrato", "Solo quiero asesoría"],
        help="Si tienes un contrato en PDF o texto, el sistema lo analiza primero.",
    )

with col_tipo:
    tipo_activo = st.radio(
        "Tipo de activo",
        ["vivienda", "vehiculo"],
        format_func=lambda x: "Vivienda" if x == "vivienda" else "Vehículo",
    )

st.divider()

ingreso_raw = st.number_input(
    "Ingreso mensual bruto (COP)",
    min_value=0,
    step=500_000,
    value=0,
    help="Déjalo en 0 si prefieres que el asesor sugiera rangos de ingreso recomendados.",
)

if ingreso_raw > 0:
    ingreso_formateado = f"${ingreso_raw:,.0f}".replace(",", ".")
    st.markdown(
        f'<p class="etiqueta-peso">{ingreso_formateado} COP</p>',
        unsafe_allow_html=True,
    )
    cuota_max = ingreso_raw * 0.30
    cuota_formateada = f"${cuota_max:,.0f}".replace(",", ".")
    st.caption(f"Cuota máxima recomendada (regla del 30%): {cuota_formateada} COP/mes")

texto_documento = None

if modo == "Tengo un contrato":
    st.divider()
    opcion = st.radio(
        "Cómo quieres ingresar el contrato",
        ["Subir PDF", "Pegar texto"],
    )

    if opcion == "Subir PDF":
        archivo = st.file_uploader(
            "Sube el contrato en PDF",
            type=["pdf"],
            help="Asegúrate de que el PDF tenga texto seleccionable, no sea escaneado.",
        )
        if archivo:
            with pdfplumber.open(io.BytesIO(archivo.read())) as pdf:
                texto_documento = "\n".join(
                    pagina.extract_text() or ""
                    for pagina in pdf.pages
                ).strip()
            if not texto_documento:
                st.warning(
                    "El PDF no contiene texto extraíble. "
                    "Si es un documento escaneado, usa la opción de pegar texto."
                )
                texto_documento = None
            else:
                st.success(f"PDF cargado correctamente — {len(texto_documento):,} caracteres leídos.")
    else:
        texto_documento = st.text_area(
            "Pega el texto del contrato aquí",
            height=200,
            placeholder="Copia y pega el contenido del contrato o las condiciones financieras...",
        )
        if texto_documento:
            texto_documento = texto_documento.strip() or None

st.divider()

analizar = st.button("Analizar", type="primary", use_container_width=True)

if analizar:
    if modo == "Tengo un contrato" and not texto_documento:
        st.error("Por favor ingresa el contrato antes de continuar.")
        st.stop()

    with st.spinner("Consultando tasas y preparando tu análisis..."):
        llm = crear_llm()
        grafo = crear_grafo(llm)

        estado_inicial = {
            "texto_documento": texto_documento,
            "tipo_activo": tipo_activo,
            "ingreso_mensual": float(ingreso_raw),
            "datos_contrato": None,
            "analisis": None,
            "reporte_final": None,
        }

        resultado = grafo.invoke(estado_inicial)

    if resultado.get("datos_contrato"):
        with st.expander("Condiciones extraídas del contrato", expanded=False):
            st.markdown(resultado["datos_contrato"])

    st.subheader("Análisis y recomendación")
    st.markdown(resultado.get("analisis", "No se generó análisis."))

    if resultado.get("reporte_final"):
        st.divider()
        st.subheader("Reporte completo")
        st.markdown(resultado["reporte_final"])
        st.download_button(
            label="Descargar reporte en Markdown",
            data=resultado["reporte_final"],
            file_name="reporte_financiero.md",
            mime="text/markdown",
            use_container_width=True,
        )
