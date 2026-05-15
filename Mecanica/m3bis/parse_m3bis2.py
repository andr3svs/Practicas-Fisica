import pandas as pd, numpy as np
xls = pd.ExcelFile('C:/Users/Andres/Practicas-Fisica/Mecanica/m3bis/m3bis2.xlsx')

w0 = pd.read_excel(xls, sheet_name='w0')
wsd = pd.read_excel(xls, sheet_name='wsderecha')
wsi = pd.read_excel(xls, sheet_name='wsizquierda')
wad = pd.read_excel(xls, sheet_name='waderecha')
wai = pd.read_excel(xls, sheet_name='waizquierda')
md = pd.read_excel(xls, sheet_name='minderecho')
mi = pd.read_excel(xls, sheet_name='minizquierdo')

print(f"w0: {w0['w_0_final'].dropna().values[0]:.2f}")
print(f"ws (d): {wsd['w_s_d_av'].dropna().values[0]:.2f}, ws (i): {wsi['w_s_av'].dropna().values[0]:.2f}")
print(f"wa (d): {wad['w_a_d'].dropna().values[0]:.2f}, wa (i): {wai['w_a_iz_av'].dropna().values[0]:.2f}")

f_max_d = md['f_max'].dropna().mean()
f_max_small_d = md['f_max_small'].dropna().mean()
print(f"min_der: max_small {f_max_small_d * 2 * np.pi:.2f} rad/s, max {f_max_d * 2 * np.pi:.2f} rad/s")

