#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 16:53:03 2025

@author: ale
SELECCION
"""
def rank(poblacion):                    # LA POBLACION DEBE ESTAR ORDENADA
    padre1=[]
    padre2=[]
    for i in range(0,len(poblacion),2):
        p1=poblacion[i]
        p2=poblacion[i+1]
        #print('padre1',p1)
        #print('padre2',p2)
        padre1.append(p1)
        padre2.append(p2)
    return padre1,padre2 
