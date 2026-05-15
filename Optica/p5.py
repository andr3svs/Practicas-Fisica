from pathlib import Path

import numpy as np
from uncertainties import unumpy as unp


# gptada padre todo esto
def formato_incertidumbre(valor):
    """Devuelve un valor de uncertainties en el formato nominal(incertidumbre)."""
    nominal = unp.nominal_values(valor)
    incertidumbre = unp.std_devs(valor)
    return f"{nominal:.4g}({incertidumbre:.2g})"


def generar_documento_latex():
    """Escribe un informe LaTeX con las medidas y los aumentos calculados."""
    salida = Path(__file__).with_name("p5_resultados.tex")
    medidas_copio_tex = "\\\\\n".join(
        f"Microscopio {indice + 1} & {formato_incertidumbre(valor)} & mm"
        for indice, valor in enumerate(medidas_copio_con_incertidumbre)
    )
    medidas_micrometro_tex = "\\\\\n".join(
        f"Micr\\'ometro {indice + 1} & {formato_incertidumbre(valor)} & mm"
        for indice, valor in enumerate(medidas_micrometro_con_incertidumbre)
    )
    aumentos_tex = "\\\\\n".join(
        f"Aumento {indice + 1} & {formato_incertidumbre(valor)} & --"
        for indice, valor in enumerate(aumento_microscopio)
    )

    documento = rf"""\documentclass{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{booktabs}}
\usepackage{{siunitx}}

\\title{{Pr\'actica de \'optica: medidas del microscopio}}
\date{{}}

\begin{{document}}
\maketitle

Las incertidumbres indicadas corresponden a la combinaci\'on de las
incertidumbres de tipo A y B usadas en el script. Los resultados se
escriben como valor nominal(incertidumbre).

\begin{{table}}[ht]
\centering
\caption{{Medidas obtenidas}}
\begin{{tabular}}{{lcc}}
	oprule
Magnitud & Valor & Unidad \\\\
\midrule
{medidas_copio_tex} \\
{medidas_micrometro_tex} \\
\bottomrule
\end{{tabular}}
\end{{table}}

El aumento del microscopio se obtiene mediante
\[
M = \frac{{d_{{\mathrm{{microscopio}}}}}}{{d_{{\mathrm{{micr\'ometro}}}}}}.
\]

\begin{{table}}[ht]
\centering
\caption{{Aumento del microscopio}}
\begin{{tabular}}{{lcc}}
	oprule
Magnitud & Valor & Unidad \\\\
\midrule
{aumentos_tex} \\
\bottomrule
\end{{tabular}}
\end{{table}}

\end{{document}}
"""
    salida.write_text(documento, encoding="utf-8")
    return salida


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

documento_generado = generar_documento_latex()
print(f"Documento LaTeX generado: {documento_generado}")
