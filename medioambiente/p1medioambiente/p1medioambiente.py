"""Plantilla de análisis experimental

Este archivo contiene funciones genéricas y una estructura mínima para
analizar experimentos similares a los de la práctica. Reemplaza los
valores de ejemplo y las rutas por los datos concretos de tu experimento.

- Mantén las funciones reutilizables (cálculo, ajuste, generación de incertidumbres).
- Rellena los arrays `v_0_all`, `theta_all` y `b_all` con tus datos.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from uncertainties import ufloat
from uncertainties import unumpy
from scipy.optimize import curve_fit
import math


# ------------------ Helpers ------------------
def get_base_dir():
    """Devuelve la carpeta donde está este script."""
    return os.path.dirname(os.path.abspath(__file__))


def ruta(nombre_archivo):
    """Construye una ruta absoluta relativa a este script."""
    return os.path.join(get_base_dir(), nombre_archivo)


def separate_uncertainties(uarray: unumpy.uarray):
    """Separa una `uarray` en valores nominales y desviaciones estándar."""
    nominal = unumpy.nominal_values(uarray)
    error = unumpy.std_devs(uarray)
    return nominal, error


def generate_uncertainties_for_chi2_1(data=None, fit=None, num_params=None,
                                     x_data=None, y_data=None, x_fit=None, y_fit=None):
    """Genera incertidumbres que dan chi^2_red ~ 1.

    Provee dos modos: eje único (data, fit, num_params) o par (x,y).
    Devuelve un array de incertidumbres compatibles con los datos.
    """
    if data is not None and fit is not None and num_params is not None:
        residuals = data - fit
        dof = len(data) - num_params
        sigma = np.sqrt(np.sum(residuals**2) / dof)
        return np.full_like(data, sigma, dtype=float)

    if all(v is not None for v in (x_data, y_data, x_fit, y_fit, num_params)):
        x_res = x_data - x_fit
        y_res = y_data - y_fit
        combined = np.sqrt(x_res**2 + y_res**2)
        dof = len(x_data) - num_params
        sigma = np.sqrt(np.sum(combined**2) / dof)
        return np.full_like(x_data, sigma, dtype=float), np.full_like(y_data, sigma, dtype=float)

    raise ValueError("Proporciona (data, fit, num_params) o (x_data, y_data, x_fit, y_fit, num_params)")
"""
# ------------------ Parámetros ------------------"""
### Medidas directas
temperatura_cuerpo=ufloat(304.3722222, 0.1) # K
temperatura_suelo=ufloat(294.55, 0.1) # K
area_pie=ufloat(0.0169730236, 0.001) # m^2
espesor_suela=ufloat(0.024, 0.01) # m
temperatura_ropa=ufloat(298.05, 0.1) # K
radio_interior=ufloat(0.2, 0.01) # m
espesor_ropa=ufloat(0.0035, 0.01) # m
altura_sin_cabeza=ufloat(1.5, 0.01) # m
temperatura_ambiente=ufloat(296.25, 0.1) # K
altura_con_cabeza=ufloat(1.725, 0.01) # m
peso=ufloat(77, 1) # kg
diametro_cabeza=ufloat(0.225, 0.01) # m
humedad_relativa=44 # fracción
### Medidas Tabuladas
conductividad_zapatos=0.29 # W/mK
conductividad_ropa=0.05 # W/mK
anchura_omega=2*np.pi*radio_interior
# coeficiente de convección de cabeza (E18 en la hoja) — calculado desde la diferencia de temperaturas
# Se usa la expresión de la hoja: h_cabeza = 0.51*(T_cuerpo - T_ambiente)^(1/4)
h_cabeza = None
indice_metabolico=70
# Calcular presión parcial de vapor desde la humedad relativa (E27 en la hoja)
# E27 = B25/100 * 6.107 * EXP(17.08*(B12-273.15)/(B12-273.15+234.2))
e_s = 6.107 * unumpy.exp(17.08*(temperatura_ambiente-273.15)/(temperatura_ambiente-273.15+234.2))
presion_parcial_vapor_agua = humedad_relativa/100 * e_s
### Medidas Indirectas
radio_exterior=radio_interior + espesor_ropa
flujo_calor_pies=(temperatura_cuerpo - temperatura_suelo) * conductividad_zapatos*area_pie / espesor_suela
flujo_calor_cuerpo = np.pi * ((temperatura_cuerpo - temperatura_ropa) * conductividad_ropa * 2 * altura_sin_cabeza) / unumpy.log((radio_exterior*1.0 / radio_interior))

# Longitud de transición (expresión corregida — ajustar según la fórmula física correcta)
# Se evalúa la raíz cúbica del cociente (N/D) tal como en la hoja Excel
x_transicion = ((1e9 * (14e-6)**2) / (9.8 * (temperatura_ropa - temperatura_ambiente) * 2 / (temperatura_ropa + temperatura_ambiente)))**(1/3)
h_laminar=1.07*((temperatura_ropa - temperatura_ambiente)/x_transicion)**(1/4)
h_turbulento=1.13* (temperatura_ropa - temperatura_ambiente)**(1/3)
superficie_cuerpo=0.202*peso**(0.425)*altura_con_cabeza**(0.725)
# Convección: usar E12 = 2*pi*radio_interior (anchura_omega) y B13 = altura_con_cabeza
flujo_conveccion = h_laminar*(temperatura_ropa-temperatura_ambiente)*anchura_omega*x_transicion \
    + h_turbulento*(temperatura_ropa-temperatura_ambiente)*anchura_omega*(altura_con_cabeza - x_transicion)

# Convección de la cabeza (E18 = 0.51*(B2-B12)^(1/4))
# Calculamos el coeficiente h_cabeza desde la hoja y usamos el área de la cabeza: 4*pi*r^2 = pi*d^2
h_cabeza = 0.51*(temperatura_cuerpo - temperatura_ambiente)**(1/4)
area_cabeza = 4*np.pi*(diametro_cabeza/2)**2
flujo_cabeza_conveccion = h_cabeza*(temperatura_cuerpo - temperatura_ambiente)*area_cabeza

# Radiación: usar temperatura de la ropa (B7) según la hoja
flujo_radiacion = 0.85*0.7*5.67e-8*(temperatura_ropa**4 - temperatura_ambiente**4)*superficie_cuerpo
flujo_perdido_neto=flujo_calor_pies + flujo_calor_cuerpo + flujo_conveccion + flujo_cabeza_conveccion + flujo_radiacion
intercambio_calor_evaporacion = 3.05e-3*(5733 - 6.99*indice_metabolico - presion_parcial_vapor_agua + 0.42*(indice_metabolico - 58.15))*superficie_cuerpo
intercambio_conveccion_respiracion = 0.0014*indice_metabolico*(34 - temperatura_ambiente + 273.15)*superficie_cuerpo
intercambio_evaporacion_respiracion = 1.72e-5*indice_metabolico*(5867 - presion_parcial_vapor_agua)*superficie_cuerpo


"""
Visualizacion de resultados
"""
print(f"Flujo de calor perdido por los pies: {flujo_calor_pies:.2f} W")
print(f"Flujo de calor perdido por el cuerpo: {flujo_calor_cuerpo:.2f} W")
print(f"Flujo de calor perdido por convección: {flujo_conveccion:.2f} W")
print(f"Flujo de calor perdido por convección en la cabeza: {flujo_cabeza_conveccion:.2f} W")
print(f"Flujo de calor perdido por radiación: {flujo_radiacion:.2f} W")     


# Totales: (A) suma de los componentes de superficie (pies, cuerpo, convección, cabeza, radiación)
print(f"Flujo perdido neto (superficies): {flujo_perdido_neto:.2f} W")
print(f"Flujo perdido neto (superficies) calorias: {flujo_perdido_neto*20.67:.2f} kcal/dia")

# (B) total incluyendo intercambios por evaporación y respiración
flujo_total = flujo_perdido_neto + intercambio_calor_evaporacion + intercambio_conveccion_respiracion + intercambio_evaporacion_respiracion
print(f"Flujo total (incluye intercambios): {flujo_total:.2f} W")
# Mostrar también los términos de intercambio para referencia
print(f"  - Intercambio evaporación (term): {intercambio_calor_evaporacion:.2f} W")
print(f"  - Intercambio convección respiración: {intercambio_conveccion_respiracion:.2f} W")
print(f"  - Intercambio evaporación respiración: {intercambio_evaporacion_respiracion:.2f} W")

# ----- Gráfica de componentes (no usar datos de Excel) -----
# Agrupamos la contribución de la cabeza dentro de la convección
labels = ['Pies', 'Cuerpo', 'Convección', 'Radiación']
components = [flujo_calor_pies, flujo_calor_cuerpo, flujo_conveccion + flujo_cabeza_conveccion, flujo_radiacion]

# Extraer valores nominales y errores y convertir a kcal/día
KCAL_PER_W = 20.67
nominales = unumpy.nominal_values(components) * KCAL_PER_W
errores = unumpy.std_devs(components) * KCAL_PER_W

fig, ax = plt.subplots(figsize=(10,6))
pos = np.arange(len(labels))
bars = ax.bar(pos, nominales, color=['#4c72b0','#55a868','#c44e52','#ccb974'])
ax.set_xticks(pos)
ax.set_xticklabels(labels)
ax.set_ylabel('Flujo (kcal/día)')
ax.set_title('Contribución de componentes al flujo de calor')
ax.grid(axis='y', alpha=0.3)
for i, b in enumerate(bars):
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h + max(nominales)*0.02, f"{nominales[i]:.1f}", ha='center', va='bottom', fontsize=9)

# Ajustar escala vertical para mejor visualización
ymax = max(nominales) if len(nominales)>0 else 1
ax.set_ylim(0, float(ymax) * 1.3)

outpath = ruta('flows_components.png')
plt.tight_layout()
plt.savefig(outpath, dpi=200)
print(f"Gráfica guardada en: {outpath}")
try:
    plt.show()
except Exception:
    pass


# ----- Generar tabla LaTeX con formato de incertidumbres (GUM) -----
def gum_format(value, std, sig=2):
    """Formatea value±std siguiendo regla GUM: std con `sig` cifras significativas,
    y el valor nominal con el mismo número de decimales que la incertidumbre.
    Devuelve cadena tipo '12.34 \\pm 0.56'.
    Si std==0, muestra dos decimales por defecto.
    """
    try:
        std = float(std)
        val = float(value)
    except Exception:
        return f"{value} \\pm {std}"
    if std <= 0:
        # mostrar con 2 decimales
        return f"{val:.2f} \\pm {0:.2f}"
    exponent = math.floor(math.log10(abs(std)))
    ndigits = -exponent + (sig - 1)
    # redondear incertidumbre
    u_rounded = round(std, ndigits)
    decimals = max(0, ndigits)
    # si u_rounded es 0 por redondeo, incrementar decimales
    if u_rounded == 0:
        decimals = sig
        u_rounded = round(std, decimals)
    val_rounded = round(val, decimals)
    fmt = f"{{:.{decimals}f}}"
    return f"{fmt.format(val_rounded)} \\pm {fmt.format(u_rounded)}"


items = [
    ("T cuerpo (K)", temperatura_cuerpo),
    ("T ropa (K)", temperatura_ropa),
    ("T ambiente (K)", temperatura_ambiente),
    ("T suelo (K)", temperatura_suelo),
    ("Área pie (m^2)", area_pie),
    ("Espesor suela (m)", espesor_suela),
    ("Radio interior (m)", radio_interior),
    ("Espesor ropa (m)", espesor_ropa),
    ("Altura (sin cabeza) (m)", altura_sin_cabeza),
    ("Altura (con cabeza) (m)", altura_con_cabeza),
    ("Peso (kg)", peso),
    ("Diámetro cabeza (m)", diametro_cabeza),
    ("Flujo pies (W)", flujo_calor_pies),
    ("Flujo cuerpo (W)", flujo_calor_cuerpo),
    ("Flujo convección (W)", flujo_conveccion + flujo_cabeza_conveccion),
    ("Flujo radiación (W)", flujo_radiacion),
    ("Flujo perdido neto (W)", flujo_perdido_neto),
    ("Intercambio evap. (W)", intercambio_calor_evaporacion),
    ("Intercambio conv. resp. (W)", intercambio_conveccion_respiracion),
    ("Intercambio evap. resp. (W)", intercambio_evaporacion_respiracion),
    ("Flujo total (W)", flujo_total),
]

latex_lines = []
latex_lines.append('\\begin{tabular}{l c}')
latex_lines.append('\\hline')
latex_lines.append('Magnitud & Valor\\\\')
latex_lines.append('\\hline')
for name, val in items:
    # obtener nominal y std
    if hasattr(val, 'std_dev'):
        nom = float(unumpy.nominal_values(val))
        stdv = float(unumpy.std_devs(val))
    else:
        try:
            nom = float(val)
            stdv = 0.0
        except Exception:
            nom = val
            stdv = 0.0
    formatted = gum_format(nom, stdv, sig=2)
    latex_lines.append(f"{name} & $ {formatted} $\\\\")

latex_lines.append('\\hline')
latex_lines.append('\\end{tabular}')

out_tex = ruta('table_uncertainties.tex')
with open(out_tex, 'w', encoding='utf-8') as f:
    f.write('\\n'.join(latex_lines))

print(f"Tabla LaTeX de incertidumbres guardada en: {out_tex}")

# ----- Gráfica: flujos en función del índice metabólico -----
def compute_flows_for_met(met):
    """Devuelve (flujo_superficies, flujo_total) como ufloat para un índice metabólico dado."""
    intercambio_calor_evaporacion_m = 3.05e-3*(5733 - 6.99*met - presion_parcial_vapor_agua + 0.42*(met - 58.15))*superficie_cuerpo
    intercambio_conveccion_respiracion_m = 0.0014*met*(34 - temperatura_ambiente + 273.15)*superficie_cuerpo
    intercambio_evaporacion_respiracion_m = 1.72e-5*met*(5867 - presion_parcial_vapor_agua)*superficie_cuerpo
    flujo_perdido_neto_m = flujo_calor_pies + flujo_calor_cuerpo + flujo_conveccion + flujo_cabeza_conveccion + flujo_radiacion
    flujo_total_m = flujo_perdido_neto_m + intercambio_calor_evaporacion_m + intercambio_conveccion_respiracion_m + intercambio_evaporacion_respiracion_m
    return flujo_perdido_neto_m, flujo_total_m

met_values = [70, 40, 235, 115]
met_labels = ['70 (de pie)', '40 (dormir)', '235 (trabajo pesado)', '115 (limpieza)']

# Calcular flujos usando compute_flows_for_met
total_vals_w = []
for m in met_values:
    f_super, f_total = compute_flows_for_met(m)
    total_vals_w.append(unumpy.nominal_values(f_total))

# Convertir a kcal/día
total_vals = [v * KCAL_PER_W for v in total_vals_w]

# Imprimir valores del segundo gráfico
print("\n----- Flujos en función del índice metabólico (kcal/día) -----")
for label, total_val in zip(met_labels, total_vals):
    print(f"{label}: {total_val} kcal/día")

fig, ax = plt.subplots(figsize=(10,6))
ind = np.arange(len(met_values))
width = 0.5

# Crear barras solo para el flujo total
bars = ax.bar(ind, total_vals, width, color='#c44e52')

# Agregar valores encima de las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height}',
            ha='center', va='bottom', fontsize=10)

ax.set_xticks(ind)
ax.set_xticklabels(met_labels)
ax.set_ylabel('Flujo (kcal/día)')
ax.set_title('Flujo total según índice metabólico')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
# Ajustar escala vertical para la gráfica metabólica
ymax_m = max(total_vals) if len(total_vals)>0 else 1
ax.set_ylim(0, float(ymax_m) * 1.3)
out2 = ruta('flows_vs_metabolism.png')
plt.savefig(out2, dpi=200)
print(f"Gráfica metabolismo guardada en: {out2}")
try:
    plt.show()
except Exception:
    pass
