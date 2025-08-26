#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* PNR_sistemis
#* Programa para procesar modelos dinámicos basado en el modelo de Putman-Norden_Rayleigh
#*
#* UADER - FCyT
#* Ingeniería de Software II
#*
#* Dr. Pedro E. Colla
#* copyright (c) 2023,2024
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

import pandas as pd
import numpy as np
import sys
import os
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, root_scalar
from scipy.integrate import quad
import argparse

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*                             Librerías y funciones de soporte
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

def E_proyecto(K,a,gamma):
   tf=np.sqrt(-np.log(1-gamma)/a)
   Ef=gamma*K
   return tf,Ef

def E_acum(K,a,t):
    return K*(1-np.exp(-a*(t**2)))

# p(t): esfuerzo instantáneo / staff
def E(t, K, a):
    return 2 * K * a * t * np.exp(-a * t**2)

def find_near_zero(K, a, tolerance):
    def equation(t):
        return E(t, K, a) - tolerance
    result = root_scalar(equation, bracket=[0.1, 100], method='brentq')
    t_near_zero = result.root if result.converged else None
    return t_near_zero

def find_maximum(K, a):
    def negative_E(t):
        return -E(t, K, a)
    result = minimize_scalar(negative_E, bounds=(0, 100), method='bounded')
    t_max = result.x
    E_max = E(t_max, K, a)
    return t_max, E_max

def y(t, K, a, z):
    return 2 * K * a * t * np.exp(-a * t**2) - z

def find_zeros(K, a, z):
    zeros = []
    intervals = np.linspace(0, 100, 500)
    for i in range(len(intervals) - 1):
        t1, t2 = intervals[i], intervals[i + 1]
        if y(t1, K, a, z) * y(t2, K, a, z) < 0:
            zero = root_scalar(y, args=(K, a, z), bracket=[t1, t2], method='bisect')
            if zero.converged:
                zeros.append(zero.root)
    return sorted(zeros)

def area_under_curve(t1, t2, K, a, z):
    integral, _ = quad(lambda t: max(y(t, K, a, z), 0), t1, t2)
    return integral

def encuentra_restriccion(K,a,pr):
    ceros = find_zeros(K, a, pr)
    if len(ceros) >= 2:
       t1, t2 = ceros[0], ceros[-1]
       _E2 = area_under_curve(t1, t2, K, a, pr)  # se calcula pero no se muestra aquí
    else:
       print("No se encontraron suficientes ceros para calcular el área.")
       sys.exit(1)
    return ceros[0],ceros[-1]

def calcula_restriccion(K,a,pr,t1,t2):
    Er=E_acum(K,a,t2)-E_acum(K,a,t1)
    E3=pr*(t2-t1)
    E2=Er-E3
    return Er,E2,E3

def esfuerzo_fijo(Epend,pr):
    return Epend/pr

def average_value(K, a, tx):
    integral, _ = quad(E, 0, tx, args=(K, a))
    average = integral / tx
    return average

#*=*=*=*=*=*=*=* Funciones auxiliares de graficación

def esfuerzo_instantaneo(t, a):
    # Usa K global (ver sección donde se asigna K)
    return 2 * K * a * t * np.exp(-a * t**2)

def esfuerzo_constante(t,pr):
    l=len(t)
    return np.full(l,pr)

def esfuerzo_acumulado(t,a):
    return K*(1-np.exp(-a * t**2))

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Defaults del proyecto testigo
Kp=212
pr=15
version="1.1"
name="NoName"
rr=False

# Limpia consola (Windows/Linux/Mac)
os.system('cls' if os.name == 'nt' else 'clear')

# Argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--version", required=False, help="version", action="store_true")
ap.add_argument("-k", "--esfuerzo", required=False, type=float, help="Esfuerzo total (PM)")
ap.add_argument("-p", "--pmax", required=False, type=float, help="Staff máximo")
ap.add_argument("-n", "--name", required=False, type=str, help="Nombre proyecto")
ap.add_argument("-r", "--restriccion", required=False, help="Calcula corrección por restricción", action="store_true")
ap.add_argument("--a4", required=False, help="Grafica y calcula también con a cuadruplicado (punto 8.c)", action="store_true")
args = vars(ap.parse_args())

if args['esfuerzo'] is not None:
   Kp=float(args['esfuerzo'])

if args['pmax'] is not None:
   pr=float(args['pmax'])

if args['restriccion']:
   rr=True
   print("Calcula proyecto con restricción de recursos pmax=%.1f" % (pr))

if args['version']:
   print("Programa %s version %s" % (sys.argv[0],version))
   sys.exit(0)

if args['name']:
   name=args['name']

#*=*=*=*=*=*=*=* Calibración con dataset histórico (punto 8.a)
t_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])         # Tiempo (meses)
E_data = np.array([8, 21, 25, 30, 25, 24, 17, 15, 11, 6])  # Staff instantáneo (personas)
df = pd.DataFrame(E_data, index=t_data)
print(df)

# K histórico para ajuste (integral / suma discreta)
K = np.sum(E_data)
print("El esfuerzo total del dataset histórico es K=%d PM" % (K))

# Ajuste de 'a' por mejor fit de la forma Rayleigh
popt, pcov = curve_fit(esfuerzo_instantaneo, t_data, E_data, p0=[0.1])
a_estimada = popt[0]
print(f"Parámetro a estimado (calibración): a={a_estimada:.4f}")

# Gráfico 1: datos históricos vs modelo suavizado (calibración)
t_fit = np.linspace(min(t_data), max(t_data), 200)
E_fit = esfuerzo_instantaneo(t_fit, a_estimada)
plt.figure()
plt.scatter(t_data, E_data, label='Datos históricos', zorder=3)
plt.plot(t_fit, E_fit, label='Modelo ajustado (a_cal)', zorder=2)
plt.xlabel('Tiempo (meses)')
plt.ylabel('Esfuerzo instantáneo p(t) [personas]')
plt.legend()
plt.title('Calibración con dataset histórico')
plt.show()

#*=*=*=*=*=*=*=* Proyecto testigo con K indicado (punto 8.a y 8.b)
K = Kp  # desde aquí, K global pasa a ser el del proyecto solicitado
print("\nProyecto '%s' con esfuerzo K=%.1f PM" % (name, K))

# Curva PNR con a_calibrado y K solicitado
t_fit = np.linspace(min(t_data), max(t_data), 200)
O_fit = esfuerzo_instantaneo(t_fit, a_estimada)

# Para comparar, también mostramos el modelo ajustado con K histórico
# (ya se graficó antes); ahora graficamos el del proyecto
plt.figure()
plt.scatter(t_data, E_data, label='Datos históricos', zorder=3)
plt.plot(t_fit, O_fit, label='PNR (K solicitado, a_cal)', zorder=2, color='blue')
plt.xlabel('Tiempo (meses)')
plt.ylabel('Esfuerzo instantáneo p(t) [personas]')
plt.legend()
plt.title('PNR para K solicitado vs datos históricos')
plt.show()

# Esfuerzo acumulado del proyecto con a_cal
t_fit = np.linspace(min(t_data), max(t_data), 200)
O_acum = esfuerzo_acumulado(t_fit, a_estimada)
plt.figure()
plt.plot(t_fit, O_acum, label='Esfuerzo acumulado E(t) con a_cal', color='blue')
plt.xlabel('Tiempo (meses)')
plt.ylabel('Esfuerzo acumulado E(t) [PM]')
plt.legend()
plt.title('Esfuerzo acumulado del proyecto (a_cal)')
plt.show()

# Planeamiento sin restricciones
gamma=0.9
tf,Ef = E_proyecto (K,a_estimada,gamma)
print("\nSolución sin restricciones (a_cal)")
print("\tEsfuerzo nominal (K)=%.1f PM" % (K))
print("\tTiempo para entrega tf@E=%.0f%%K = %.2f meses" % (gamma*100, tf))

tmax, pmax = find_maximum(K, a_estimada)
t_near_zero = find_near_zero(K, a_estimada, 1.0)
if t_near_zero is None:
    print("No se encontró un valor de t cercano a cero para p(t).")
    sys.exit(1)
Enz=E_acum(K,a_estimada,t_near_zero)-E_acum(K,a_estimada,tf)
pmed = average_value(K, a_estimada, tf)
prel = E(tf,K,a_estimada)
print("\tMáximo staff: pmax=%.2f personas en t=%.2f meses" % (pmax, tmax))
print("\tStaff promedio [0, tf]: pmed=%.2f personas" % (pmed))
print("\tStaff al release: prel=%.2f personas" % (prel))
print("\tTiempo residual tnz=%.2f meses, esfuerzo residual Enz=%.2f PM" % (t_near_zero, Enz))

#*=*=*=*=*=*=*=* Punto 8.c: usar a cuadruplicado (opcional con --a4)
if args['a4']:
    a4 = 4.0 * a_estimada
    print("\n[8.c] Análisis con a cuadruplicado: a4 = 4*a_cal = %.4f" % a4)

    # Curva instantánea con a4
    O_fit_a4 = esfuerzo_instantaneo(t_fit, a4)
    plt.figure()
    plt.scatter(t_data, E_data, label='Datos históricos', zorder=3)
    plt.plot(t_fit, O_fit,     label='PNR (K, a_cal)', zorder=2)
    plt.plot(t_fit, O_fit_a4,  label='PNR (K, a=4*a_cal)', zorder=2, linestyle='--')
    plt.xlabel('Tiempo (meses)')
    plt.ylabel('Esfuerzo instantáneo p(t) [personas]')
    plt.legend()
    plt.title('Comparación p(t): a_cal vs 4*a_cal (mismo K)')
    plt.show()

    # Acumulado con a4
    O_acum_a4 = esfuerzo_acumulado(t_fit, a4)
    plt.figure()
    plt.plot(t_fit, O_acum,    label='E(t) con a_cal')
    plt.plot(t_fit, O_acum_a4, label='E(t) con 4*a_cal', linestyle='--')
    plt.xlabel('Tiempo (meses)')
    plt.ylabel('Esfuerzo acumulado E(t) [PM]')
    plt.legend()
    plt.title('Esfuerzo acumulado: a_cal vs 4*a_cal')
    plt.show()

    tf4, _Ef4 = E_proyecto(K, a4, gamma)
    tmax4, pmax4 = find_maximum(K, a4)
    prel4 = E(tf4, K, a4)

    print("[8.c] Sin restricciones con a=4*a_cal")
    print("\tTiempo para entrega tf4@E=%.0f%%K = %.2f meses" % (gamma*100, tf4))
    print("\tMáximo staff pmax4=%.2f personas en t=%.2f meses" % (pmax4, tmax4))
    print("\tStaff al release (prel4)=%.2f personas" % (prel4))
    print("\tObservación: al cuadruplicar 'a', el pico es más alto y ocurre antes; "
          "para el mismo K, pmax aumenta ~x2 y tmax se reduce ~a la mitad, "
          "lo que puede ampliar la 'zona imposible' si el tope de recursos pr es bajo.")

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#*       Restricción de staff (opcional con -r, se deja igual)
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

if not rr:
   print("\nCálculo con restricción de recursos no fue requerido")
   sys.exit(0)
else:
   print("\nSe calcula con restricción de recursos requeridos pr=%.1f" % (pr))

if pr<prel:
    print("** Aviso ** Los recursos deben ser superiores a %.1f personas" % (prel))
    pr=round(prel+0.5)
    print("Se ajusta recursos mínimos a pr=%.1f" % (pr))

t1,t2 = encuentra_restriccion(K,a_estimada,pr)

if t2>tf:
    print("La restricción dura más que el proyecto, incrementar recursos")
    sys.exit(1)

Er,E2,E3 = calcula_restriccion(K,a_estimada,pr,t1,t2)
E1=E_acum(K,a_estimada,t1)
E4=E_acum(K,a_estimada,tf)-E_acum(K,a_estimada,t2)

print("\nSolución con restricciones proyecto %s" % (name))
print("\tEsfuerzo nominal (K)=%.1f PM" % (K))
print("\tTiempo para entrega (tf)=%.1f meses" % (tf))
print("\tLa restricción ocurre en [%.1f, %.1f] meses" % (t1,t2))
print("\tE1=%.1f PM  | Er=%.2f PM  | E3 (posible)=%.2f PM  | E2 (pendiente)=%.2f PM  | E4=%.1f PM"
      % (E1,Er,E3,E2,E4))

print("\tEtot=E1+E2+E3+E4=%.1f PM" % (E1+E2+E3+E4))
tx=esfuerzo_fijo(E2,pr)

print("\tTiempo agregado adicional tx=%.2f meses con pr=%.2f (Ex=%.2f PM)" % (tx,pr,pr*tx))
print("\tDuración total con restricción: %.1f meses" % (tf+tx))

# Gráfico de etapas con restricción
t_E1=np.linspace(0,t1,100)
t_E1_fit = esfuerzo_instantaneo(t_E1, a_estimada)

t_E2=np.linspace(t1,t2,100)
t_E2_fit=esfuerzo_instantaneo(t_E2, a_estimada)
t_E3_fit=esfuerzo_constante(t_E2,pr)

t_Ex = np.linspace(t2,t2+tx,100)
t_Ex_fit=esfuerzo_constante(t_Ex,pr)

t_E4=np.linspace(t2+tx,tf+tx,100)
t_tail=np.linspace(t2,tf,100)
t_E4_fit = esfuerzo_instantaneo(t_tail, a_estimada)

t_med = np.linspace(0,tf+tx,100)
t_med_fit=esfuerzo_constante(t_med,average_value(K,a_estimada,tf))
t_min = np.linspace(0,tf+tx,100)
t_min_fit=esfuerzo_constante(t_min,prel)

plt.figure()
plt.plot(t_E1, t_E1_fit, label='E1', color='blue')
plt.plot(t_E2, t_E2_fit, label='E2 (restricción)', linestyle=":", color='blue')
plt.plot(t_E2, t_E3_fit, label='E3 (disponible)', color='red')
plt.plot(t_Ex, t_Ex_fit, label='Ex (adicional)', color='green')
plt.plot(t_E4, t_E4_fit, label='E4', color='blue')
plt.plot(t_med, t_med_fit, label='media', linestyle="--", color='black')
plt.plot(t_min, t_min_fit, label='min', linestyle=":", color='black')
plt.xlabel('Tiempo (meses)')
plt.ylabel('Esfuerzo instantáneo (personas)')
plt.legend()
plt.title('Proyecto con restricción de recursos')
plt.show()
