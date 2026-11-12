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


# DATOS EXPERIMENTALES: posiciones de extremos de cada curva I(V).
hg_maxima_v = np.array([], dtype=float)  # V
hg_minima_v = np.array([], dtype=float)  # V
hg_temperature_c = np.array([], dtype=float)  # C, una por curva registrada
hg_stopping_v = np.array([], dtype=float)  # V, una por curva registrada
ne_maxima_v = np.array([], dtype=float)  # V
ne_minima_v = np.array([], dtype=float)  # V
ne_stopping_v = np.array([], dtype=float)  # V
u_voltage = 0.0  # V
u_temperature = 0.0  # C

hg_max_u = measured(hg_maxima_v, u_voltage)
hg_min_u = measured(hg_minima_v, u_voltage)
hg_temp_u = measured(hg_temperature_c, u_temperature)
hg_stop_u = measured(hg_stopping_v, u_voltage)
ne_max_u = measured(ne_maxima_v, u_voltage)
ne_min_u = measured(ne_minima_v, u_voltage)
ne_stop_u = measured(ne_stopping_v, u_voltage)
if hg_max_u.size < 2 or hg_min_u.size < 2 or ne_max_u.size < 2 or ne_min_u.size < 2:
    raise ValueError("Se necesitan al menos dos maximos y dos minimos por gas.")
if len(hg_temperature_c) != len(hg_stopping_v) or len(ne_stopping_v) == 0:
    raise ValueError("Cada curva debe tener temperatura y potencial de frenado.")
if np.any(unp.nominal_values(np.diff(hg_max_u)) == 0) or np.any(
    unp.nominal_values(np.diff(hg_min_u)) == 0
):
    raise ValueError("Los extremos consecutivos no pueden coincidir.")

hg_max_spacing = np.diff(hg_max_u)
hg_min_spacing = np.diff(hg_min_u)
ne_max_spacing = np.diff(ne_max_u)
ne_min_spacing = np.diff(ne_min_u)
electron_charge = 1.602176634e-19
hg_energy_j = electron_charge * (sum(hg_max_spacing) / len(hg_max_spacing))
ne_energy_j = electron_charge * (sum(ne_max_spacing) / len(ne_max_spacing))

show("separacion de maximos Hg (V):", hg_max_spacing)
show("separacion de minimos Hg (V):", hg_min_spacing)
show("energia de excitacion Hg (J):", hg_energy_j)
show("separacion de maximos Ne (V):", ne_max_spacing)
show("separacion de minimos Ne (V):", ne_min_spacing)
show("energia de excitacion Ne (J):", ne_energy_j)
