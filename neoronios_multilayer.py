import numpy as np
import random
import time

COEF_APRENDIZADO = 1


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
        self.y = 1 / (1 + np.exp(-COEF_APRENDIZADO * v))

        # if v > 0:
        #    self.y = 1
        # else:
        #    self.y = 0

    def calcularErro(self, yDesejado):
        self.erro = yDesejado - self.y

    @staticmethod
    def atualizarSinapses(neoronios):
        for i in range(len(neoronios)):
            for j in range(len(neoronios[i])):
                neoronios[i][j].sinapses = (
                    COEF_APRENDIZADO * neoronios[i][j].s * neoronios[i][j].vetorEntrada
                ) + neoronios[i][j].sinapses

    @staticmethod
    def classificar(neoronios, dados):
        resultado = []

        epoca(neoronios, dados)

        for i in range(len(neoronios[len(neoronios) - 1])):
            resultado.append(neoronios[len(neoronios) - 1][i].y)

        return resultado


def instanciarNeoronios(shape, n_entradas):
    neoronios = []
    t = []
    for i in range(shape[0]):
        t.append(Neoronio(n_entradas, 0))
    neoronios.append(t)

    for i in range(1, len(shape)):
        t = []
        for j in range(shape[i]):
            t.append(Neoronio(shape[i - 1], i))
        neoronios.append(t)

    return neoronios


def calcularErroMedioVetorEntrada(errosNeoronios):
    erroMedioVetorEntrada = 0

    for i in range(len(errosNeoronios)):
        erroMedioVetorEntrada += errosNeoronios[i] ** 2

    erroMedioVetorEntrada = erroMedioVetorEntrada / len(errosNeoronios)
    return erroMedioVetorEntrada


def calcularErroEpoca(errosMediosVetorEntrada):
    erroEpoca = 0

    for i in range(len(errosMediosVetorEntrada)):
        erroEpoca += errosMediosVetorEntrada[i]

    erroEpoca = erroEpoca / len(errosMediosVetorEntrada)
    return erroEpoca


def epoca(neoronios, dados):
    errosNeoronios = []
    for camada in range(len(neoronios)):
        for neoronio in range(len(neoronios[camada])):
            if camada == 0:  ## Primeira camada
                neoronios[camada][neoronio].vetorEntrada = dados.vetorEntrada
                neoronios[camada][neoronio].calcularV()
                neoronios[camada][neoronio].funcaoAtivacao(
                    neoronios[camada][neoronio].v
                )
                # print("y Primeira Camada: ", neoronios[camada][neoronio].y)
                # print("sinapses Primeira Camada: ", neoronios[camada][neoronio].sinapses)

            if camada == len(neoronios) - 1:  ## ultima camada
                vetorEntrada = [i.y for i in neoronios[camada - 1]]

                # print("vetorEntrada: ", vetorEntrada)
                neoronios[camada][neoronio].vetorEntrada = np.concatenate(
                    ([1], vetorEntrada)
                )
                # neoronios[camada][neoronio].vetorEntrada = dados.vetorEntrada

                neoronios[camada][neoronio].calcularV()
                neoronios[camada][neoronio].funcaoAtivacao(
                    neoronios[camada][neoronio].v
                )
                neoronios[camada][neoronio].calcularErro(dados.yDesejado[neoronio])
                # print(f"y do neuronio     {neoronio}: {neoronios[camada][neoronio].y}")
                # print(f"erro do neuronio  {neoronio}: {neoronios[camada][neoronio].erro}")
                errosNeoronios.append(neoronios[camada][neoronio].erro)

            if camada > 0 and camada < len(neoronios) - 1:  ## camadas escondidas
                vetorEntrada = [i.y for i in neoronios[camada - 1]]
                neoronios[camada][neoronio].vetorEntrada = np.concatenate(
                    ([1], vetorEntrada)
                )

                neoronios[camada][neoronio].calcularV()
                neoronios[camada][neoronio].funcaoAtivacao(
                    neoronios[camada][neoronio].v
                )

    return errosNeoronios


def calcularSs(neoronios):
    for camada in range(len(neoronios) - 1, -1, -1):
        for neoronio in range(len(neoronios[camada])):
            if camada == len(neoronios) - 1:
                neoronios[camada][neoronio].s = neoronios[camada][neoronio].erro * (
                    COEF_APRENDIZADO
                    * neoronios[camada][neoronio].y
                    * (1 - neoronios[camada][neoronio].y)
                )

            else:
                somatorio = 0
                for k in range(len(neoronios[camada + 1])):
                    somatorio = (
                        +neoronios[camada + 1][k].s
                        * neoronios[camada + 1][k].sinapses[neoronio + 1]
                    )

                neoronios[camada][neoronio].s = (
                    COEF_APRENDIZADO
                    * neoronios[camada][neoronio].y
                    * (1 - neoronios[camada][neoronio].y)
                    * somatorio
                )


def treinar(neoronios, conjuntoTreino):
    start_time = time.time()
    erroEpoca = 1

    while erroEpoca >= 0.00001:
        errosMediosVetorEntrada = []
        for i in range(len(conjuntoTreino)):
            errosNeoronios = epoca(neoronios, conjuntoTreino[i])
            calcularSs(neoronios)
            neoronios[0][0].atualizarSinapses(neoronios)
            errosMediosVetorEntrada.append(
                calcularErroMedioVetorEntrada(errosNeoronios)
            )

        erroEpoca = calcularErroEpoca(errosMediosVetorEntrada)

        print("Erro da epoca: ", erroEpoca)
    end_time = time.time()
    print("Tempo Total de treinamento: ", end_time - start_time, "s")


def main():
    N_DIGITOS = 1
    neoronios = instanciarNeoronios([N_DIGITOS, N_DIGITOS], 16384)
    #conjuntoTreino = carregarImagensTreino(2)
    #print(conjuntoTreino[0].vetorEntrada, conjuntoTreino[0].yDesejado)
    # conjuntoTreino = Dados([1, 0, 1], [1])

    # epoca(neoronios, conjuntoTreino[0])
    # calcularSs(neoronios)
    # neoronios[0][0].atualizarSinapses(neoronios)

    # epoca(neoronios, conjuntoTreino[0])
    # calcularSs(neoronios)
    # neoronios[0][0].atualizarSinapses(neoronios)

    #treinar(neoronios, conjuntoTreino)

    print(neoronios[1][0].sinapses)


if __name__ == "__main__":
    #from dataTools import *

    main()
