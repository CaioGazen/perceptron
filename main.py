from matplotlib.image import imread
import numpy as np
import random
import os
import pickle

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


def carregarImagensTreino():
    conjuntoTreino = []
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
    return conjuntoTreino


def classificarTeste(neoronios):
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



def interpretarResultado(resultado):
    indice = {
    str([0, 0]): "nenhum ",
    str([0, 1]): "   1   ",
    str([1, 0]): "   0   ",
    str([1, 1]): "  0,1  "
    }
    return indice[str(resultado)]


def compararResultados(resultados):
    print("  Valor Real | Classificacao | indice ")
    for i in range(len(resultados)):
        print("  ", interpretarResultado(resultados[i][0].yDesejado),
              "  |   ", interpretarResultado(resultados[i][1]), "   | ", i)



def instanciarNeoronios():
    neoronios = []

    for i in range(N_DIGITOS):
        neoronios.append(Neoronio(16384))

    return neoronios



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

                #print(neoronios[j].sinapses)

            #print(errosNeoronios)
            errosMediosVetorEntrada.append(
                calcularErroMedioVetorEntrada(errosNeoronios))

        erroEpoca = calcularErroEpoca(errosMediosVetorEntrada)
        print("Erro da epoca: ", erroEpoca)


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
        print(interpretarResultado(resultado))

def salvar(obj, fileName):
    with open(fileName + '.pkl', 'wb') as outputFile:  # Overwrites any existing file.
        pickle.dump(obj, outputFile, pickle.HIGHEST_PROTOCOL)

def carregar(fileName):
    with open(fileName + '.pkl', 'rb') as inputFile:
        return pickle.load(inputFile)


def main():
    neoronios = instanciarNeoronios()
    sair = False

    while not sair:
        print("""
            Escolha uma das alternativas a baixo
                1 - Treinar rede neural
                2 - Classificar
                3 - Live classificar
                4 - Salvar
                5 - Carregar
                6 - Sair
        """)

        match input():
            case "1":
                conjuntoTreino = carregarImagensTreino()
                treinar(neoronios, conjuntoTreino)
            case "2":
                resultados = classificarTeste(neoronios)
                compararResultados(resultados)

            case "3":
                live(neoronios)

            case "4":
                salvar(neoronios, input("Digite o nome do aquivo a ser salvo: "))
                print("Arquivo salvo com sucesso")
            case "5":
                neoronios = carregar(input("Digite o nome do aquivo que deseja carregar: "))
                print("Arquivo carregado com sucesso")

            case "6":
                sair = True
            case _:
                print("alternativa invalida")


if __name__ == "__main__":
    main()