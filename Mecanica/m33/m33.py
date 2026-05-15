import os
import matplotlib.pyplot as plt
import numpy as np
import statistics  as st
import scipy as sp
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

# Configurar directorio de salida
output_dir = os.path.dirname(os.path.abspath(__file__))

# Archivo de resultados
resultados_txt = os.path.join(output_dir, 'm33_resultados.txt')
with open(resultados_txt, 'w', encoding='utf-8') as f:
    pass

def log_output(text):
    print(text)
    with open(resultados_txt, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

# Configure Matplotlib: black traces with an elegant serif style
from cycler import cycler
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
	'figure.facecolor': 'white',
	'axes.facecolor': 'white',
	'axes.edgecolor': 'black',
	'axes.labelcolor': 'black',
	'xtick.color': 'black',
	'ytick.color': 'black',
	'text.color': 'black',
	'lines.linewidth': 1.6,
	'lines.markersize': 6,
	'axes.grid': True,
	'grid.color': '#e6e6e6',
	'grid.linestyle': '-',
	'grid.linewidth': 0.8,
	'font.family': 'serif',
	'font.serif': ['DejaVu Serif', 'Times New Roman'],
	'legend.frameon': False,
	'axes.prop_cycle': cycler('color', ['#000000'])
})
#functions
def sound(n,d):
    return 4 * C_frecuencia * d / n
## Data input


#Experimento A: Frecuencias and V were measured, in hz and volts respectively
A_frecuencias= [1384.313333, 1576.286667, 1708.343333, 1889.833333,2070,2191]
A_voltajes=[6.89,10.76,2.703333333,1.406666667,4.37,2.146666667]
A_u_voltajes=0.05*np.array(A_voltajes)+0.001

#Experimento B: Frecuencias and V were measured, in hz and volts respectively
B_frecuencias=[1278, 1466, 1661, 1811, 1999, 2117]
B_voltajes=[1.34, 0.926666667, 4.13, 1.693333333, 1.013333333, 1.296666667]
B_u_voltajes=0.05*np.array(B_voltajes)+0.001

# Combined frequency and voltage arrays
frecuencias = A_frecuencias + B_frecuencias
voltajes = A_voltajes + B_voltajes
u_voltajes = 0.05*np.array(voltajes) + 0.001

#Experimento C: For a maximum frecuency, the distance of the quincke tube wwas measured, in hz and cm respectively

C_frecuencia=1576
C_voltaje= [
    10.85333333, 14.82666667, 13.26, 7.423333333, 2.623333333, 
    1.923333333, 1.733333333, 1.96, 0.5, 0.6, 
    0.613333333, 1.143333333, 0.646666667, 1.353333333, 1.416666667, 
    2.0, 2.49, 1.263333333, 2.69, 4.813333333, 
    8.006666667, 11.99, 14.28, 13.23333333, 7.656666667, 
    6.063333333, 2.846666667, 3.09, 0.453333333, 1.153333333, 
    2.183333333, 2.176666667, 1.94, 1.526666667, 1.83, 
    2.716666667, 2.173333333, 3.24, 3.59, 5.496666667, 
    4.356666667, 6.146666667, 10.43666667, 10.69666667, 1.466666667, 
    5.666666667, 13.97, 11.77, 4.636666667, 3.626666667, 
    4.26, 1.903333333, 2.776666667, 2.516666667, 1.05, 
    1.31, 0.85, 1.946666667, 2.286666667, 1.513333333, 
    8.636666667, 10.50666667, 7.48
]
C_minimum_voltaje=np.array([])
C_maximum_voltaje=np.array([])
C_number_maxima=np.array([])
C_number_minima=np.array([])

C_voltaje_arr = np.array(C_voltaje)

# Find peaks (maxima)
peaks, _ = find_peaks(C_voltaje_arr, prominence=1, distance=5)
C_number_maxima = peaks
C_maximum_voltaje = C_voltaje_arr[peaks]

# Find troughs (minima) by finding peaks of the negative signal
troughs, _ = find_peaks(-C_voltaje_arr)

# Filtrar para mantener solo mínimos que alternen entre los máximos
valid_troughs = []

# Mínimo antes del primer máximo
troughs_before = [t for t in troughs if t < peaks[0]]
if troughs_before:
    valid_troughs.append(min(troughs_before, key=lambda t: C_voltaje_arr[t]))

# Mínimo entre máximos consecutivos
for i in range(len(peaks) - 1):
    troughs_between = [t for t in troughs if peaks[i] < t < peaks[i+1]]
    if troughs_between:
        valid_troughs.append(min(troughs_between, key=lambda t: C_voltaje_arr[t]))

# Mínimo después del último máximo
troughs_after = [t for t in troughs if t > peaks[-1]]
if troughs_after:
    valid_troughs.append(min(troughs_after, key=lambda t: C_voltaje_arr[t]))

valid_troughs = np.array(valid_troughs)
C_number_minima = valid_troughs
C_minimum_voltaje = C_voltaje_arr[valid_troughs]

log_output(f"Máximos en los índices: {C_number_maxima}")
log_output(f"Mínimos en los índices: {C_number_minima}")

extremes_voltaje=np.concatenate((C_maximum_voltaje, C_minimum_voltaje))
extremes_number=np.concatenate((C_number_maxima, C_number_minima))
C_distancias_cm = list(np.arange(0, 32.1, 0.51))
# Set a reasonable fixed uncertainty for distances (e.g. 0.1 cm)
C_u_distancias_cm = 0.1 * np.ones(len(C_distancias_cm))
C_u_voltajes=0.05*np.array(C_voltaje)+0.001

# Convert distances to meters
C_distancias_m = np.array(C_distancias_cm) / 100.0
C_u_distancias_m = C_u_distancias_cm / 100.0

#uncetainty

##plotting
plt.figure(constrained_layout=True)

plt.errorbar(frecuencias, voltajes, yerr=u_voltajes, xerr=np.array(frecuencias)*0.05, fmt='o', color='black', ecolor='lightgray', elinewidth=3, capsize=0)
plt.title('Voltage vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Voltage (V)')
plt.savefig(os.path.join(output_dir, 'm33_voltaje_vs_frecuencia.png'), dpi=300)
plt.show()

# Ajuste a la fórmula Δd = n * c / (4 f)
# Separar máximos y mínimos para ajustes independientes

# MÁXIMOS
if len(C_number_maxima) >= 2:
    max_idx = C_number_maxima.astype(int)
    d_pos_max_m = C_distancias_m[max_idx]
    delta_d_max_m = d_pos_max_m - d_pos_max_m[0]
    n_max = np.arange(len(max_idx), dtype=float)
    
    # Excluir primer punto para ajuste a través del origen
    mask_max = n_max > 0
    n_fit_max = n_max[mask_max]
    delta_fit_max = delta_d_max_m[mask_max]
    sigma_d_max = C_u_distancias_m[max_idx][mask_max]
    
    w_max = 1.0 / (sigma_d_max ** 2)
    s_num_max = np.sum(w_max * n_fit_max * delta_fit_max)
    s_den_max = np.sum(w_max * (n_fit_max ** 2))
    s_max = s_num_max / s_den_max
    var_s_max = 1.0 / s_den_max
    sigma_s_max = np.sqrt(var_s_max)
    c_fit_max = s_max * 4.0 * C_frecuencia
    sigma_c_max = sigma_s_max * 4.0 * C_frecuencia
    
    log_output(f"Fit MÁXIMOS: c = {c_fit_max:.2f} ± {sigma_c_max:.2f} m/s")
    
    # Plot máximos
    plt.figure(constrained_layout=True)
    plt.errorbar(n_fit_max, delta_fit_max, yerr=sigma_d_max, fmt='o', color='black', ecolor='lightgray', capsize=3)
    n_line = np.linspace(0, n_fit_max.max(), 100)
    plt.plot(n_line, s_max * n_line, '--', color='black', label=f'Maxima: c={c_fit_max:.1f} m/s')
    plt.xlabel('n (relative ordinal)')
    plt.ylabel('Δd (m)')
    plt.title('Fit Δd = n*c/(4f) - MAXIMA')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'm33_ajuste_maximos.png'), dpi=300)
    plt.show()
else:
    log_output('No hay suficientes máximos para ajustar.')

# MÍNIMOS
if len(C_number_minima) >= 2:
    min_idx = C_number_minima.astype(int)
    d_pos_min_m = C_distancias_m[min_idx]
    delta_d_min_m = d_pos_min_m - d_pos_min_m[0]
    n_min = np.arange(len(min_idx), dtype=float)
    
    # Excluir primer punto para ajuste a través del origen
    mask_min = n_min > 0
    n_fit_min = n_min[mask_min]
    delta_fit_min = delta_d_min_m[mask_min]
    sigma_d_min = C_u_distancias_m[min_idx][mask_min]
    
    w_min = 1.0 / (sigma_d_min ** 2)
    s_num_min = np.sum(w_min * n_fit_min * delta_fit_min)
    s_den_min = np.sum(w_min * (n_fit_min ** 2))
    s_min = s_num_min / s_den_min
    var_s_min = 1.0 / s_den_min
    sigma_s_min = np.sqrt(var_s_min)
    c_fit_min = s_min * 4.0 * C_frecuencia
    sigma_c_min = sigma_s_min * 4.0 * C_frecuencia
    
    log_output(f"Fit MÍNIMOS: c = {c_fit_min:.2f} ± {sigma_c_min:.2f} m/s")
    
    # Plot mínimos
    plt.figure(constrained_layout=True)
    plt.errorbar(n_fit_min, delta_fit_min, yerr=sigma_d_min, fmt='o', color='black', ecolor='lightgray', capsize=3)
    n_line = np.linspace(0, n_fit_min.max(), 100)
    plt.plot(n_line, s_min * n_line, '--', color='black', label=f'Minima: c={c_fit_min:.1f} m/s')
    plt.xlabel('n (relative ordinal)')
    plt.ylabel('Δd (m)')
    plt.title('Fit Δd = n*c/(4f) - MINIMA')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'm33_ajuste_minimos.png'), dpi=300)
    plt.show()
else:
    log_output('No hay suficientes mínimos para ajustar.')

# Comparar con teórica
theta = 27.5 # Temperatura en °C
log_output(f"\n--- Parámetros Físicos ---")
log_output(f"Temperatura: theta = {theta} °C")

c_theory = 331.3 * np.sqrt(1 + theta / 273.15)
log_output(f"Velocidad teórica a {theta} °C: c = {c_theory:.2f} m/s")
if len(C_number_maxima) >= 2:
    diff_max = (c_fit_max - c_theory) / c_theory * 100.0
    log_output(f"Diferencia MÁXIMOS: {diff_max:.2f} %")
if len(C_number_minima) >= 2:
    diff_min = (c_fit_min - c_theory) / c_theory * 100.0
    log_output(f"Diferencia MÍNIMOS: {diff_min:.2f} %")


#plotting (mostrar distancias en metros)
plt.figure(constrained_layout=True)
plt.errorbar(C_distancias_m, C_voltaje, yerr=C_u_voltajes, xerr=C_u_distancias_m, fmt='o', color='black', ecolor='lightgray', elinewidth=3, capsize=0)
plt.plot(C_distancias_m[C_number_maxima.astype(int)], np.array(C_voltaje)[C_number_maxima.astype(int)], 'rv', markersize=8, label='Detected maxima')
plt.plot(C_distancias_m[C_number_minima.astype(int)], np.array(C_voltaje)[C_number_minima.astype(int)], 'b^', markersize=8, label='Detected minima')
plt.title('Voltage vs Distance')
plt.xlabel('Distance (m)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.savefig(os.path.join(output_dir, 'm33_voltaje_vs_distancia.png'), dpi=300)
plt.show()