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
def generate_uncertainties_for_chi2_1(data, fit, num_params):
    """
    Generate uncertainties that produce chi_squared_red = 1
    We want to make the reduced chi-squared equal to 1,
    which means that the uncertainties should be set such
    that the sum of squared residuals divided by the degrees of freedom equals 1.
    
    Works for any axis (x or y data).

    Args:
        data: measured data points (x or y)
        fit: fitted/theoretical values (x or y)
        num_params: number of parameters in the fit
        
    
    Returns:
        uncertainties array
    """
    residuals = data - fit
    dof = len(data) - num_params
    
    # Standard deviation of residuals
    sigma = np.sqrt(np.sum(residuals**2) / dof)
    
    # All uncertainties equal to sigma
    uncertainties = np.full_like(data, sigma, dtype=float)
    
    return uncertainties
def Rutherford_scattering_fit(b,theta,v_0,r_0,k):
    """
    Rutherford scattering fit function.  
    Parameters: b: impact parameter, theta: scattering angle, v_0: initial velocity,
      r_0 distance of the center of the well to the center of forces
    Implicit relation for all the variables.  
    """
    return b*1/np.cos(theta/2)-(k/(m*v_0**2))*(1/np.sin(theta/2))+r_0

"""
Fixed parameters for the plot
"""
g= 9.81 #Gravity acceleration, in m/s^2
b_exp=7.5e-2 #Initial distance to the well, in meters
v_0_06_exp=sqrt(2*g*0.06) #Initial velocity, in m/s
v_0_07_exp=sqrt(2*g*0.07)
v_0_08_exp=sqrt(2*g*0.08)
v_0_09_exp=sqrt(2*g*0.09)
v_0_10_exp=sqrt(2*g*0.10)
v_0_11_exp=sqrt(2*g*0.11)

theta_06_exp=np.radians(30) #Scattering angle, in radians
theta_07_exp=np.radians(35)
theta_08_exp=np.radians(40)
theta_09_exp=np.radians(45)
theta_10_exp=np.radians(50)
theta_11_exp=np.radians(55)

r_0_exp=0.1 #Distance of the center of the well to the center of forces, in meters



"""
INTRODUCING DATAx
The data for the laboratory practice must be taken into an excel file, and this will read it.
"""
#Excel file location
excel_path_user="C:\\Users\\Andres\\proyectos\\Mecanica\\m12bis_mecanica\\m12bis.xlsx"
data_raw=pd.read_excel(excel_path_user,sheet_name="Sheet")
#The trayectories of the well case that will be fitted.
x_06= pd.DataFrame(data_raw["x0.6"])
y_06= pd.DataFrame(data_raw["y0.6"])
x_07= pd.DataFrame(data_raw["x0.7"])
y_07= pd.DataFrame(data_raw["y0.7"])
x_08= pd.DataFrame(data_raw["x0.8"])
y_08= pd.DataFrame(data_raw["y0.8"])
x_09= pd.DataFrame(data_raw["x0.9"])
y_09= pd.DataFrame(data_raw["y0.9"])
x_10= pd.DataFrame(data_raw["x1.0"])
y_10= pd.DataFrame(data_raw["y1.0"])
x_11= pd.DataFrame(data_raw["x1.1"])
y_11= pd.DataFrame(data_raw["y1.1"])

### The uncertainties will be chosen artificially to chi reduced square=1, since the theory is already proven 

"""
Data manipulation
"""
"""
Fit
"""
# Fit para todas las alturas
popt_06, pcov_06 = np.curve_fit(Rutherford_scattering_fit, b_exp, theta_06_exp, v_0_06_exp, r_0_exp)
print("Parámetros del fit (0.6 cm):")
print(f"  k = {popt_06[0]:.4e}")
print(f"  Covarianza:\n{pcov_06}\n")

popt_07, pcov_07 = np.curve_fit(Rutherford_scattering_fit, b_exp, theta_07_exp, v_0_07_exp, r_0_exp)
print("Parámetros del fit (0.7 cm):")
print(f"  k = {popt_07[0]:.4e}")
print(f"  Covarianza:\n{pcov_07}\n")

popt_08, pcov_08 = np.curve_fit(Rutherford_scattering_fit, b_exp, theta_08_exp, v_0_08_exp, r_0_exp)
print("Parámetros del fit (0.8 cm):")
print(f"  k = {popt_08[0]:.4e}")
print(f"  Covarianza:\n{pcov_08}\n")

popt_09, pcov_09 = np.curve_fit(Rutherford_scattering_fit, b_exp, theta_09_exp, v_0_09_exp, r_0_exp)
print("Parámetros del fit (0.9 cm):")
print(f"  k = {popt_09[0]:.4e}")
print(f"  Covarianza:\n{pcov_09}\n")

popt_10, pcov_10 = np.curve_fit(Rutherford_scattering_fit, b_exp, theta_10_exp, v_0_10_exp, r_0_exp)
print("Parámetros del fit (1.0 cm):")
print(f"  k = {popt_10[0]:.4e}")
print(f"  Covarianza:\n{pcov_10}\n")

popt_11, pcov_11 = np.curve_fit(Rutherford_scattering_fit, b_exp, theta_11_exp, v_0_11_exp, r_0_exp)
print("Parámetros del fit (1.1 cm):")
print(f"  k = {popt_11[0]:.4e}")
print(f"  Covarianza:\n{pcov_11}\n")

"""
Obtention of uncertaintes for the fit parameters
"""
generate_uncertainties_for_chi2_1(y_data=y_06, y_fit=Rutherford_scattering_fit(x_06, *popt_06), num_params=len(popt_06))
"""
Plotting
"""
#h1_aire vs coeficiente adiabatico experimental
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(x_06, coeficiente_adiabatico_aire_nominl, yerr=coeficiente_adiabatico_aire_error, xerr=h1_aire_error, fmt='none', color="red",
              label="Coeficiente adiabático aire", capsize=3, markersize=4)
# 2. LÍNEA TEÓRICA (axhline)
# y: valor donde se dibuja. linestyle: estilo de línea ('-' continua, '--' discontinua)
plt.axhline(y=gamma_teorico_aire, color='firebrick', linestyle='-', linewidth=2, 
            label='Valor teórico (Gas Diatómico)')

# 3. LÍNEA BIBLIOGRÁFICA (axhline)
plt.axhline(y=gamma_biblio_aire, color='forestgreen', linestyle='--', linewidth=2, 
            label='Valor bibliográfico')

plt.xlabel('h1 aire (cm)', fontsize=12)
plt.ylabel('Coeficiente adiabático', fontsize=12)
#Some options:
plt.title('Coeficiente adiabático experimental vs h1 aire', fontsize=14)
plt.legend()
plt.grid(False)
#Do the plot
plt.show()


#h1_co2 vs coeficiente adiabatico experimental
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(h1_co2_nominal, coeficiente_adiabatico_co2_nominal, yerr=coeficiente_adiabatico_co2_error, xerr=h1_co2_error, fmt='none', color="blue",
              label="Coeficiente adiabático CO2", capsize=3, markersize=4)
# 2. LÍNEA TEÓRICA (axhline)
# y: valor donde se dibuja. linestyle: estilo de línea ('-' continua, '--' discontinua)
plt.axhline(y=gamma_teorico_co2, color='firebrick', linestyle='-', linewidth=2, 
            label='Valor teórico (Gas Diatómico)')

# 3. LÍNEA BIBLIOGRÁFICA (axhline)
plt.axhline(y=gamma_biblio_co2, color='forestgreen', linestyle='--', linewidth=2, 
            label='Valor bibliográfico')

plt.xlabel('h1 co2 (cm)', fontsize=12)
plt.ylabel('Coeficiente adiabático', fontsize=12)
#Some options:
plt.title('Coeficiente adiabático experimental vs h1 co2', fontsize=14)
plt.legend()
plt.grid(False)
#Do the plot
plt.show()


print("Proceso finalizado.")
