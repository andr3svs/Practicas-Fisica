import pandas as pd
xls = pd.ExcelFile('C:/Users/Andres/Practicas-Fisica/Mecanica/m3bis/m3bis2.xlsx')
for sheet in xls.sheet_names:
    print(f'Sheet: {sheet}')
    df = pd.read_excel(xls, sheet_name=sheet, nrows=99)
    print(df)
