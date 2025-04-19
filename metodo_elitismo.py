#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 17:08:25 2025

@author: ale
ELITISMO
"""

def elitismo(poblacion, aptitudes, n):
    # Asumiendo que poblacion y aptitudes están ordenadas de mejor a peor
    if len(poblacion) <= n:
        # Devolvemos toda la población (todos son élite)
        return poblacion.copy(), aptitudes.copy()
    else:
        # Devolvemos los n mejores
        return poblacion[:n].copy(), aptitudes[:n].copy()

