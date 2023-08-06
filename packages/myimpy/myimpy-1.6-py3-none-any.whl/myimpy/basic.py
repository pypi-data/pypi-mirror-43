#H#######################################################################
# FILENAME :        basic.py             
# 
# DESIGN REF: numpy
#
# DESCRIPTION :
#       This script obtains basic information of an image.
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

#   Get the luminance of an image
def get_luminance(input_image):
    return np.sum(input_image)/np.size(input_image)

#   Get the contrast of an image
def get_contrast(input_image):
    return (np.amax(input_image) - np.amin(input_image))/(np.amax(input_image) + np.amin(input_image))

#   Draw the histogram of an image