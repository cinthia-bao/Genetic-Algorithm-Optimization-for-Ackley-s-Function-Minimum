#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis de convergencia del algoritmo genético
"""
import json
import os
from get_population import aptitude
import matplotlib.pyplot as plt

def leer_json(nombre_archivo):
    with open(nombre_archivo, "r") as f:
        datos = json.load(f)
    return datos

nombre_archivo = "ackley.json"
print(f"Usando archivo: {nombre_archivo}")

datos = leer_json(nombre_archivo)
ap_mejor_individuo = []
ap_promedio = []
mejor_z = []  # Para almacenar los mejores valores Z de cada generación

# Primera pasada: recolectar todos los valores Z para encontrar el máximo global
all_z_values = []
for gen in datos:
    poblacion = gen["Poblacion"]
    _, _, z_ordenado = aptitude(poblacion)
    all_z_values.extend(z_ordenado)

max_global = min(all_z_values) if all_z_values else 1.0  # Evitar división por cero

# Segunda pasada: calcular métricas normalizadas
for gen in datos:
    poblacion = gen["Poblacion"]
    _, aptitudes, z_valores = aptitude(poblacion)
    
    # Normalización usando max_global
    aptitudes_normalizadas = [round(max_global/z, 4) for z in z_valores]
    
    max_aptitud = max(aptitudes_normalizadas)
    aptitud_promedio = sum(aptitudes_normalizadas) / len(aptitudes_normalizadas)
    
    ap_mejor_individuo.append(max_aptitud)
    ap_promedio.append(aptitud_promedio)
    mejor_z.append(z_valores[0])  # Guardar el mejor Z real
import matplotlib.pyplot as plt
import seaborn as sns  # Para mejorar el estilo de las gráficas

# Configuración de estilo general
sns.set_theme(style="whitegrid", context="talk")

# Crear gráfica de aptitud
plt.figure(figsize=(12, 7))
plt.plot(
    ap_mejor_individuo, 'b-', label='Mejor aptitud', linewidth=2.5, marker='o', markersize=6
)
plt.plot(
    ap_promedio, 'r--', label='Aptitud promedio', linewidth=2.5, marker='s', markersize=6
)
plt.fill_between(
    range(len(ap_mejor_individuo)),
    ap_mejor_individuo,
    ap_promedio,
    color='gray',
    alpha=0.2,
    label='Rango entre mejor y promedio'
)
plt.xlabel("Generación", fontsize=14)
plt.ylabel("Aptitud Normalizada", fontsize=14)
plt.title("Evolución de la Aptitud en el Algoritmo Genético", fontsize=16, weight='bold')
plt.legend(loc="upper left", fontsize=12, frameon=True, shadow=True, fancybox=True)
plt.grid(True, alpha=0.4)

# Guardar la gráfica
ruta = os.path.join("/home/ale/META_H/MINIMOFUNCION", 'Aptitud_vs_generacion_mejorada.png')
plt.savefig(ruta, dpi=300, bbox_inches='tight')
plt.close()

# Crear gráfica para valores Z reales
plt.figure(figsize=(12, 7))
plt.plot(
    mejor_z, 'g-', label='Mejor valor Z', linewidth=2.5, marker='^', markersize=6
)
plt.axhline(
    y=min(mejor_z), color='purple', linestyle='--', linewidth=1.5,
    label=f"Mejor valor Z alcanzado: {min(mejor_z):.4f}"
)
plt.xlabel("Generación", fontsize=14)
plt.ylabel("Valor Z (Fitness Real)", fontsize=14)
plt.title("Evolución del Mejor Fitness (Valor Z)", fontsize=16, weight='bold')
plt.legend(loc="upper right", fontsize=12, frameon=True, shadow=True, fancybox=True)
plt.grid(True, alpha=0.4)

# Guardar la gráfica
ruta_z = os.path.join("/home/ale/META_H/MINIMOFUNCION", 'Fitness_vs_generacion_mejorada.png')
plt.savefig(ruta_z, dpi=300, bbox_inches='tight')
plt.close()

print(f"Gráficos mejorados guardados en:\n{ruta}\n{ruta_z}")
