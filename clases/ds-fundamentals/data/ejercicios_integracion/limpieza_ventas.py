import pandas as pd
import numpy as np
import json

try:
    ventas = pd.read_csv('ejercicios_integracion/ventas_tienda_simulada.csv')
    print(ventas.head())
except FileNotFoundError:
    print("Archivo no encontrado :|")
    exit()
with open('C:\Users\Caesar\Documents\GitHub\mitic-data-science-team-1-septiembre-2024\clases\ds-fundamentals\data\ejercicios_integracion\\competencia_kaggle.json') as f:
    competencia = json.load(f)

ventas.fillna(0, inplace=True)


ventas['total'] = ventas['cantidad'] * ventas['precio_unitario']

total_ventas = ventas['total'].sum()
promedio_precio = ventas['precio_unitario'].mean()

print(f'Total de ventas: {total_ventas}')
print(f'Precio promedio por unidad: {promedio_precio}')

ventas.to_csv('ejercicios_integracion/ventas_limpias.csv', index=False)


