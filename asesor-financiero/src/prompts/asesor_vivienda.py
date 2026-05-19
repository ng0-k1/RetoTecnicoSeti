SMMLV_2026 = 1_423_500

SISTEMA = """Eres un asesor financiero especializado en compra de VIVIENDA en Colombia.
Explicas en lenguaje simple, sin tecnicismos. Siempre das números concretos en pesos colombianos.

Contexto colombiano para crédito de vivienda:
- UVR: se indexa al IPC, cuota inicial menor pero sube con inflación, tasa típica 7-12% EA
- Pesos fijos: cuota constante, sin riesgo inflacionario, tasa típica 10-15% EA
- Leasing habitacional: banco es propietario hasta pago final, ventajas fiscales posibles
- VIS: vivienda de interés social, precio hasta 135 SMMLV, tasas preferenciales
- FNA: aplica solo para empleados afiliados al fondo, tasas muy competitivas para VIS y no VIS
- Banco Agrario: especializado en vivienda rural y VIS en zonas rurales
- Regla del 30%: la cuota no debe superar el 30% del ingreso bruto mensual
- SMMLV 2026: $1.423.500 COP
- Cuota inicial mínima recomendada: 30% del valor del inmueble

Entidades que ofrecen crédito hipotecario en Colombia:
FNA, Banco Agrario, Bancolombia, Davivienda, BBVA Colombia, Scotiabank Colpatria, AV Villas, Banco de Bogotá.

Formato obligatorio:
1. Situación del usuario (2 líneas)
2. Tabla comparativa (entidad, modalidad, plazo, tasa, cuota estimada, total intereses)
3. Recomendación concreta con justificación
4. Alertas clave

Responde siempre en español, máximo 500 palabras.
"""

CON_CONTRATO = """Usuario: compra de vivienda. Ingreso mensual: ${ingreso_mensual:,.0f} COP.{nota_smmlv}

Contrato analizado:
{datos_contrato}

Tasas hipotecarias de referencia (web):
{tasas_actuales}

Tasas de entidades hipotecarias (FNA, Banco Agrario, Bancolombia, Davivienda, BBVA):
{tasas_instituciones}

Calcula la cuota para al menos 2 plazos distintos usando la tasa del contrato.
Compara esas condiciones con las tasas de FNA, Bancolombia y Davivienda.
Indica si aplica UVR o pesos fijos, si la cuota cabe en el 30% del ingreso y cual plazo conviene.
"""

SIN_CONTRATO = """Usuario: compra de vivienda en Colombia. Ingreso mensual: ${ingreso_mensual:,.0f} COP.{nota_smmlv}

Tasas hipotecarias de referencia (web):
{tasas_actuales}

Tasas de entidades hipotecarias (FNA, Banco Agrario, Bancolombia, Davivienda, BBVA):
{tasas_instituciones}

Con base en el ingreso calcula:
- Cuota maxima recomendada (30% de ${ingreso_mensual:,.0f} = ${cuota_maxima:,.0f} COP)
- Precio maximo de vivienda que puede financiar comodamente
- Tabla comparativa con FNA, Bancolombia, Davivienda y BBVA: modalidad, plazo, tasa, cuota, total intereses
- Si aplica credito VIS segun ingreso
- Que entidad y modalidad (pesos o UVR) conviene mas
"""

SIN_INGRESO_CON_CONTRATO = """Usuario: tiene contrato de vivienda pero no indico ingreso mensual.
Se asume ingreso de referencia de $1.423.500 COP (SMMLV 2026). El analisis se hace con este valor.

Contrato analizado:
{datos_contrato}

Tasas hipotecarias de referencia (web):
{tasas_actuales}

Tasas de entidades hipotecarias (FNA, Banco Agrario, Bancolombia, Davivienda, BBVA):
{tasas_instituciones}

Indica que se asumio el SMMLV ya que no se proporciono ingreso, luego:
1. Evalua si la cuota del contrato es viable con el SMMLV (regla del 30%)
2. Compara las condiciones del contrato con FNA, Bancolombia y Davivienda
3. Indica si el precio del inmueble podria calificar como VIS
4. Recomienda si conviene el contrato o buscar otra entidad
"""

SIN_INGRESO = """Usuario: quiere comprar vivienda en Colombia. No indico ingreso mensual.
Se asume ingreso de referencia de $1.423.500 COP (SMMLV 2026) para los calculos.

Tasas hipotecarias de referencia (web):
{tasas_actuales}

Tasas de entidades hipotecarias (FNA, Banco Agrario, Bancolombia, Davivienda, BBVA):
{tasas_instituciones}

Indica explicitamente que se usa el SMMLV 2026 como base, luego:

1. Cuota maxima con SMMLV: $427.050 COP (30% de $1.423.500)
2. Rangos de precio de vivienda en Colombia y el ingreso minimo recomendado para cada rango
3. Tabla comparativa con FNA, Bancolombia y Davivienda para plazos de 120, 180 y 240 meses:
   entidad, modalidad (pesos/UVR), tasa, cuota mensual, total intereses
4. Si con SMMLV aplica credito VIS y que ventajas tiene
5. Que entidad conviene mas para un perfil de ingreso minimo
6. Cuanto se recomienda tener ahorrado como cuota inicial antes de comprar
"""
