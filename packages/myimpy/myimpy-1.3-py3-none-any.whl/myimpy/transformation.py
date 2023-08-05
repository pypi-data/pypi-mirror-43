#H#######################################################################
# FILENAME :        transformation.py             
# 
# DESIGN REF: numpy
#
# DESCRIPTION :
#       This script implements basic image transformations.
#
# PUBLIC FUNCTIONS :
#       
#
# NOTES :
#       
#
# 
#
# CHANGES :
#
# NO    VERSION     DATE        WHO     DETAIL
#  
#
#H#

import numpy as np

#   Transforming an image into a grayscale one
def rgb2gray(source):
    if len(np.shape(source)) == 3:
        return np.dot(source[...,:3], [0.299, 0.587, 0.114])
    elif len(np.shape(source)) == 2:
        print('[olala]  The image is already grayscale!')
        return source

#   Making downsampled image
def downsample_image(gray):
    odd_even = gray[0::2,1::2] # Extract odd rows and even columns
    return odd_even

#   Binarizing the image with a threshold input
def gray2bin(gray, threshold):
    binary = gray[:,:] > threshold
    return binary

#   Shuffle the pixels of an image
def shuffle_image(source):
    im_shuffle = source.ravel().copy()
    np.random.shuffle(im_shuffle)
    im_shuffle=np.reshape(im_shuffle, source.shape)
    return im_shuffle

#   Invert the image grayscale
def invert_image(source):
    a = -1
    b = 255
    invert_image = a*source.copy() + b
    return invert_image

#   Linearize the image grayscale
def linear(source, a, b):
    linearized = a*source.copy() + b
    linearized[linearized > 255] = 255
    linearized[linearized < 0] = 0
    return linearized