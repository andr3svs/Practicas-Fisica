import numpy as np
from uncertainties import unumpy as unp


def measured(values, type_b):
    values = np.asarray(values, dtype=float)
    if values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("Rellena todos los arrays de datos experimentales.")
    type_a = np.std(values, ddof=1) / np.sqrt(values.size) if values.size > 1 else 0.0
    error = np.sqrt(type_a**2 + np.asarray(type_b, dtype=float) ** 2)
    return unp.uarray(values, error)


def finite(result, name):
    nominal = np.asarray(unp.nominal_values(result), dtype=float)
    error = np.asarray(unp.std_devs(result), dtype=float)
    if not np.all(np.isfinite(nominal)) or not np.all(np.isfinite(error)):
        raise ValueError(f"Resultado no finito en {name}.")


def show(name, result):
    finite(result, name)
    print(name, [f"{value:.3uS}" for value in np.atleast_1d(result)])


# DATOS EXPERIMENTALES: sustituye los arrays y las incertidumbres tipo B.
U = np.array([], dtype=float)  # V, tension aceleradora
I = np.array([], dtype=float)  # A, corriente de Helmholtz
diameter = np.array([], dtype=float)  # m, diametro de la trayectoria
u_U = 0.0  # V
u_I = 0.0  # A
u_diameter = 0.0  # m

N = 124.0
coil_radius = 0.150  # m
mu0 = 4 * np.pi * 1e-7  # N A^-2

if not len(U) == len(I) == len(diameter):
    raise ValueError("U, I y diameter deben tener la misma longitud.")
U_u = measured(U, u_U)
I_u = measured(I, u_I)
diameter_u = measured(diameter, u_diameter)
if np.any(unp.nominal_values(I_u) == 0) or np.any(unp.nominal_values(diameter_u) <= 0):
    raise ValueError("La corriente y el diametro deben ser no nulos y positivos.")

radius_u = diameter_u / 2
field_u = (5 / 4) ** 1.5 * N * mu0 * I_u / coil_radius
if np.any(unp.nominal_values(field_u) == 0):
    raise ValueError("El campo magnetico no puede ser cero.")

charge_to_mass = 2 * U_u / (field_u**2 * radius_u**2)
show("e/m (C kg^-1):", charge_to_mass)
