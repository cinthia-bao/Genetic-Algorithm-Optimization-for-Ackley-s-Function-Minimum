#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 17:04:42 2025

@author: ale
"""
import random

def bit_flip(p1,p2,h1,h2, porcentaje):
    total_ = [p1,p2,h1,h2]
    indiv_ = len(p1)+len(p2)+len(h1)+len(h2)
    ind = int(porcentaje*indiv_/100)
    for i in range(ind):
        indicelista =random.randint(0,len(total_)-1)
        lista_escogida = total_[indicelista]
        indice = random.randint(0,len(lista_escogida)-1)
        mutante = lista_escogida[indice]
        mutante = list(mutante)
        gen_ind = random.randint(0,len(mutante)-1)
        gen_mutante = mutante[gen_ind]
        if gen_mutante ==0:
            mutante[gen_ind] = 1
        else :
            mutante[gen_ind] = 0
        mutante = [int(x) for x in mutante]
        lista_escogida[indice]=list(mutante)
        total_[indicelista]=lista_escogida
    p1,p2,h1,h2=total_[0],total_[1],total_[2],total_[3]
    return p1,p2,h1,h2