#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#* EffortModel (modificado para Punto 9)
#* Programa para procesar modelos lineales y exponenciales (Mínimos cambios)
#* UADER - FCyT - Ingeniería de Software II
#* Dr. Pedro E. Colla (base) - ajustes por alumno
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

import numpy as np
import pandas as pd
import argparse
import statsmodels.api as sm
import sys
import os
import matplotlib.pyplot as plt

# -------------------------
# Dataset solicitado (Punto 9)
# -------------------------
data = {
    'LOC':    [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
    'Esfuerzo': [2,    3,    5,    7,    11,   13,   17,   19,   23,   29]
}

# Inicialización
version="7.1"
os.system('cls' if os.name == 'nt' else 'clear')

# Argumentos (opcional, conserva compatibilidad)
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--version", required=False, help="version", action="store_true")
ap.add_argument("-p", "--plot", required=False, help="Mostrar plot (default True)", action="store_true")
args = vars(ap.parse_args())

if args['version'] == True:
   print("Program %s version %s" % (sys.argv[0],version))
   sys.exit(0)

# Construir DataFrame
df = pd.DataFrame(data)
print("\nDataset histórico (LOC vs Esfuerzo)")
print(df)

# -------------------------
# 1) Modelo Lineal (y = m*x + c)
# -------------------------
x = df['LOC'].values
y = df['Esfuerzo'].values

# Ajuste lineal (np.polyfit)
m, c = np.polyfit(x, y, 1)   # m = pendiente, c = intercepto (returns [m, c])
# Predicciones y métricas
y_pred_lin = m * x + c
ss_res_lin = np.sum((y - y_pred_lin)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2_lin = 1 - ss_res_lin/ss_tot

print("\nModelo lineal ajustado:")
print(f"  E_lineal(LOC) = {m:.6f}*LOC + {c:.6f}")
print(f"  R-squared (lineal) = {r2_lin:.4f}")

# -------------------------
# 2) Modelo Exponencial (E = k * LOC^b) via log-log OLS
#    ln(E) = ln(k) + b * ln(LOC)
# -------------------------
# Transformaciones logaritmicas
df['logLOC'] = np.log(df['LOC'])
df['logEsfuerzo'] = np.log(df['Esfuerzo'])

X = sm.add_constant(df['logLOC'])  # intercept + slope
Y = df['logEsfuerzo']
model_log = sm.OLS(Y, X).fit()

lnk = model_log.params['const']
b = model_log.params['logLOC']
k = np.exp(lnk)
r2_exp = model_log.rsquared

print("\nModelo exponencial ajustado (log-log OLS):")
print(f"  ln(E) = {lnk:.6f} + {b:.6f} * ln(LOC)")
print(f"  => E_exp(LOC) = {k:.6f} * LOC^{b:.6f}")
print(f"  R-squared (exponencial, log-log) = {r2_exp:.4f}")

# -------------------------
# 3) Elegir el mejor modelo por R^2 (comparar r2_lin con r2_exp)
# -------------------------
# Nota: r2_exp proviene del ajuste en log-log; lo comparamos directamente aunque
#       no sea exactamente idéntico en interpretación a R^2 en escala original.
best_model = 'lineal' if r2_lin >= r2_exp else 'exponencial'
print(f"\nMejor modelo según R^2: {best_model} (R2_lineal={r2_lin:.4f}, R2_exponencial={r2_exp:.4f})")

# -------------------------
# 4) Estimaciones pedidas: LOC = 9100 y LOC = 200
# -------------------------
loc1 = 9100
loc2 = 200

# Predicción lineal
pred_lin_loc1 = m * loc1 + c
pred_lin_loc2 = m * loc2 + c

# Predicción exponencial
pred_exp_loc1 = k * (loc1 ** b)
pred_exp_loc2 = k * (loc2 ** b)

print("\nEstimaciones:")
print(f"  LOC={loc1}:  lineal => {pred_lin_loc1:.3f} PM,  exponencial => {pred_exp_loc1:.3f} PM")
print(f"  LOC={loc2}:  lineal => {pred_lin_loc2:.3f} PM,  exponencial => {pred_exp_loc2:.3f} PM")

# Selección final: usar el mejor modelo para los cálculos de la consigna
if best_model == 'lineal':
    estim_loc1 = pred_lin_loc1
    estim_loc2 = pred_lin_loc2
    modelo_usado_text = f"Modelo lineal: E(LOC) = {m:.6f}*LOC + {c:.6f}"
else:
    estim_loc1 = pred_exp_loc1
    estim_loc2 = pred_exp_loc2
    modelo_usado_text = f"Modelo exponencial: E(LOC) = {k:.6f} * LOC^{b:.6f}"

print(f"\nModelo seleccionado para estimar (según R^2): {modelo_usado_text}")
print(f"Estimación final para LOC={loc1}: {estim_loc1:.3f} PM")
print(f"Estimación final para LOC={loc2}: {estim_loc2:.3f} PM")

# -------------------------
# 5) Graficar: datos históricos + ambos modelos + marcar las estimaciones
# -------------------------
x_plot = np.linspace(min(x)*0.8, max(x)*1.05, 400)

y_line_plot = m * x_plot + c
y_exp_plot = k * (x_plot ** b)

plt.figure(figsize=(9,6))
plt.scatter(x, y, label='Datos históricos', zorder=5, color='black')
plt.plot(x_plot, y_line_plot, label=f'Modelo lineal (R2={r2_lin:.3f})', color='red', linewidth=1.6)
plt.plot(x_plot, y_exp_plot, label=f'Modelo exponencial (R2={r2_exp:.3f})', color='green', linewidth=1.6)
# marcar estimaciones
plt.scatter([loc1], [pred_lin_loc1], marker='x', color='red', s=80, label=f'Pred lineal LOC={loc1}: {pred_lin_loc1:.2f}')
plt.scatter([loc1], [pred_exp_loc1], marker='o', color='green', s=80, label=f'Pred exp LOC={loc1}: {pred_exp_loc1:.2f}')
plt.scatter([loc2], [pred_lin_loc2], marker='x', color='red', s=80, label=f'Pred lineal LOC={loc2}: {pred_lin_loc2:.2f}')
plt.scatter([loc2], [pred_exp_loc2], marker='o', color='green', s=80, label=f'Pred exp LOC={loc2}: {pred_exp_loc2:.2f}')

plt.xlabel('Tamaño [LOC]')
plt.ylabel('Esfuerzo [PM]')
plt.title('Ajuste de modelos: Lineal vs Exponencial (Punto 9)')
plt.legend(loc='upper left')
plt.grid(alpha=0.3)
plt.show()

# -------------------------
# 6) Mensaje final y advertencia sobre extrapolación para LOC=200
# -------------------------
print("\n--- Observaciones finales ---")
print(f"Mejor modelo por R^2: {best_model}")
print(f"Estimación elegida para LOC={loc1}: {estim_loc1:.3f} PM")
print(f"Estimación elegida para LOC={loc2}: {estim_loc2:.3f} PM")
print("\nPrecaución: la estimación para LOC=200 implica extrapolación hacia abajo\n"
    "fuera del rango de datos históricos (el mínimo histórico es 1000 LOC). "
    "Las predicciones en áreas fuera del rango de calibración pueden ser poco confiables; "
    "se recomienda validar con datos adicionales o usar juicio experto.")
