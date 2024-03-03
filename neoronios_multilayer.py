import numpy as np
import random
import time
import multiprocessing

COEF_APRENDIZADO = 0.5


class Neoronio:
    def __init__(self, numeroSinapses, layer):
        self.sinapses = np.array([random.randint(0, 1) for i in range(numeroSinapses)])
        self.sinapses = np.concatenate(([1], self.sinapses))
        self.layer = layer
        self.s = 99
        self.vetorEntrada = []

    def calcularV(self):
        self.v = np.dot(self.sinapses, self.vetorEntrada)

    def funcaoAtivacao(self, v):
        self.y = (1/(1+np.exp(-COEF_APRENDIZADO*v)))

    def calcularErro(self, yDesejado):
        self.erro = yDesejado - self.y
    
    @staticmethod
    def atualizarSinapses(neoronios):
        for i in range(len(neoronios)):
            for j in range(len(neoronios[i])):
                neoronios[i][j].sinapses = (COEF_APRENDIZADO * neoronios[i][j].s * neoronios[i][j].vetorEntrada) + neoronios[i][j].sinapses
                
    
    @staticmethod
    def classificar(neoronios, dados):
        resultado = []
        for i in range(len(neoronios)):
            neoronios[i].calcularV(dados.vetorEntrada)
    
            neoronios[i].funcaoAtivacao(neoronios[i].v)
    
            resultado.append(neoronios[i].y)
        return resultado

def calcularErroMedioVetorEntrada(errosNeoronios):
    erroMedioVetorEntrada = 0

    for i in range(len(errosNeoronios)):
        erroMedioVetorEntrada += (errosNeoronios[i]**2)

    erroMedioVetorEntrada = erroMedioVetorEntrada/len(errosNeoronios)
    return erroMedioVetorEntrada


def calcularErroEpoca(errosMediosVetorEntrada):
    erroEpoca = 0

    for i in range(len(errosMediosVetorEntrada)):
        erroEpoca += errosMediosVetorEntrada[i]

    erroEpoca = erroEpoca/len(errosMediosVetorEntrada)
    return erroEpoca



def epoca(neoronios, dados):
    errosNeoronios = []
    for i in range(len(neoronios)):
        for j in range(len(neoronios[i])):
            if i == 0:
                neoronios[i][j].vetorEntrada = dados.vetorEntrada
                neoronios[i][j].calcularV()
                neoronios[i][j].funcaoAtivacao(neoronios[i][j].v)
            
            if i == len(neoronios) - 1:
                vetorEntrada = [i.y for i in neoronios[i-1]]
                neoronios[i][j].vetorEntrada = np.concatenate(([1], vetorEntrada))

                neoronios[i][j].calcularV()
                neoronios[i][j].funcaoAtivacao(neoronios[i][j].v)

                neoronios[i][j].calcularErro(dados.yDesejado[j])
                errosNeoronios.append(neoronios[i][j].erro)
            
            if i > 0 and i < len(neoronios) - 1:
                vetorEntrada = [i.y for i in neoronios[i-1]]
                neoronios[i][j].vetorEntrada = np.concatenate(([1], vetorEntrada))

                neoronios[i][j].calcularV()
                neoronios[i][j].funcaoAtivacao(neoronios[i][j].v)
                
    return errosNeoronios
            
def calcularSs(neoronios):
    for i in range(len(neoronios) - 1, -1, -1):
        for j in range(len(neoronios[i])):
            
            if i == len(neoronios) - 1:
                neoronios[i][j].s = neoronios[i][j].erro * (COEF_APRENDIZADO * neoronios[i][j].y * (1 - neoronios[i][j].y))

    
            else:
                somatorio = 0
                for k in range(len(neoronios[i+1])):
                    
                    somatorio =+ neoronios[i+1][k].s * neoronios[i+1][k].sinapses[j+1]
                    
                neoronios[i][j].s = (COEF_APRENDIZADO * neoronios[i][j].y * (1 - neoronios[i][j].y) * somatorio)
                
    
            
            
def treinar(neoronios, conjuntoTreino):
    
    start_time = time.time()
    erroEpoca = 1

    while (erroEpoca >= 0.00001):
        errosMediosVetorEntrada = []
        for i in range(len(conjuntoTreino)):
            errosNeoronios = epoca(neoronios, conjuntoTreino[i])
            calcularSs(neoronios)
            neoronios[0][0].atualizarSinapses(neoronios)
            errosMediosVetorEntrada.append(calcularErroMedioVetorEntrada(errosNeoronios))

        erroEpoca = calcularErroEpoca(errosMediosVetorEntrada)
        
        
        print("Erro da epoca: ", erroEpoca)
    end_time = time.time()
    print("Tempo Total de treinamento: ", end_time - start_time, "s")

def main():
    neoronios = [[Neoronio(2, 0)], [Neoronio(1, 1)],[Neoronio(1, 1)],[Neoronio(1, 1)]]
    neoronios[0][0].sinapses = [1,0,1]
    neoronios[1][0].sinapses = [1,1]
    #epoca(neoronios, Dados([1,0,1], 1))
    #calcularSs(neoronios)
    #neoronios[0][0].atualizarSinapses(neoronios)
    treinar(neoronios, [Dados([1,0,1], [1])])

    print(neoronios[1][0].sinapses)

if __name__ == "__main__":
    from dataTools import *
    main()
    