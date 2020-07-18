# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 00:27:06 2020

@author: Mauricio Bolívar & Valentina Campos
"""


import random
import numpy as np
import sys
from matplotlib import pyplot as plt
np.set_printoptions(threshold=sys.maxsize)
cafe=np.zeros((100,100))

def estadoinicial(matriz):
    i=45
    while i<55:
        j=45
        while j<55:
            matriz[i][j]=1
            j+=1
        i+=1
        
def graficar(matriz,tiempo):
    fig, ax = plt.subplots() 
    ax.matshow(matriz, cmap ="gist_earth") 
  
    ax.set_title('Cafe en t='+str(tiempo)) 
    plt.show() 
    
def plotear(lista):
    plt.plot(lista)
    plt.ylabel('Entropia')
    plt.xlabel('Tiempo')
    plt.show()

def divisor(lista,fila,columna):
    r,h=lista.shape
    return (lista.reshape(h//fila,fila,-1,columna)
            .swapaxes(1,2)
            .reshape(-1,fila,columna))


def dividirmat (array):
    nueva=[]
    nueva.append(divisor(array,10,10))
    return nueva

def recorrerEstados(array):
    lista=[]
    for i in array: #matriz 10x10
        cantidad=0
        for j in i:
            cantidad=np.count_nonzero(j)
            if cantidad>0:
                lista.append(cantidad)
    return lista

def calculoprob(lista):
    proba=[]
    entrop=0
    for elemento in lista:
        prob=elemento/100
        proba.append(prob)
    a=0
    suma=0
    while a<len(proba):
        suma=suma+abs(proba[a]*np.log(proba[a]))
        a+=1
    entrop=suma
    return entrop
    
def simular(parametro,pasos):
    documento=open('Memoria.txt','w')
    a=1
    estadoinicial(cafe)
    graficar(cafe,0)
    while a<=pasos:
        n1=0
        while n1<len(parametro[1]): #recorrer cada fila
            n2=0
            while n2<len(parametro[1]): #recorrer cada columna
                if parametro[n1][n2]==1:
                    rng=random.randint(1,4) #uno de 4 numeros para que se mueva a una de cuatro celdas
                    if rng==1 and n1+1<len(parametro[1]) and parametro[n1+1][n2]!=1:
                        parametro[n1][n2]=0
                        parametro[n1+1][n2]=1
                        n2+=1
                    elif rng==2 and n1-1>=0 and parametro[n1-1][n2]!=1:
                        parametro[n1][n2]=0
                        parametro[n1-1][n2]=1
                        n2+=1
                    elif rng==3 and n2+1<len(parametro[1]) and parametro[n1][n2+1]!=1:
                        parametro[n1][n2]=0
                        parametro[n1][n2+1]=1
                        n2+=1
                    elif rng==4 and n2-1>=0 and parametro[n1][n2-1]!=1:
                        parametro[n1][n2]=0
                        parametro[n1][n2-1]=1
                        n2+=1
                    else:
                        n2+=1
                else:
                    n2+=1
            n1+=1
        for row in cafe:
            np.savetxt(documento,row)
        a+=1
    graficar(parametro,a-1)
    documento.close() 
    
               
def recorrer(itera): #lee el documento con todas las iteraciones y lo va extendiendo segun las que se pidan
    #recorre toda la matriz que guarda todas las matrices en el tiempo
    dato=np.loadtxt('Memoria.txt').reshape((100*itera),100)
    nivel=0
    recorrex=0
    cutoff=100
    entrop=[]
    while nivel<itera:
        n1=0
        while recorrex<cutoff:
            n2=0
            while n2<100:
                cafe[n1][n2]=dato[recorrex][n2]
                n2=n2+1
            n1=n1+1
            recorrex=recorrex+1
        ent=calculoprob(recorrerEstados(dividirmat(cafe)))
        entrop.append(ent)
        recorrex=cutoff
        cutoff=cutoff+100
        nivel=nivel+1
    graficar(cafe,itera)
    plotear(entrop)
"Programa Principal, recordar que los pasos y las iteraciones deben ser iguales"
cant=int(input('Iteraciones: '))
simular(cafe,cant)   
recorrer(cant) 
