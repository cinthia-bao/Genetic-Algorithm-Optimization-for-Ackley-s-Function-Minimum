#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 17:06:15 2025

@author: ale
"""

import json
from collections import Counter
from get_population import actualizar_json, aptitude
# IMPORT METHODS
from metodo_seleccion import rank
from metodo_cruza import cruza_uniforme
from metodo_elitismo import elitismo
from metodo_mutacion import bit_flip


def cargar_poblacion(archivo="poblacion_inicial.json"):
    with open(archivo, "r") as f:
        datos = json.load(f)
    return datos["poblacion"]

def hay_muchos_clones(poblacion, max_clones=25):
    individuos_tuplas = [tuple(ind) for ind in poblacion]
    conteo = Counter(individuos_tuplas)
    for ind, count in conteo.items():
        if count > max_clones:
            print(f"¡Alerta! Individuo clonado {count} veces (límite: {max_clones})")
            return True
    return False

diferencia = .35
mejor_individuo = [] 
ap_mejor_individuo = []
ap_prom = []
poblacion = cargar_poblacion()
delta = 100
i = 0
actualizar_json('ackley.json', i, poblacion)

while delta > diferencia:
    # Verificar clones antes de comenzar la generación
    if hay_muchos_clones(poblacion):
        print("¡Demasiados clones! Deteniendo la ejecución.")
        break
    
    print(f'######################## GENERACION {i} #########################')
    print('******************* HACIENDO SELECCION RANK ************************')

    padre1_al_p, padre2_al_p = rank(poblacion)

    print('******************* HACIENDO CRUZA DE UN CORTE ************************')
    h1_alp_1c, h2_alp_1c = cruza_uniforme(padre1_al_p, padre2_al_p)

    print('******************* HACIENDO MUTACION *****************************')
    padre1_al_p, padre2_al_p, h1_alp_1c, h2_alp_1c = \
        bit_flip(padre1_al_p, padre2_al_p, h1_alp_1c, h2_alp_1c, 50)

    print('***************** HACEINDO ELITISMO *******************')
    
    valt = padre1_al_p + padre2_al_p + h1_alp_1c + h2_alp_1c
    population_ordenado, aptitud_ordenada, z_ordenado = aptitude(valt)
    poblacion, aptitud = elitismo(population_ordenado, aptitud_ordenada, len(poblacion))
    poblacion = list(poblacion)
    aptitud = list(aptitud)
    
    # Obtener el mejor individuo y su aptitud
    mejor_idx = aptitud.index(max(aptitud))
    mejor_individuo = poblacion[mejor_idx]
    mejor_ap = aptitud[mejor_idx]
    aptitud_promedio = sum(aptitud) / len(aptitud)
    print(aptitud_promedio)
    delta = abs(mejor_ap - aptitud_promedio)
    i += 1
    actualizar_json('ackley.json', i, poblacion)
    # Verificar clones después de actualizar la población
    if hay_muchos_clones(poblacion):
        break

print("Proceso finalizado.")