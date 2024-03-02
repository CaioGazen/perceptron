from matplotlib.image import imread
import numpy as np
import cv2 as cv
import pickle
import os

N_DIGITOS = 3

class Dados:
    def __init__(self, vetorEntrada, yDesejado):
        self.vetorEntrada = np.array(vetorEntrada)
        self.yDesejado = yDesejado

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

            resultados.append([dado, neoronios[0].classificar(neoronios, dado)])

            j += 1

        i += 1

    return resultados



def interpretarResultado(resultado):
    resultadoInterpretado = ""
    flag = 0
    for i in range(len(resultado)):
        if resultado[i] and flag != 0:
            resultadoInterpretado = resultadoInterpretado +","+str(i)
        
        if resultado[i] and flag == 0:
            resultadoInterpretado = str(i)
            flag = 1

        
    if resultadoInterpretado == "":
        resultadoInterpretado = "nenhum " 


    #indice = {
    #str([0, 0]): "nenhum ",
    #str([0, 1]): "   1   ",
    #str([1, 0]): "   0   ",
    #str([1, 1]): "  0,1  "
    #}

    return resultadoInterpretado


def compararResultados(resultados):
    print("  Valor Real | Classificacao | indice ")
    for i in range(len(resultados)):
        print("  ", interpretarResultado(resultados[i][0].yDesejado),
              "  |   ", interpretarResultado(resultados[i][1]), "   | ", i)


def salvar(obj, fileName):
    with open(fileName + '.pkl', 'wb') as outputFile:  # Overwrites any existing file.
        pickle.dump(obj, outputFile, pickle.HIGHEST_PROTOCOL)

def carregar(fileName):
    with open(fileName + '.pkl', 'rb') as inputFile:
        return pickle.load(inputFile)



def live(neoronios):
    
    
    def live_classificar():
        image = np.sum(img, 2)
        image = image.ravel()

        yDesejado = 0

        dado = Dados(image, yDesejado)
        resultado = neoronios[0].classificar(neoronios, dado)

        print(resultado)
        print(interpretarResultado(resultado))
    
    global LBDown
    LBDown = False
    
    def draw_circle(event, x, y, flags, param):
        global LBDown

        if event == cv.EVENT_LBUTTONDOWN: # check if mouse event is click
            LBDown = True

        if event == cv.EVENT_LBUTTONUP: # check if mouse event is click
            LBDown = False
            live_classificar()

        if LBDown == True:
            cv.circle(img, (x, y), 5, (0,0,0), -1) # draw filled circle with 100px radius


    img = np.full((128,128,3), 255, np.uint8)

    cv.namedWindow('image')
    cv.setMouseCallback('image',draw_circle)

    sair = False

    while(1): 
        cv.imshow('image',img)
        k = cv.waitKey(20) & 0xFF

        if k == 32:
            img = np.full((128,128,3), 255, np.uint8)

        elif k == 27:
            cv.destroyAllWindows()
            break
