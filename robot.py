import sys
from math import *
import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs


class Robot:
    def __init__(self, th, a) -> None:
        self.th = th
        self.a = a
        self.L = sum(a)
        self.EPSILON = .01
    def muestra_origenes(self, O, final=0):
        # Muestra los orígenes de coordenadas para cada articulación
        print('Origenes de coordenadas:')
        for i in range(len(O)):
            print('(O'+str(i)+')0\t= '+str([round(j,3) for j in O[i]]))
        if final:
            print('E.Final = '+str([round(j,3) for j in final]))

    def muestra_robot(self, O, obj):
        # Muestra el robot graficamente
        plt.figure()
        plt.xlim(-self.L, self.L)
        plt.ylim(-self.L, self.L)
        T = [np.array(o).T.tolist() for o in O]
        for i in range(len(T)):
            plt.plot(T[i][0], T[i][1], '-o', color=cs.hsv_to_rgb(i/float(len(T)),1,1))
        plt.plot(obj[0], obj[1], '*')
        plt.pause(0.0001)
        plt.show()
        #  input()
        plt.close()

    def cinematica_inversa(self):
        
