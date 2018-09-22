import numpy as np
from PIL import ImageGrab
import cv2
import time

def read_screen():
    while True:
        #Focuse on the window of the game
        screen = np.array(ImageGrab.grab(bbox=(0 ,40, 740, 500)))
        new_screen = process_img(screen)
        #Covert Image to default color

        cv2.imshow('window', new_screen)
        #cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

        #Quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
#Process Image to simplify it
def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    return processed_img

read_screen()