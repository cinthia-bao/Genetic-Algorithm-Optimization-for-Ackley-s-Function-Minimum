#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 15:41:14 2025

@author: ale
"""

import random
import numpy as np
import json
import os

# CARACTERÍSTICA DE LA POBLACIÓN
tamano = 100         # NUMERO DE INDIVIDUOS
dig = 16            # DIGITOS DEL INDIVIDUO
inicio = -15        # VALOR MINIMO DEL RANGO
fin = 30            # VALOR MAXIMO DEL RANGO

# PARAMETROS DE LA FUNCION DE ACKLEY
a, b, c, d = 20, 0.2, 2*np.pi, 2

# FUNCION DE ACKLEY
def fitness(x1, x2):
    return (
        a + np.exp(1) - a * np.exp(-b * np.sqrt((x1**2 + x2**2)/d)) - 
        np.exp((np.cos(c*x1) + np.cos(c*x2))/d)
    )


# FUNCION PARA INICIAR LA POBLACION

def initialize_population(tamano, dig, min_val, max_val):
    num_bin = set()  # Usamos un set para evitar duplicados
    while len(num_bin) < tamano:  
        # Generamos una lista de bits en lugar de un string
        binario = tuple(random.randint(0, 1) for _ in range(dig))
        num_bin.add(binario)  # Añadimos al set (sin duplicados)
    # Convertimos el set a una lista de listas para la salida
    num_bin = [list(binario) for binario in num_bin]
    return num_bin


# SE CREA LA PRIMERA GENERACION
population = initialize_population(tamano,dig,inicio,fin)

# FUNCION PARA LA APTITUD Y EL ORDENAMIENTO
def aptitude(population):
    """
    Función que calcula la aptitud y ordena la poblacion conforme su aptitud,
    la ordena de mayor a menor.
    """
    # TOMA 2 NUMEROS EN BINARIO
    corte =int (len(population[0])/2)
    x1,x2 = [],[]
    for i in range(len(population)):
        individuo = population[i]
        x1_value = individuo[:corte]
        x2_value = individuo[corte:]
        x1.append(x1_value)
        x2.append(x2_value)
    # COVIERTE DE BINARIOS A DECIMALES
    def binarios_a_decimales(binarios):
        decimales = [int("".join(map(str, bits)), 2) for bits in binarios]
        return decimales
    x1_decimales = binarios_a_decimales(x1)
    x2_decimales = binarios_a_decimales(x2)
    # CONVIERTE EN UN VALOR DE ENTRE -15 Y 30
    step = (fin - inicio) /255
    x1_coord = [inicio + step * i for i in x1_decimales]
    x2_coord = [inicio + step * i for i in x2_decimales]
    # SE CALCULA EL VALOR DE Z
    z = [float(fitness(x1_coord[i], x2_coord[i])) for i in range(len(x1_coord))]
    # SE CALCULA LA APTITUD
    z_min = min(z)
    aptitud = [z_min/z[i] for i in range(len(z))]
    # ORGANIZACION DE Z Y POBLACION EN FUNCION DE LA APTITUD
    z_ordenado = [z for _, z in sorted(zip(aptitud, z), reverse=True)]
    population_ordenado = [population for _, population in sorted(zip(aptitud, population), \
                                                                  reverse=True)]
    aptitud_ordenada = sorted(aptitud, reverse=True)
    return population_ordenado, aptitud_ordenada, z_ordenado


population_sort, aptitud_sort, z_value = aptitude(population)

# FUNCION PARA GUARDAR LA POBLACIONEN UN ARCHIVO JSON
def guardar_poblacion(poblacion, archivo="poblacion_inicial.json"):
    if not os.path.exists(archivo):  # Verificar si el archivo no existe
        datos = {"poblacion": poblacion}
        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)
        print("Población y aptitud guardadas en", archivo)
    else:
        print("El archivo ya existe, no se guardaron cambios.")

guardar_poblacion(population)

# FUNCION PARA GUARDAR LAS GENERACIONES

def actualizar_json(nombre_archivo, generacion, poblacion):
    """
    Actualiza un archivo JSON con nuevas generaciones y poblaciones.

    :param nombre_archivo: Nombre del archivo JSON.
    :param generacion: Número de la generación.
    :param poblacion: Lista de listas representando la población.
    """
    datos = []
    
    # Verificar si el archivo existe y no está vacío
    if os.path.exists(nombre_archivo) and os.path.getsize(nombre_archivo) > 0:
        try:
            with open(nombre_archivo, "r") as f:
                datos = json.load(f)  # Cargar los datos previos
        except json.JSONDecodeError:
            print(f"⚠️ Archivo {nombre_archivo} no contiene un JSON válido. Será sobrescrito.")
            datos = []  # Reiniciar datos si el JSON es inválido
    # Agregar la nueva generación
    nueva_generacion = {
        "Generacion": generacion,
        "Poblacion": poblacion
    }
    datos.append(nueva_generacion)  # Añadir a la lista de datos
    # Guardar el JSON actualizado
    with open(nombre_archivo, "w") as f:
        json.dump(datos, f, indent=4)
    print(f" Generación {generacion} agregada a {nombre_archivo}")


