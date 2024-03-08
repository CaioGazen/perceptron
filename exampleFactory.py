import numpy as np
import os
import cv2 as cv
import matplotlib.image




# Create a black image, a window and bind the function to window
global img, LBDown, FOLDER, CURRENT_DIGIT, currentImage

img = np.full((128,128,3), 255, np.uint8)

LBDown = False
currentImage = 0

def save():
    global img, LBDown, FOLDER, CURRENT_DIGIT, currentImage

    while (1):
        if not os.path.isfile(FOLDER + CURRENT_DIGIT +'/'+ str(currentImage) +'.png'):
            matplotlib.image.imsave(FOLDER + CURRENT_DIGIT +'/'+ str(currentImage) +'.png', img)
            print("saved image to "+ str(currentImage) + '.png')
            currentImage+= 1
            break

        currentImage+= 1


# create function to draw circle on mouse click
def draw_circle(event, x, y, flags, param):
    global LBDown, img

    if event == cv.EVENT_RBUTTONDOWN:
        img = np.full((128,128,3), 255, np.uint8)
    
    if event == cv.EVENT_LBUTTONDOWN: # check if mouse event is click
        LBDown = True

    if event == cv.EVENT_LBUTTONUP: # check if mouse event is click
        LBDown = False

    if LBDown:
        cv.circle(img, (x, y), 5, (0,0,0), -1) # draw filled circle with 100px radius
        

def main():
    global img, LBDown, FOLDER, CURRENT_DIGIT

    def chooseFolder():
        global img, LBDown, FOLDER, CURRENT_DIGIT
        match input("""
                1 - trainig
                2 - examples

                """):

            case "1":
                FOLDER = "digits_training/"
            case "2":
                FOLDER = "digits_examples/"
            case _:
                print("alternativa invalida")
                chooseFolder()

    chooseFolder()
    CURRENT_DIGIT = str(input("Digit: "))
    
    # create cv2 window and bind callback
    cv.namedWindow(str(CURRENT_DIGIT))
    cv.setMouseCallback(str(CURRENT_DIGIT),draw_circle)

    while(1): 
        cv.imshow(str(CURRENT_DIGIT),img)
        k = cv.waitKey(20) & 0xFF

        if k == 32:
            save()
            img = np.full((128,128,3), 255, np.uint8)
        elif k == 27:
            break
    
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()