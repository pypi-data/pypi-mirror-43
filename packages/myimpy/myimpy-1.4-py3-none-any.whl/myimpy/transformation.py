#H#######################################################################
# FILENAME :        transformation.py             
#
# DESCRIPTION :
#       This script implements basic image transformations.
#
# AUTHOR :          Jinhang <jinhang.d.zhu@gmail.com>
# START DATE :      07 Mar. 2019
# LAST UPDATE :     12 Mar. 2019
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

#   Calculate the histogram of the image
def calchist(source):
    gray = rgb2gray(source)
    (height,width) = np.shape(gray)
    hist = np.zeros(256, dtype = int)
    axis_height = np.arange(0,height,1)
    axis_width = np.arange(0,width,1)
    for i in axis_height:
        for j in axis_width:
            hist[np.uint8(gray[i,j])] = hist[np.uint(gray[i,j])] + 1
    hist = hist/np.size(gray)
    return hist

#   Calculate the transfer function of equalization
#   Calculate the cumulative function of the function
def calccumu(source):
    axis_range = np.arange(0,256)
    hist = calchist(source)
    cumu_trans = np.zeros(256)
    for i in axis_range:
        if i == 0:
            cumu_trans[i] = hist[i]
        else:
            cumu_trans[i] = cumu_trans[i-1] + hist[i]
    cumu_trans = cumu_trans * 255
    return cumu_trans

#   Histogram Equalization
def equalization(source):
    gray = rgb2gray(source)
    (height,width) = np.shape(gray)
    axis_height = np.arange(0,height,1)
    axis_width = np.arange(0,width,1)
    cumu_trans = calccumu(source)
    equalized = source.copy()
    for i in axis_height:
        for j in axis_width:
            equalized[i,j] = cumu_trans[np.uint8(equalized[i,j])]
    return equalized