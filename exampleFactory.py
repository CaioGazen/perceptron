from matplotlib.image import imread
import numpy as np
import os
import cv2 as cv
import matplotlib.image

CURRENT_DIGIT = "1"
#FOLDER = "digits_examples/"
FOLDER = "digits_training/"

# Create a black image, a window and bind the function to window
img = np.full((128,128,3), 255, np.uint8)


global LBDown
LBDown = False

def save():

    matplotlib.image.imsave(FOLDER + CURRENT_DIGIT + '/Untitled.png', img)

# create function to draw circle on mouse click
def draw_circle(event, x, y, flags, param):
    global LBDown

    if event == cv.EVENT_LBUTTONDOWN: # check if mouse event is click
        LBDown = True

    if event == cv.EVENT_LBUTTONUP: # check if mouse event is click
        LBDown = False

    if LBDown == True:
        cv.circle(img, (x, y), 5, (0,0,0), -1) # draw filled circle with 100px radius
        
# create cv2 window and bind callback
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)

while(1): 
    cv.imshow('image',img)
    k = cv.waitKey(20) & 0xFF

    if k == 32:
        save()
        img = np.full((128,128,3), 255, np.uint8)
    elif k == 27:
        break



cv.destroyAllWindows()