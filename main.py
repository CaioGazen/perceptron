import numpy as np
import random


COEF_APRENDIZADO = 0.5


class Neoronio:
    def __init__(self, numeroSinapses):
        self.sinapses = np.array([random.randint(0,1) for i in range(numeroSinapses)])

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
        self.sinapses = (COEF_APRENDIZADO * self.erro * vetorEntrada) + self.sinapses

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

doencas = ["gripe", "dengue", "catapora"]

sintomas = ["Tosse", "Congestao Nasal", "Febre", "Dor", "Manchas", "Nauseas", "Fraquesa", "Bolhas", "Coceira"]

conjuntoTreino = [
        Dados([1,1,1,1,1,0,0,1,0,0], [1, 0, 0]),
        Dados([1,0,0,1,1,1,1,1,0,0], [0, 1, 0]), 
        Dados([1,0,0,1,0,1,0,1,1,1], [0, 0, 1])
    ]



neoronios = [Neoronio(10), Neoronio(10), Neoronio(10)]

#neoronio[0].sinapses = np.array([0,0,1,1,1,0,0,0,0,0])
#neoronio[1].sinapses = np.array([1,1,1,1,1,0,0,0,0,0])
#neoronio[2].sinapses = np.array([0,0,0,0,0,1,1,1,1,1])
def treinar(neoronios, conjuntoTreino):

    erroEpoca = 1
    while(erroEpoca >= 0.00001): 
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
            errosMediosVetorEntrada.append(calcularErroMedioVetorEntrada(errosNeoronios))

        erroEpoca = calcularErroEpoca(errosMediosVetorEntrada)
        print(erroEpoca)

def dignosticar(neoronios, dados):
    for i in range(len(neoronios)):
        neoronios[i].calcularV(dados.vetorEntrada)

        neoronios[i].funcaoAtivacao(neoronios[i].v)

        if neoronios[i].y == 1:
            print("\n\n    O diagnostico do programa é: " + doencas[i])
            print("\n\n aperte qualquer tecla para continuar")
            input()



exit = False

while not exit:
    print("""
        Escolha uma das alternativas a baixo
            1 - treinar rede neural
            2 - fazer um diagnostico
            3 - sair
    """)

    match input():
        case "1":
            treinar(neoronios, conjuntoTreino)
        case "2":
            dados = [1]
            print("informe os sintomas apresentados pelo paciente.")
            for i in sintomas:
                print(i + "[0/1]:")
                dados.append(int(input()))
            dignosticar(neoronios, Dados(dados, 0))
        case "3": 
            exit = True
        case _:
            print("alternativa invalida")