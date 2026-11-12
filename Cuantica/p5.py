import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Datos: voltaje en V y radio en mm, convertido después a m.
array_voltage = np.array([2480, 3040, 3520, 4000, 4510, 5000, 4300, 3800], dtype=float)
radius2 = np.array([10.6, 9.8, 9.7, 9.5, 9, 8.95, 8.75, 10.075], dtype=float) * 1e-3
radius1 = (
    np.array([16.275, 13.8, 13.025, 13, 12.225, 11.925, 12.75, 14.2], dtype=float)
    * 1e-3
)

R = 65e-3  # Provided by the guide
h = 6.62607015e-34
electron_charge = 1.602176634e-19
electron_mass = 9.1093837015e-31

lambda_electron = h / np.sqrt(2 * electron_mass * electron_charge * array_voltage)
print("De Broglie wavelength (m):", lambda_electron)

# Hipotesis alternativa: ambos anillos tienen el mismo d1, pero n=1 y n=2.
d1 = 213e-12
radius_n1 = 2 * R * lambda_electron / d1
radius_n2 = 2 * R * 2 * lambda_electron / d1
ratio_measured = radius2 / radius1

print("Hipotesis: mismo d1 = 213 pm, con n=1 y n=2")
print("Radio teorico n=1 (mm):", radius_n1 * 1e3)
print("Radio teorico n=2 (mm):", radius_n2 * 1e3)
print("Razon medida radius2/radius1:", ratio_measured)
print("Razon teorica radio(n=2)/radio(n=1): 2.0")
print("Razon media medida radius2/radius1:", ratio_measured.mean())
print(
    "Error relativo medio radius1 frente a n=1 (%):",
    np.mean((radius1 - radius_n1) / radius_n1) * 100,
)
print(
    "Error relativo medio radius2 frente a n=2 (%):",
    np.mean((radius2 - radius_n2) / radius_n2) * 100,
)

# Seccion 1 Comprobar de broigle
voltage_inverse_s = 1 / np.sqrt(array_voltage)
slope, intercept, r_value, p_value, std_err = linregress(voltage_inverse_s, radius1)
print("Slope:", slope)
print("Intercept:", intercept)
print("R-squared:", r_value**2)

# plotting the data and the fit
uncertainty_radius = 0.05e-3
plt.errorbar(
    voltage_inverse_s,
    radius1 * 1e3,
    yerr=np.full_like(radius1, uncertainty_radius) * 1e3,
    fmt="o",
    capsize=3,
    label="Datos Experimentales",
    color="blue",
)
plt.plot(
    voltage_inverse_s,
    (slope * voltage_inverse_s + intercept) * 1e3,
    color="red",
    label="Fit",
)
plt.plot(
    voltage_inverse_s,
    radius_n1 * 1e3,
    color="tab:green",
    linestyle="--",
    label="Prediccion d1, n=1",
)
plt.plot(
    voltage_inverse_s,
    radius_n2 * 1e3,
    color="tab:orange",
    linestyle="--",
    label="Prediccion d1, n=2",
)
plt.xlabel("$1/\\sqrt{V}$ ($\\mathrm{V}^{-1/2}$)")
plt.ylabel("Radio (mm)")
plt.title("Radio vs $\\frac{1}{\\sqrt{V}}$")
plt.legend()
plt.grid()
plt.show()
