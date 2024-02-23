import os

CURRENT_DIGIT = "1"
i = 0 

while True:
    while os.path.isfile('digits_training/'+ CURRENT_DIGIT +'/Untitled.png') == False:
        pass
    print("New file added")
    if os.path.isfile('digits_training/'+ CURRENT_DIGIT +'/'+ str(i) +'.png') == False:
        os.rename('digits_training/'+ CURRENT_DIGIT +'/Untitled.png', 'digits_training/'+ CURRENT_DIGIT +'/'+ str(i) +'.png')
        print("Renamed file Untitle.png to "+ str(i) + '.png')
    i += 1