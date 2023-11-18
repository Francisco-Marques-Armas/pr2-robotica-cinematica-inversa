import sys
from math import *
import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs

class Robot:
    def __init__(self, tipos, th, a, objetivo) -> None:
        self.tipos = tipos
        self.th = th
        self.a = a
        self.objetivo = objetivo
        self.L = sum(a)
        self.EPSILON = .01
        self.dist = float("inf")
        self.prev = 0.
        self.numero_puntos = len(th)
        self.O = self.cin_dir(self.th,self.a)

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

    def cin_dir(self, th, a):
        #Sea 'th' el vector de thetas
        #Sea 'a'  el vector de longitudes
        T = np.identity(4)
        o = [[0,0]]
        for i in range(len(th)):
            T = np.dot(T, self.matriz_T(0,th[i],a[i],0))
            tmp=np.dot(T,[0,0,0,1])
            o.append([tmp[0],tmp[1]])
        return o

    def matriz_T(self, d, th, a, al):
        # Calcula la matriz T (ángulos de entrada en radianes)
        
        return [ [cos(th), -sin(th)*cos(al),  sin(th)*sin(al), a*cos(th)]
                ,[sin(th),  cos(th)*cos(al), -sin(al)*cos(th), a*sin(th)]
                ,[      0,          sin(al),          cos(al),         d]
                ,[      0,                0,                0,         1]
                ]

    def normalizar_radianes(self, angulo):
        # Entre -pi y pi
        angulo_normalizado = angulo % (2 * pi)
        # Si es más que pi, restamos 2pi
        if angulo_normalizado > pi:
            angulo_normalizado -= 2 * pi
        return angulo_normalizado
    
    def cinematica_inversa(self):
        iteracion = 1
        while (self.dist > self.EPSILON and abs(self.prev-self.dist) > self.EPSILON/100.):
            self.prev = self.dist
            O=[self.cin_dir(self.th,self.a)]
            # Para cada combinación de articulaciones:
            for i in range(len(self.th)):
                # cálculo de la cinemática inversa:
                punto_final = O[i][-1]
                articulacion = O[i][self.numero_puntos - i - 1]
                if (self.tipos[self.numero_puntos - i - 1] == 'R'):
                    # Calculamos tangente 1: ángulo entre vector articulacion y punto final
                    diferencia_y_art_final = punto_final[1] - articulacion[1]
                    diferencia_x_art_final = punto_final[0] - articulacion[0]
                    angulo_art_final = atan2(diferencia_y_art_final, diferencia_x_art_final)
                    # Calculamos tangente 2: ángulo entre vector articulacion y punto objetivo
                    diferencia_y_art_obj = self.objetivo[1] - articulacion[1]
                    diferencia_x_art_obj = self.objetivo[0] - articulacion[0]
                    angulo_art_obj = atan2(diferencia_y_art_obj, diferencia_x_art_obj)
                    # Calculamos la diferencia entre los dos ángulos
                    angulo_diferencia = angulo_art_obj - angulo_art_final
                    # Normalizamos el ángulo
                    angulo_diferencia = self.normalizar_radianes(angulo_diferencia)
                    self.th[self.numero_puntos - 1 - i] += angulo_diferencia
                elif (self.tipos[self.numero_puntos - i - 1] == 'P'):
                    # calcular a
                    print("Error: articulación prismática no implementada.")
                    # Sumar todos los theta previos
                    suma_theta = 0
                    for j in range(self.numero_puntos - i - 1):
                        suma_theta += self.th[j]
                    # Normalizar el ángulo
                    suma_theta = self.normalizar_radianes(suma_theta)
                    # Calcular vector articulacion
                    vector_articulacion = [cos(suma_theta), sin(suma_theta)]
                    # Calcular vector objetivo
                    vector_objetivo = [self.objetivo[0] - articulacion[0], self.objetivo[1] - articulacion[1]]
                    # Sumar producto escalar de los dos vectores
                    nueva_d = np.dot(vector_articulacion, vector_objetivo)
                    # Sumar al conjunto a
                    self.a[self.numero_puntos - 1 - i] += nueva_d
                else:
                    print("Error: tipo de articulación no reconocido.")
                    exit()
                # Calculamos tangente 1: ángulo entre vector articulacion y objetivo y eje x
                # si es una prismática, no se modifica el ángulo

                O.append(self.cin_dir(self.th,self.a))
            self.dist = np.linalg.norm(np.subtract(self.objetivo,O[-1][-1]))
            print ("\n- Iteracion " + str(iteracion) + ':')
            self.muestra_origenes(O[-1])
            self.muestra_robot(O, self.objetivo)
            print ("Distancia al objetivo = " + str(round(self.dist,5)))
            iteracion+=1
            O[0]=O[-1]
        if self.dist <= self.EPSILON:
            print ("\n" + str(iteracion) + " iteraciones para converger.")
        else:
            print ("\nNo hay convergencia tras " + str(iteracion) + " iteraciones.")
            print ("- Umbral de convergencia epsilon: " + str(self.EPSILON))
            print ("- Distancia al objetivo:          " + str(round(self.dist,5)))
            print ("- Valores finales de las articulaciones:")
        for i in range(len(self.th)):
            print ("  theta" + str(i+1) + " = " + str(round(self.th[i],3)))
        for i in range(len(self.th)):
            print ("  L" + str(i+1) + "     = " + str(round(self.a[i],3)))
                    