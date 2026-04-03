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
Fixed parameters for the plot
gamma theoretical and bibliographic values for air and co2
gamma is the adiabatic coefficient, which is the ratio of specific heats (Cp/Cv) for a gas.
For diatomic gases like air, the theoretical value of gamma is approximately 1.4.
For CO2, which is a linear molecule with more degrees of freedom, the theoretical value of gamma is approximately 1.3.
"""
gamma_teorico_aire = 1.4  # Diatomic gas (like air) using the equipartition theorem
gamma_teorico_co2 = 1.3 # Triatomic linear molecule (like CO2)
gamma_biblio_aire = 1.41 #+-0.05  #https://www.researchgate.net/profile/Jose-Faro-2/publication/243492025_A_simple_experiment_for_measuring_the_adiabatic_coefficient_of_air/links/57768c9008ae1b18a7e1acd1/A-simple-experiment-for-measuring-the-adiabatic-coefficient-of-air.pdf
gamma_biblio_co2 = 1.294   # https://sci-hub.ru/10.1063/1.1723788
"""
INTRODUCING DATAx
The data for the laboratory practice must be taken into an excel file, and this will read it.
"""
#Excel file location
excel_path_user="C:/Users/Andres/proyectos/p7_termodinamica/p7.xlsx"
data_raw=pd.read_excel(excel_path_user,sheet_name="Sheet")
h1_aire_ufloat = unumpy.uarray(data_raw["h1_aire"],data_raw["u_h1_aire"])
h2_aire_ufloat= unumpy.uarray(data_raw["h2_aire"],data_raw["u_h2_aire"])
h1_co2_ufloat= unumpy.uarray(data_raw["h1_co2"],data_raw["u_h1_co2"])
h2_co2_ufloat= unumpy.uarray(data_raw["h2_co2"],data_raw["u_h2_co2"])

"""
Data manipulation
"""
coeficiente_adiabatico_aire_experimental=(h1_aire_ufloat)/(h1_aire_ufloat-h2_aire_ufloat)
coeficiente_adiabatico_co2_experimental=(h1_co2_ufloat)/(h1_co2_ufloat-h2_co2_ufloat)
#Get data into numpy usable form
h1_aire_nominal,h1_aire_error= separate_uncertainties(h1_aire_ufloat)
h2_aire_nominal,h2_aire_error= separate_uncertainties(h2_aire_ufloat)
h1_co2_nominal,h1_co2_error= separate_uncertainties(h1_co2_ufloat)
h2_co2_nominal,h2_co2_error= separate_uncertainties(h2_co2_ufloat)
coeficiente_adiabatico_aire_nominal, coeficiente_adiabatico_aire_error= separate_uncertainties(coeficiente_adiabatico_aire_experimental)
coeficiente_adiabatico_co2_nominal, coeficiente_adiabatico_co2_error= separate_uncertainties(coeficiente_adiabatico_co2_experimental)   

"""
Plotting
"""
#h1_aire vs coeficiente adiabatico experimental
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(h1_aire_nominal, coeficiente_adiabatico_aire_nominal, yerr=coeficiente_adiabatico_aire_error, xerr=h1_aire_error, fmt='none', color="red",
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
