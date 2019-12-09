import pdb
import pickle
import random
import copy
import numpy as np
import cv2
img = cv2.imread('./face.png')
cv2.imshow('orig', img)
cv2.waitKey(-1)  # Wait until a key is pressed to exit the program
cv2.destroyAllWindows()