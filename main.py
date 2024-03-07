from matplotlib.image import imread
import numpy as np
import random
import os
import timeit
from neoronios import *
from dataTools import *

N_DIGITOS = 3

def main():
    neoronios = instanciarNeoronios([N_DIGITOS, N_DIGITOS], 16384)  
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
                conjuntoTreino = carregarImagensTreino(N_DIGITOS)
                treinar(neoronios, conjuntoTreino)
            case "2":
                resultados = classificarTeste(neoronios, N_DIGITOS)
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