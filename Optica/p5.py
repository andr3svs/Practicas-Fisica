import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
from uncertainties import unumpy as unp


def formatear_incertidumbre(medida, cifras=2):
    valor = ufloat(float(unp.nominal_values(medida)), float(unp.std_devs(medida)))
    return format(valor, f".{cifras}uS")


def formatear_array(medidas, cifras=2):
    return [formatear_incertidumbre(medida, cifras) for medida in medidas]


# PARAMETROS
fp = 0.15 * 10**9
fp3 = 0.20 * 10**9  # en la 3 se requiere una lente con mayor distancia focal
# Datos parte 1
# esto es la medidas de la distancia 1:
# Incertidumbre: Como es el valor abosluto de una resta, he tomado la incertidumbre de las dos medidas
medidas_d1 = np.array([-3000000, -3100000, -3200000])
medidas_d2 = np.array([-300000, -200000, -200000])

medidas_d1_p1_tipo_a = np.sqrt(
    1000**2 + 1000**2
)  # incertidunbre de ambos valores de la resta
medidas_d1_p1_tipo_b = np.std(medidas_d1, ddof=1) / np.sqrt(len(medidas_d1))
medidas_d1_p1_incertidumbre_total = np.sqrt(
    medidas_d1_p1_tipo_a**2 + medidas_d1_p1_tipo_b**2
)
medidas_d1_p1_con_incertidumbre = unp.uarray(
    medidas_d1, medidas_d1_p1_incertidumbre_total
)

medidas_d2_p1_tipo_a = 1000
medidas_d2_p1_tipo_b = np.std(medidas_d2, ddof=1) / np.sqrt(len(medidas_d2))
medidas_d2_p1_incertidumbre_total = np.sqrt(
    medidas_d2_p1_tipo_a**2 + medidas_d2_p1_tipo_b**2
)
medidas_d2_p1_con_incertidumbre = unp.uarray(
    medidas_d2, medidas_d2_p1_incertidumbre_total
)

print("Medidas de las lineas con incertidumbre:")
print(formatear_array(medidas_d1_p1_con_incertidumbre))
print(formatear_array(medidas_d2_p1_con_incertidumbre))

# S
medidas_s_p1 = np.array([1500000, 2100000, 2000000])
medidas_s_p1_tipo_a = 1000  # aqui estoy asumiendo que las hicimos con el error de 10um
medidas_s_p1_tipo_b = np.std(medidas_s_p1, ddof=1) / np.sqrt(len(medidas_s_p1))
medidas_s_p1_incertidumbre_total = np.sqrt(
    medidas_s_p1_tipo_a**2 + medidas_s_p1_tipo_b**2
)
medidas_s_p1_con_incertidumbre = unp.uarray(
    medidas_s_p1, medidas_s_p1_incertidumbre_total
)
print("Medidas de la distancia s con incertidumbre:")
print(formatear_array(medidas_s_p1_con_incertidumbre))
# Calculo d
d = unp.sqrt(medidas_d1_p1_con_incertidumbre * medidas_d2_p1_con_incertidumbre)

# Calculo de D: introduce aqui la distancia focal f' en las mismas unidades
# que d y d'_1.
f_prima = fp
D = f_prima * (
    2
    - (d**2 + medidas_d1_p1_con_incertidumbre**2)
    / (d * medidas_d1_p1_con_incertidumbre)
)

print("D:")
print(formatear_array(D))

# Calculo de la longitud de onda:
# s = 3 * lambda * D / d  ->  lambda = s * d / (3 * D)
longitud_onda = medidas_s_p1_con_incertidumbre * d / (3 * D)


def promedio_con_incertidumbre(medidas):
    valores = unp.nominal_values(medidas)
    incertidumbres = unp.std_devs(medidas)
    incertidumbre_repeticion = np.std(valores, ddof=1) / np.sqrt(len(valores))
    incertidumbre_propagada = np.sqrt(np.sum(incertidumbres**2)) / len(valores)
    incertidumbre_total = np.sqrt(
        incertidumbre_repeticion**2 + incertidumbre_propagada**2
    )
    return unp.uarray(np.mean(valores), incertidumbre_total)


longitud_onda_average = promedio_con_incertidumbre(longitud_onda)

print("Longitud de onda lambda:")
print(formatear_array(longitud_onda))

print("Promedio de la longitud de onda:")
print(formatear_incertidumbre(longitud_onda_average))

# parte 2
medidas_s_p2 = np.array([600000, 700000, 650000])
medidas_d1_p2 = np.array([-3000000, -3000000, -3000000])
medidas_d2_p2 = np.array([-300000, -300000, -300000])

medidas_d1_p2_tipo_a = np.sqrt(1000**2 + 1000**2)
medidas_d1_p2_tipo_b = np.std(medidas_d1_p2, ddof=1) / np.sqrt(len(medidas_d1_p2))
medidas_d1_p2_incertidumbre_total = np.sqrt(
    medidas_d1_p2_tipo_a**2 + medidas_d1_p2_tipo_b**2
)
medidas_d1_p2_con_incertidumbre = unp.uarray(
    medidas_d1_p2, medidas_d1_p2_incertidumbre_total
)

medidas_d2_p2_tipo_a = 1000
medidas_d2_p2_tipo_b = np.std(medidas_d2_p2, ddof=1) / np.sqrt(len(medidas_d2_p2))
medidas_d2_p2_incertidumbre_total = np.sqrt(
    medidas_d2_p2_tipo_a**2 + medidas_d2_p2_tipo_b**2
)
medidas_d2_p2_con_incertidumbre = unp.uarray(
    medidas_d2_p2, medidas_d2_p2_incertidumbre_total
)

medidas_s_p2_tipo_a = 1000
medidas_s_p2_tipo_b = np.std(medidas_s_p2, ddof=1) / np.sqrt(len(medidas_s_p2))
medidas_s_p2_incertidumbre_total = np.sqrt(
    medidas_s_p2_tipo_a**2 + medidas_s_p2_tipo_b**2
)
medidas_s_p2_con_incertidumbre = unp.uarray(
    medidas_s_p2, medidas_s_p2_incertidumbre_total
)

d_p2 = unp.sqrt(medidas_d1_p2_con_incertidumbre * medidas_d2_p2_con_incertidumbre)
D_p2 = f_prima * (
    2
    - (d_p2**2 + medidas_d1_p2_con_incertidumbre**2)
    / (d_p2 * medidas_d1_p2_con_incertidumbre)
)
# En la parte 2, s corresponde a una interfranja.
longitud_onda_p2 = medidas_s_p2_con_incertidumbre * d_p2 / D_p2
longitud_onda_p2_average = promedio_con_incertidumbre(longitud_onda_p2)
print("Longitud de onda lambda de la parte 2:")
print(formatear_array(longitud_onda_p2))
print("Promedio de la longitud de onda de la parte 2:")
print(formatear_incertidumbre(longitud_onda_p2_average))

# parte 3
medidas_s_p3 = np.array([520000, 650000, 770000])
medidas_d1_p3 = np.array([-1270000, -960000, -1140000])
medidas_d2_p3 = np.array([-500000, -440000, -300000])
fp3 = 0.20 * 10**9
incertidumbre_tipo_a_todas = 100000  # en esta parte nos equivocamos y tomamos el error de 100um que es el de la mirilla del ocular

medidas_s_p3_tipo_b = np.std(medidas_s_p3, ddof=1) / np.sqrt(len(medidas_s_p3))
medidas_s_p3_incertidumbre_total = np.sqrt(
    incertidumbre_tipo_a_todas**2 + medidas_s_p3_tipo_b**2
)
medidas_s_p3_con_incertidumbre = unp.uarray(
    medidas_s_p3, medidas_s_p3_incertidumbre_total
)

medidas_d1_p3_tipo_b = np.std(medidas_d1_p3, ddof=1) / np.sqrt(len(medidas_d1_p3))
medidas_d1_p3_incertidumbre_total = np.sqrt(
    incertidumbre_tipo_a_todas**2 + medidas_d1_p3_tipo_b**2
)
medidas_d1_p3_con_incertidumbre = unp.uarray(
    medidas_d1_p3, medidas_d1_p3_incertidumbre_total
)

medidas_d2_p3_tipo_b = np.std(medidas_d2_p3, ddof=1) / np.sqrt(len(medidas_d2_p3))
medidas_d2_p3_incertidumbre_total = np.sqrt(
    incertidumbre_tipo_a_todas**2 + medidas_d2_p3_tipo_b**2
)
medidas_d2_p3_con_incertidumbre = unp.uarray(
    medidas_d2_p3, medidas_d2_p3_incertidumbre_total
)

d_p3 = unp.sqrt(medidas_d1_p3_con_incertidumbre * medidas_d2_p3_con_incertidumbre)
D_p3 = fp3 * (
    2
    - (d_p3**2 + medidas_d1_p3_con_incertidumbre**2)
    / (d_p3 * medidas_d1_p3_con_incertidumbre)
)
print("D de la parte 3:")
print(formatear_array(D_p3))
# En la parte 3, s corresponde a una interfranja.
longitud_onda_p3 = medidas_s_p3_con_incertidumbre * d_p3 / D_p3
longitud_onda_p3_average = promedio_con_incertidumbre(longitud_onda_p3)
print("Promedio de la longitud de onda de la parte 3:")
print(formatear_array(longitud_onda_p3))
print(formatear_incertidumbre(longitud_onda_p3_average))

# grafica
# creo un array con todos los promedios y su incertidumbre
lambda_averages = [
    longitud_onda_average,
    longitud_onda_p2_average,
    longitud_onda_p3_average,
]
lambda_plot = unp.uarray(
    [float(unp.nominal_values(value)) for value in lambda_averages],
    [float(unp.std_devs(value)) for value in lambda_averages],
)
plt.errorbar(
    ["Parte 1", "Parte 2", "Parte 3"],
    unp.nominal_values(lambda_plot),
    yerr=unp.std_devs(lambda_plot),
    fmt="o",
    capsize=5,
)
plt.axhline(589, color="tab:red", linestyle="--", label=r"$\lambda$ Na teórica = 589")
plt.ylabel("Longitud de onda")
plt.title("Longitud de onda por parte")
plt.legend()
plt.tight_layout()
plt.show()
