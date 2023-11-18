#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Robótica Computacional - 
# Grado en Ingeniería Informática (Cuarto)
# Práctica: Resolución de la cinemática inversa mediante CCD
#           (Cyclic Coordinate Descent).

import sys # leer fichero
from math import *
import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs
from robot import Robot

EPSILON = .01
tipos = []
th=[]
a =[]
restricciones = []
L = sum(a) # variable para representación gráfica

#plt.ion() # modo interactivo

# introducción del punto para la cinemática inversa
if len(sys.argv) != 4:
  sys.exit("Número de argumentos incorrecto. Modo de uso: " + 
           "python " + sys.argv[0] + " fichero_entrada x y")
objetivo=[float(i) for i in sys.argv[2:]]

# Lectura del fichero
fichero = open(sys.argv[1], "r")
lineas = fichero.readlines()
for linea in lineas:
  if linea[0] != '#':
    #print(linea)
    linea = linea.split()
    # tipo de articulación
    tipos.append(linea[0])
    # theta
    th.append(float(linea[1]))
    # a
    a.append(float(linea[2]))
    restricciones.append(float(linea[3]))
    if (tipos[-1] == 'R'):
      # theta y restricción a radianes
      th[-1] = th[-1]*pi/180
      restricciones[-1] = restricciones[-1]*pi/180

    
fichero.close()
robot = Robot(tipos, th,a,objetivo)
O=robot.cin_dir(th,a)
#O=zeros(len(th)+1) # Reservamos estructura en memoria
 # Calculamos la posicion inicial
print ("- Posicion inicial:")
robot.muestra_origenes(O)
robot.cinematica_inversa()