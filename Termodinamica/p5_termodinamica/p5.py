import pandas as pd
import uncertainties
import matplotlib.pyplot as plt
import matplotlib as mpl
from uncertainties import unumpy
import numpy as np
"""
Functions separate_uncertainties
In: unumpy.array
Returns the nominal and the error part as two separate numpy arrays arr
"""
def separate_uncertainties(uarray : unumpy.uarray):
    nominal=unumpy.nominal_values(uarray)
    error=unumpy.std_devs(uarray)
    return (nominal,error)
"""
INTRODUCING DATA
The data for the laboratory practice must be taken into an excel file, and this will read it.
"""
#Excel file location
excel_path_user="p5\datap05_bomba_calor2.xlsx"
data_raw=pd.read_excel(excel_path_user,sheet_name="Medidas")
t_f_ufloat = unumpy.uarray(data_raw["t_f"],data_raw["u_c (T)"])
t_c_ufloat= unumpy.uarray(data_raw["t_c"],data_raw["u_c (T)"])
potencia_ufloat=unumpy.uarray(data_raw["Potencia"],data_raw["u_c (P)"])
tiempo_ufloat=unumpy.uarray(data_raw["t"],0.001)
"""
Data manipulation
"""
cop_ideal=(t_c_ufloat+273.15)/(t_c_ufloat-t_f_ufloat)
q_c=t_c_ufloat.copy()
#Calculate the heat based on the temperatures of the c focus.
q_c=4184.0*(t_c_ufloat-t_c_ufloat[0])
W_J=potencia_ufloat*tiempo_ufloat
# 1. Creamos un array del tamaño correcto lleno de NaNs (Matplotlib ignora los NaNs al dibujar)
cop_exp = unumpy.uarray(np.full(len(q_c), np.nan), np.full(len(q_c), np.nan))

# 2. Realizamos la división SÓLO a partir del índice 1 (es decir, saltándonos t=0)
cop_exp[1:] = q_c[1:] / W_J[1:]

diference_temperatures_uf=abs(t_c_ufloat-t_f_ufloat)
#Get data into numpy usable form
t_f_nominal,t_f_error= separate_uncertainties(t_f_ufloat)
t_c_nominal,t_c_error= separate_uncertainties(t_c_ufloat)
tiempo_nominal, tiempo_error= separate_uncertainties(tiempo_ufloat)
d_t_nominal, d_t_error=separate_uncertainties(diference_temperatures_uf)
cop_exp_nominal, cop_exp_error=separate_uncertainties(cop_exp)
cop_ideal_nominal, cop_ideal_error=separate_uncertainties(cop_ideal)


"""
Exporting data to excel form

"""
# 1. Extraemos las matrices
cop_nom = unumpy.nominal_values(cop_exp)
cop_err = unumpy.std_devs(cop_exp)

wj_nom = unumpy.nominal_values(W_J)
wj_err = unumpy.std_devs(W_J)

# 2. Formateamos las columnas usando listas por comprensión
# El .3f indica que queremos 3 decimales. Ajustalo según necesites.
# Usamos \\pm porque en Python necesitamos doble barra para que escriba una sola en el txt.
col_cop = [f"${n:.9f} \\pm {e:.9f}$" for n, e in zip(cop_nom, cop_err)]

# 3. Creamos el DataFrame ya formateado
df_resultados = pd.DataFrame({
    'COP': col_cop,
})

# Al tener los símbolos de $ y \, Pandas lo exportará tal cual al documento.
estilo = df_resultados.style.hide(axis="index")

with open('tabla_con_errores.tex', 'w') as f:
    f.write(estilo.to_latex(hrules=True))
"""
Plotting
"""
#First Plot Temperature vs Time
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(tiempo_nominal, t_c_nominal, yerr=t_c_error, xerr=tiempo_error, fmt='none', color="red",
              label="Temperatura foco caliente", capsize=3, markersize=4)
plt.errorbar(tiempo_nominal, t_f_nominal, yerr=t_f_error, xerr=tiempo_error, fmt='none', color="blue",
              label="Temperatura foco frío", capsize=3, markersize=4)
plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura ºC')
#Some options:
plt.title('Temperatura vs Tiempo')
plt.legend()
plt.grid(False)
#Do the plot
plt.show()

# Second plot: Escala logarítmica y estilizado profesional
plt.figure(figsize=(8, 6), dpi=150)  # Tamaño de figura ajustado para mejor proporción

# COP Ideal: Puntos circulares ('o'), rojo oscuro con barras más claras, unidos por línea punteada
plt.errorbar(d_t_nominal, cop_ideal_nominal, yerr=cop_ideal_error, xerr=d_t_error, 
             fmt='none', color="gray", 
             label="COP ideal", capsize=3, markersize=5, linestyle='--', linewidth=1)

# COP Experimental: Cuadrados ('s'), azul oscuro con barras más claras, sin línea uniéndolos
plt.errorbar(d_t_nominal, cop_exp_nominal, yerr=cop_exp_error, xerr=d_t_error, 
             fmt='none', color="black",
             label="COP experimental", capsize=3, markersize=5, linestyle='')

# --- ESCALA LOGARÍTMICA ---
# Lo más común para el COP es poner en logarítmico solo el eje Y:
plt.yscale('log')
# plt.xscale('log') # Descomenta esta línea si también quieres el eje X en logarítmico

# Etiquetas de los ejes arregladas (sin comillas raras) y con mayor tamaño
plt.xlabel('$\Delta T$ (K)', fontsize=12)
plt.ylabel('COP (adimensional)', fontsize=12)
plt.title('Evolución del COP vs $\Delta T$', fontsize=14)

# Estilo del cuadro de leyenda
plt.legend(loc='best', frameon=True, shadow=True, fontsize=10)

# Cuadrícula adaptada para escala logarítmica (mayor y menor)
plt.grid(True, which='major', linestyle='-', linewidth=0.7, alpha=0.7, color='gray')
plt.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5, color='gray')

# Ajusta los márgenes automáticamente para que no se corte ningún texto al exportar
plt.tight_layout()

# Mostrar gráfico
plt.show()


print("Proceso finalizado.")
