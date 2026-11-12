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


# DATOS EXPERIMENTALES: rellena los picos identificados en el espectrometro.
mercury_wavelength_nm = np.array([], dtype=float)  # nm, picos medidos
mercury_counts = np.array([], dtype=float)  # cuentas integradas del pico
hydrogen_wavelength_nm = np.array([], dtype=float)  # nm
hydrogen_upper_n = np.array([], dtype=float)  # n superior de cada linea de Balmer
helium_wavelength_nm = np.array([], dtype=float)  # nm
helium_counts = np.array([], dtype=float)  # cuentas integradas del pico
u_mercury_wavelength_nm = 0.3  # nm
u_hydrogen_wavelength_nm = 0.3  # nm
u_helium_wavelength_nm = 0.3  # nm
u_counts = 0.0

mercury_reference_nm = np.array(
    [365.0579, 365.48429, 404.65643, 435.8335, 546.075, 576.961, 578.969, 579.067]
)
if mercury_wavelength_nm.size != mercury_reference_nm.size:
    raise ValueError(
        "mercury_wavelength_nm debe contener los ocho picos de referencia."
    )
if mercury_counts.size != mercury_wavelength_nm.size:
    raise ValueError("mercury_counts debe tener una entrada por pico.")
if (
    hydrogen_upper_n.size != hydrogen_wavelength_nm.size
    or helium_counts.size != helium_wavelength_nm.size
):
    raise ValueError("Los arrays de cada espectro deben tener longitudes compatibles.")
if np.any(hydrogen_upper_n <= 2):
    raise ValueError("Los niveles superiores de Balmer deben cumplir n > 2.")

mercury_u = measured(mercury_wavelength_nm, u_mercury_wavelength_nm)
mercury_counts_u = measured(mercury_counts, u_counts)
hydrogen_u = measured(hydrogen_wavelength_nm, u_hydrogen_wavelength_nm)
helium_u = measured(helium_wavelength_nm, u_helium_wavelength_nm)
helium_counts_u = measured(helium_counts, u_counts)
calibration_residual = mercury_u - mercury_reference_nm
balmer_constant = hydrogen_u * (hydrogen_upper_n**2 - 4) / hydrogen_upper_n**2

show("error de calibracion (nm):", calibration_residual)
show("constante C de Balmer (nm):", balmer_constant)
show("longitudes de onda de helio (nm):", helium_u)
show("cuentas de mercurio:", mercury_counts_u)
show("cuentas de helio:", helium_counts_u)
