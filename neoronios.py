import numpy as np
import random
import time

COEF_APRENDIZADO = 0.5


class Neoronio:
    def __init__(self, numeroSinapses):
        self.sinapses = np.array([random.randint(0, 1) for i in range(numeroSinapses)])
        self.sinapses = np.concatenate(([1], self.sinapses))

    def calcularV(self, vetorEntrada):
        self.v = np.dot(self.sinapses, vetorEntrada)

    def funcaoAtivacao(self, v):
        self.y = (1/(1+np.exp(-COEF_APRENDIZADO*v)))
        # if v > 0:
        #     self.y = 1
        # else:
        #     self.y = 0

    def calcularErro(self, yDesejado):
        self.erro = yDesejado - self.y

    def atualizarSinapses(self, vetorEntrada):
        self.sinapses = (COEF_APRENDIZADO * self.erro *
                         vetorEntrada) + self.sinapses

    @staticmethod
    def classificar(neoronios, dados):
        resultado = []
        for i in range(len(neoronios)):
            neoronios[i].calcularV(dados.vetorEntrada)
    
            neoronios[i].funcaoAtivacao(neoronios[i].v)
    
            resultado.append(neoronios[i].y)
        return resultado

def instanciarNeoronios(shape, n_entradas):
    t =[]
    for i in range(shape[0]):
        t.append(Neoronio(n_entradas))
    return t

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


def treinar(neoronios, conjuntoTreino):
    start_time = time.time()
    erroEpoca = 1
    while (erroEpoca >= 0.00001):
        errosMediosVetorEntrada = []
        for i in range(len(conjuntoTreino)):
            errosNeoronios = []
            for j in range(len(neoronios)):

                neoronios[j].calcularV(conjuntoTreino[i].vetorEntrada)

                neoronios[j].funcaoAtivacao(neoronios[j].v)

                neoronios[j].calcularErro(conjuntoTreino[i].yDesejado[j])
                errosNeoronios.append(neoronios[j].erro)

                neoronios[j].atualizarSinapses(conjuntoTreino[i].vetorEntrada)

                #print(neoronios[j].sinapses)

            #print(errosNeoronios)
            errosMediosVetorEntrada.append(
                calcularErroMedioVetorEntrada(errosNeoronios))

        erroEpoca = calcularErroEpoca(errosMediosVetorEntrada)
        print("Erro da epoca: ", erroEpoca)
    end_time = time.time()
    print("Tempo Total de treinamento: ", end_time - start_time, "s")