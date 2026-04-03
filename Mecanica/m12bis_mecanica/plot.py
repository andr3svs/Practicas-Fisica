import matplotlib.pyplot as plt
import pandas as pd

# 1. Leer el excel
# Asegúrate de que el nombre del archivo coincida (data.xlsm o data.xlsx)
df = pd.read_excel("m12bis.xlsx", sheet_name=("Sheet1"))

x = df["x0.7"] # Usamos "t" para el eje X si el label dice "Tiempo (s)"
y = df['y0.7']

# 2. Configuración de estilo
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

# Tamaños de fuente grandes
FS_LABEL = 16
FS_TITLE = 18
FS_TICK = 14

# 3. Representar el decaimiento
# Se eliminó la línea plt.errorbar(x,y,yerr=y_u_c,fmt='o') que arruinaba el formato
ax.errorbar(x,y,
            label='Datos experimentales')

# 4. Etiquetas y títulos
ax.set_xlabel("x (cm)", fontsize=FS_LABEL, fontweight='bold')
ax.set_ylabel("y (cm)", fontsize=FS_LABEL, fontweight='bold')
ax.set_title("Trayectoria h=0.6", fontsize=FS_TITLE, fontweight='bold')

# Ajustar tamaño de los números en los ejes
ax.tick_params(axis='both', labelsize=FS_TICK)

# Leyenda
ax.legend(fontsize=14, frameon=True, edgecolor='black')

# 5. Guardar y finalizar
plt.tight_layout()
plt.savefig("grafico_amortiguado_limpio.png")