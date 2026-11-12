import numpy as np
from uncertainties import unumpy as unp


def measured(values, type_b):
    values = np.asarray(values, dtype=float)
    if values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("Rellena todos los arrays de datos experimentales.")
    type_a = np.std(values, ddof=1) / np.sqrt(values.size) if values.size > 1 else 0.0
    return unp.uarray(values, np.sqrt(type_a**2 + np.asarray(type_b, dtype=float) ** 2))


def show(name, result):
    nominal = np.asarray(unp.nominal_values(result), dtype=float)
    error = np.asarray(unp.std_devs(result), dtype=float)
    if not np.all(np.isfinite(nominal)) or not np.all(np.isfinite(error)):
        raise ValueError(f"Resultado no finito en {name}.")
    print(name, [f"{value:.3uS}" for value in np.atleast_1d(result)])


# DATOS EXPERIMENTALES: una fila por medida de cada color y orden.
wavelength_nm = np.array([], dtype=float)  # nm
stopping_voltage = np.array([], dtype=float)  # V
stabilization_time = np.array([], dtype=float)  # s
transmission = np.array([], dtype=float)  # 0-1
diffraction_order = np.array([], dtype=int)
u_wavelength_nm = 0.3  # nm, precision del espectrometro
u_stopping_voltage = 0.0  # V
u_stabilization_time = 0.0  # s
u_transmission = 0.0

c = 299792458.0  # m s^-1
electron_charge = 1.602176634e-19  # C
wavelength_u = measured(wavelength_nm * 1e-9, u_wavelength_nm * 1e-9)
voltage_u = measured(stopping_voltage, u_stopping_voltage)
time_u = measured(stabilization_time, u_stabilization_time)
transmission_u = measured(transmission, u_transmission)
if diffraction_order.size == 0 or diffraction_order.size != wavelength_nm.size:
    raise ValueError("diffraction_order debe tener una entrada por medida.")
if not len(stopping_voltage) == len(stabilization_time) == len(transmission):
    raise ValueError("Los arrays de p2 deben tener la misma longitud.")
if np.any(unp.nominal_values(wavelength_u) <= 0):
    raise ValueError("Las longitudes de onda deben ser positivas.")

frequency_u = c / wavelength_u
denominator = (
    len(frequency_u) * sum(value**2 for value in frequency_u) - sum(frequency_u) ** 2
)
if abs(float(unp.nominal_values(denominator))) <= 0:
    raise ValueError("No se puede calcular la recta: frecuencias insuficientes.")
slope = (
    len(frequency_u) * sum(x * y for x, y in zip(frequency_u, voltage_u))
    - sum(frequency_u) * sum(voltage_u)
) / denominator
intercept = (sum(voltage_u) - slope * sum(frequency_u)) / len(frequency_u)
work_function = -electron_charge * intercept

show("frecuencia (Hz):", frequency_u)
show("tiempo de estabilizacion (s):", time_u)
show("potencial de frenado (V):", voltage_u)
show("h/e (J C^-1 s):", slope)
show("frecuencia umbral (Hz):", -intercept / slope)
show("funcion de trabajo (J):", work_function)
