import numpy as np
from uncertainties import unumpy as unp

# DATOS PARTE 1
# Medidas del microscopio
medidas_copio = np.array([abs(90 - 95), abs(27 - 172)])  # divisiones
medidas_copio = medidas_copio * 1  # um
# no hay tipo a porque solo hemos tomado una medida de cada una de las lineas, por lo que no hay desviacion estandar
medidas_copio_incertidumbre_tipo_a = 0  # mm
medidas_copio_incertidumbre_tipo_b = 0.001  # mm dado por el fabricante
medidas_copio_incertidumbre_total = np.sqrt(
    medidas_copio_incertidumbre_tipo_a**2 + medidas_copio_incertidumbre_tipo_b**2
)

# creacion del dato con incertidumbre usando uncertainties
medidas_copio_con_incertidumbre = unp.uarray(
    medidas_copio, medidas_copio_incertidumbre_total
)

print("Medidas del microscopio con incertidumbre:")
print(medidas_copio_con_incertidumbre)
# Medidas de lineas
medidas_micrometro = np.array([31.5, 20])  # mm
medidas_micrometro_incertidumbre_tipo_a = 0  # mm
medidas_micrometro_incertidumbre_tipo_b = (
    0.0005  # mm creo que esto era la incertidumbre del tornillo micrometrico media div,
)
# pero ni idea TODO fuente de error

medidas_micrometro_incertidumbre_total = np.sqrt(
    medidas_micrometro_incertidumbre_tipo_a**2
    + medidas_micrometro_incertidumbre_tipo_b**2
)
medidas_micrometro_con_incertidumbre = unp.uarray(
    medidas_micrometro, medidas_micrometro_incertidumbre_total
)

# Calculo del aumento del microscopio
aumento_microscopio = (
    medidas_copio_con_incertidumbre / medidas_micrometro_con_incertidumbre
)
print("Aumento del microscopio:")
print(aumento_microscopio)
