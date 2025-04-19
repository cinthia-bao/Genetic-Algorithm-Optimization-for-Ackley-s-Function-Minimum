#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 21:49:02 2025

@author: ale
"""

import numpy as np
import json
import os
import matplotlib.pyplot as plt
from PIL import Image  # Para crear el GIF
import glob  # Para manejar archivos de imagen

# PARÁMETROS
inicio = -15        # VALOR MÍNIMO DEL RANGO
fin = 30            # VALOR MÁXIMO DEL RANGO
a, b, c, d = 20, 0.2, 2*np.pi, 2  # PARÁMETROS FUNCIÓN ACKLEY

# FUNCIÓN DE ACKLEY
def fitness(x1, x2):
    return (
        a + np.exp(1) - a * np.exp(-b * np.sqrt((x1**2 + x2**2)/d)) - 
        np.exp((np.cos(c*x1) + np.cos(c*x2))/d)
    )

def binarios_a_decimales(binarios):
    return [int("".join(map(str, bits)), 2) for bits in binarios]

def graficar_generacion(datos, gen_idx, output_dir="generaciones"):
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    generacion = datos[gen_idx]
    poblacion = generacion["Poblacion"]
    gen_num = generacion["Generacion"]
    
    # Crear figura 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Crear malla para la superficie de Ackley
    x = np.linspace(inicio, fin, 100)
    y = np.linspace(inicio, fin, 100)
    x_grid, y_grid = np.meshgrid(x, y)
    z_grid = np.array([[fitness(x, y) for x, y in zip(row_x, row_y)] 
                      for row_x, row_y in zip(x_grid, y_grid)])
    
    # Graficar superficie con colores azul-amarillo
    ax.plot_surface(x_grid, y_grid, z_grid, cmap='coolwarm', alpha=0.6)
    
    # Procesar población
    corte = len(poblacion[0]) // 2
    x1_bin = [ind[:corte] for ind in poblacion]
    x2_bin = [ind[corte:] for ind in poblacion]
    
    x1_dec = binarios_a_decimales(x1_bin)
    x2_dec = binarios_a_decimales(x2_bin)
    
    step = (fin - inicio) / (2**len(poblacion[0][:corte]) - 1)
    x1_coord = [inicio + step * val for val in x1_dec]
    x2_coord = [inicio + step * val for val in x2_dec]
    z = [fitness(x1_coord[i], x2_coord[i]) for i in range(len(x1_coord))]
    
    # Graficar puntos de la generación
    ax.scatter(x1_coord, x2_coord, z, color='red', marker='o', 
              label=f'Generación {gen_num}', s=40)
    
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Fitness (Z)')
    ax.set_title(f'Población en Generación {gen_num}')
    ax.legend()
    
    # Guardar imagen
    filename = os.path.join(output_dir, f"gen_{gen_num:03d}.png")
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()
    
    return filename

def crear_gif(input_dir="generaciones", output_file="evolucion.gif"):
    # Obtener lista de imágenes ordenadas
    images = sorted(glob.glob(os.path.join(input_dir, "gen_*.png")))
    
    # Leer imágenes y crear GIF
    frames = [Image.open(image) for image in images]
    
    # Guardar como GIF
    frames[0].save(output_file, format='GIF', 
                  append_images=frames[1:],
                  save_all=True, 
                  duration=500,  # duración en ms
                  loop=0)  # 0 para loop infinito
    
    print(f"GIF creado: {output_file}")

def cargar_datos(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        return json.load(f)

# Archivo JSON
archivo_json = 'ackley.json'

try:
    datos = cargar_datos(archivo_json)
    
    # Crear imágenes para cada generación
    for gen_idx in range(len(datos)):
        print(f"Procesando generación {gen_idx}")
        graficar_generacion(datos, gen_idx)
    
    # Crear GIF animado
    crear_gif()
    
    print("Proceso completado: imágenes individuales y GIF creados")
    
except Exception as e:
    print(f"Error: {e}")

