
import math

# DATOS
# El problema se modela con una Progresiin Geometrica, ya que el crecimiento es un factor multiplicativo constante cada año
P0 = 2500000            # Poblacion inicial (base 2023)
tasa = 0.03             # Tasa de crecimiento del 3%
razon = 1 + tasa        # Razon de la progresion geometrica (r)
ano_inicial = 2023

# --- a) FORMULA Y FUNCION DE LA PROGRESION GEOMETRICA ---
# La formula matematica es P(n) = P₀ * r^n
# La encapsulamos en una funcion para una implementacion limpia y reutilizable.

def calcular_poblacion_futura(n_anos):
    """
    Calcula la poblacion despues de 'n' años usando la formula de progresion geometrica.
    - n_anos (int): Numero de años transcurridos desde el año inicial.
    - Retorna (float): La población estimada.
    """
    return P0 * (razon ** n_anos)

print("--- SOLUCION DEL PROBLEMA DE CRECIMIENTO POBLACIONAL ---")
print("\na) Formula y Funcion:")
print(f"La formula matematica que modela el problema es: P(n) = {P0:,.0f} * ({razon})^n")
print("Esta formula se ha implementado en la funcion 'calcular_poblacion_futura(n)'.\n")

# --- b) CALCULO DE LA POBLACION EN 2030 ---
print("b) Poblacion en el 2030:")
anos_para_2030 = 2030 - ano_inicial
poblacion_en_2030 = calcular_poblacion_futura(anos_para_2030)
print(f"Para el 2030, han transcurrido {anos_para_2030} anos.")
print(f"La poblacion estimada sera de: {math.ceil(poblacion_en_2030):,.0f} personas.\n")

# --- c) AÑO EN QUE SE SUPERAN LOS 4 MILLONES ---
print("c) Ano en que la poblacion superara los 4 millones:")
poblacion_objetivo = 4000000
anos_necesarios = 0
poblacion_simulada = P0

while poblacion_simulada <= poblacion_objetivo:
    anos_necesarios += 1
    poblacion_simulada = calcular_poblacion_futura(anos_necesarios)

ano_final = ano_inicial + anos_necesarios
print(f"El primer ano en que la poblacion excedera los {poblacion_objetivo:,.0f} sera en {ano_final}.")
print(f"Poblacion estimada para {ano_final}: {math.ceil(poblacion_simulada):,.0f} personas.")