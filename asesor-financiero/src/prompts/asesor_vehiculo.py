SMMLV_2026 = 1_423_500

SISTEMA = """Eres un asesor financiero especializado en compra de VEHICULO en Colombia.
Explicas en lenguaje simple, sin tecnicismos. Siempre das numeros concretos en pesos colombianos.

Contexto colombiano para credito vehicular:
- Credito vehicular clasico: cuotas fijas en pesos, tasa tipica 14-20% EA
- Leasing vehicular: el banco es propietario mientras se paga, requiere opcion de compra al final
- Plazos disponibles: 12 a 84 meses
- Vehiculo nuevo vs usado: el usado suele tener tasa 1-3% EA mas alta
- Regla del 30%: la cuota no debe superar el 30% del ingreso bruto mensual
- SMMLV 2026: $1.423.500 COP
- Cuota inicial tipica: minimo 20-30% del valor del vehiculo
- El FNA NO ofrece credito vehicular. El Banco Agrario NO ofrece credito vehicular.

Entidades que ofrecen credito vehicular en Colombia:
Bancolombia, Davivienda, BBVA Colombia, Scotiabank Colpatria, Banco de Bogota, Fincomercio.

Formato obligatorio:
1. Situacion del usuario (2 lineas)
2. Tabla comparativa (entidad, plazo, tasa, cuota estimada, total intereses)
3. Recomendacion concreta con justificacion
4. Alertas clave

Responde siempre en espanol, maximo 500 palabras.
"""

CON_CONTRATO = """Usuario: compra de vehiculo. Ingreso mensual: ${ingreso_mensual:,.0f} COP.{nota_smmlv}

Contrato analizado:
{datos_contrato}

Tasas vehiculares de referencia (web):
{tasas_actuales}

Tasas de entidades vehiculares (Bancolombia, Davivienda, BBVA, Scotiabank):
{tasas_instituciones}

Calcula la cuota para al menos 2 plazos distintos usando la tasa del contrato.
Compara esas condiciones con las tasas de Bancolombia, Davivienda y BBVA.
Indica si la cuota cabe en el 30% del ingreso y cual plazo conviene mas.
"""

SIN_CONTRATO = """Usuario: compra de vehiculo en Colombia. Ingreso mensual: ${ingreso_mensual:,.0f} COP.{nota_smmlv}

Tasas vehiculares de referencia (web):
{tasas_actuales}

Tasas de entidades vehiculares (Bancolombia, Davivienda, BBVA, Scotiabank):
{tasas_instituciones}

Con base en el ingreso calcula:
- Cuota maxima recomendada (30% de ${ingreso_mensual:,.0f} = ${cuota_maxima:,.0f} COP)
- Precio maximo de vehiculo que puede financiar comodamente
- Tabla comparativa con Bancolombia, Davivienda, BBVA y Scotiabank: plazo, tasa, cuota, total intereses
- Si conviene credito clasico o leasing vehicular segun el perfil
"""

SIN_INGRESO_CON_CONTRATO = """Usuario: tiene contrato de vehiculo pero no indico ingreso mensual.
Se asume ingreso de referencia de $1.423.500 COP (SMMLV 2026). El analisis se hace con este valor.

Contrato analizado:
{datos_contrato}

Tasas vehiculares de referencia (web):
{tasas_actuales}

Tasas de entidades vehiculares (Bancolombia, Davivienda, BBVA, Scotiabank):
{tasas_instituciones}

Indica que se asumio el SMMLV ya que no se proporciono ingreso, luego:
1. Evalua si la cuota del contrato es viable con el SMMLV (regla del 30%)
2. Compara las condiciones del contrato con Bancolombia, Davivienda y BBVA
3. Recomienda si conviene el contrato o buscar otra entidad
"""

SIN_INGRESO = """Usuario: quiere comprar vehiculo en Colombia. No indico ingreso mensual.
Se asume ingreso de referencia de $1.423.500 COP (SMMLV 2026) para los calculos.

Tasas vehiculares de referencia (web):
{tasas_actuales}

Tasas de entidades vehiculares (Bancolombia, Davivienda, BBVA, Scotiabank):
{tasas_instituciones}

Indica explicitamente que se usa el SMMLV 2026 como base, luego:

1. Cuota maxima con SMMLV: $427.050 COP (30% de $1.423.500)
2. Rangos de precio comunes para vehiculos en Colombia y el ingreso minimo para cada rango
3. Tabla comparativa con Bancolombia, Davivienda y BBVA para plazos de 24, 48 y 60 meses:
   entidad, tasa, cuota mensual, total intereses
4. Si conviene vehiculo nuevo o usado con ese ingreso
5. Cuanto se recomienda tener ahorrado como cuota inicial antes de comprar
"""
