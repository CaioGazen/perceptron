from matplotlib.image import imread
import numpy as np
import random
import os
import timeit
from neoronios_multilayer import *
from dataTools import *

N_DIGITOS = 1
N_CAMADAS = 3

def instanciarNeoronios():
    neoronios = [[] for i in range(N_CAMADAS)]

    for i in range(N_DIGITOS):
        neoronios[0].append(Neoronio(16384, 0))

    for i in range(1):
        for j in range(N_DIGITOS):
            neoronios[1].append(Neoronio(N_DIGITOS, i))

    for i in range(1):
        for j in range(N_DIGITOS):
            neoronios[N_CAMADAS - 1].append(Neoronio(N_DIGITOS, i))
    
    return neoronios


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

        match input("Escolha uma opção: "):
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