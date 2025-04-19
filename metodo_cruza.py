#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 17:03:27 2025

@author: ale
CRUZA
"""
import random

def cruza_uniforme(padre1, padre2):
    h1 = []
    h2 = []
    for i in range(len(padre1)):
        p1 = padre1[i]
        p2 = padre2[i]
        h1_val = []
        h2_val = []
        for j in range( len(p2) ):
            seleccion = random.choice([p1[j],p2[j]])
            if seleccion == p1[j]:
                h1_val.append(p1[j])
                h2_val.append(p2[j])
            else:
                h1_val.append(p2[j])
                h2_val.append(p1[j])
        h1.append(h1_val)
        h2.append(h2_val)
    return h1, h2