import os

CURRENT_DIGIT = "2"
#FOLDER = "digits_examples/"
FOLDER = "digits_training/"
START_IMAGE = 0

i = START_IMAGE

while True:
    while os.path.isfile(FOLDER + CURRENT_DIGIT +'/Untitled.png') == False:
        pass
    
    print("New file added")
    if os.path.isfile(FOLDER + CURRENT_DIGIT +'/'+ str(i) +'.png') == False:
        os.rename(FOLDER + CURRENT_DIGIT +'/Untitled.png', FOLDER + CURRENT_DIGIT +'/'+ str(i) +'.png')
        print("Renamed file Untitled.png to "+ str(i) + '.png')
    i += 1