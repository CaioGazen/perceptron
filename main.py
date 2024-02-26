from matplotlib.image import imread
import numpy as np
import random
import os

COEF_APRENDIZADO = 0.5

N_DIGITOS = 2


class Neoronio:
    def __init__(self, numeroSinapses):
        self.sinapses = np.array([random.randint(0, 1)
                                 for i in range(numeroSinapses)])

    def calcularV(self, vetorEntrada):
        self.v = np.dot(self.sinapses, vetorEntrada)

    def funcaoAtivacao(self, v):
        if v > 0:
            self.y = 1
        else:
            self.y = 0

    def calcularErro(self, yDesejado):
        self.erro = yDesejado - self.y

    def atualizarSinapses(self, vetorEntrada):
        self.sinapses = (COEF_APRENDIZADO * self.erro *
                         vetorEntrada) + self.sinapses


class Dados:
    def __init__(self, vetorEntrada, yDesejado):
        self.vetorEntrada = np.array(vetorEntrada)
        self.yDesejado = yDesejado


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


conjuntoTreino = []


def carregarImagensTreino():
    i = 0
    while os.path.exists('digits_training/' + str(i)) and i < N_DIGITOS:
        print('digits_training/' + str(i))
        path = 'digits_training/' + str(i) + '/'

        yDesejado = [0 for k in range(N_DIGITOS)]
        yDesejado[i] = 1

        j = 0
        while os.path.isfile(path + str(j) + '.png'):
            image = imread(path + str(j) + '.png')
            image = np.sum(image, 2)
            image = image.ravel()

            conjuntoTreino.append(Dados(image, yDesejado))

            j += 1

        i += 1


def classificarTeste():
    resultados = []

    i = 0
    while os.path.exists('digits_examples/' + str(i)) and i < N_DIGITOS:
        path = 'digits_examples/' + str(i) + '/'

        yDesejado = [0 for k in range(N_DIGITOS)]
        yDesejado[i] = 1

        j = 0
        while os.path.isfile(path + str(j) + '.png'):
            image = imread(path + str(j) + '.png')
            image = np.sum(image, 2)
            image = image.ravel()

            dado = Dados(image, yDesejado)

            resultados.append([dado, classificar(neoronios, dado)])

            j += 1

        i += 1

    return resultados


teste = {
    str([0, 0]): "nenhum ",
    str([0, 1]): "   1   ",
    str([1, 0]): "   0   ",
    str([1, 1]): "  0,1  "
}


def compararResultados(resultados):
    print("  Valor Real | Classificacao | indice ")
    for i in range(len(resultados)):
        print("  ", teste[str(resultados[i][0].yDesejado)],
              "  |   ", teste[str(resultados[i][1])], "   | ", i)


neoronios = [Neoronio(16384), Neoronio(16384)]

# neoronio[0].sinapses = np.array([0,0,1,1,1,0,0,0,0,0])
# neoronio[1].sinapses = np.array([1,1,1,1,1,0,0,0,0,0])
# neoronio[2].sinapses = np.array([0,0,0,0,0,1,1,1,1,1])


def treinar(neoronios, conjuntoTreino):

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

                print(neoronios[j].sinapses)

            print(errosNeoronios)
            errosMediosVetorEntrada.append(
                calcularErroMedioVetorEntrada(errosNeoronios))

        erroEpoca = calcularErroEpoca(errosMediosVetorEntrada)
        print(erroEpoca)


def classificar(neoronios, dados):
    resultado = []
    for i in range(len(neoronios)):
        neoronios[i].calcularV(dados.vetorEntrada)

        neoronios[i].funcaoAtivacao(neoronios[i].v)

        resultado.append(neoronios[i].y)
    return resultado


def live(neoronios):
    sair = False
    while not sair:
        while not os.path.isfile("live.sig"):
            pass

        os.remove("live.sig")

        image = imread("live.png")
        image = np.sum(image, 2)
        image = image.ravel()

        yDesejado = 0

        dado = Dados(image, yDesejado)

        resultado = classificar(neoronios, dado)
        print(resultado)
        print(teste[str(resultado)])


sair = False

while not sair:
    print("""
        Escolha uma das alternativas a baixo
            1 - treinar rede neural
            2 - classificar
            4 - live classificar
            3 - sair
    """)

    match input():
        case "1":
            carregarImagensTreino()
            treinar(neoronios, conjuntoTreino)
        case "2":
            resultados = classificarTeste()
            compararResultados(resultados)

        case "3":
            sair = True

        case "4":
            live(neoronios)
        case _:
            print("alternativa invalida")
