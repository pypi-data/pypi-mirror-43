#H#######################################################################
# FILENAME :        morphology.py             
# 
# DESIGN REF: numpy
#
# DESCRIPTION :
#       This script implements basic image morphology operations.
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

#   Get the k value of a structure element
def get_k(selem):
    (width,height) = np.shape(selem)
    if width == height:
        if width % 2 == 1:
            k = (width-1)/2
        elif width % 2 == 0:
            k = width/2
        k = int(k)
        return k
    elif width != height:
        print('[olala]  The structure element is NOT square!')
        return -1

#   Get the nonzero indices of a structure element
def get_index(selem):
    k = get_k(selem)
    store_i = [] # Store the horizonal indices of elements 1's
    store_j = [] # Store the vertical indices of elements 1's
    range_i = np.arange(-k,k+1)
    range_j = np.arange(-k,k+1)
    for i in range_i:
        for j in range_j:
            if selem[i+k,j+k] != 0:
                store_i.append(i)
                store_j.append(j)
    return store_i,store_j


#   Expand the image to make it have k more circles of pixels
def expand_image(source,k):
    (width_image,height_image)=np.shape(source.copy())
    expanded = np.zeros((width_image + 2*k,height_image + 2*k))
    expanded[k:-k,k:-k]=source[:,:]
    return expanded

#   Erosion
def erosion(source,selem):
    # Copied image of the original one
    im_copy = source.copy()
    
    # Expand the image
    k = get_k(selem)
    expanded = expand_image(im_copy,k)
    
    # Get information from the structure element and the image
    store_i,store_j = get_index(selem)
    (width_image,height_image)=np.shape(expanded)
    
    #print('shape of the original: ',np.shape(im_copy))
    #print('shape of the expanded: ',np.shape(expanded))
    
    if width_image >= 3 and height_image >= 3 and k >= 1:
        # Shifting the filter over the pixels inside
        for i_image in np.arange(k,width_image - k):          # There is a problem where I wrote a wrong right end width_image + k
            for j_image in np.arange(k,height_image - k):     # Mention that width_image is the expanded one
                # print('i_image:{},j_image:{},k:{}'.format(i_image,j_image,k))  # Helped me to find the error
                # Element-wise multiplication to find nonzeros
                frame = expanded[i_image - k:i_image + k + 1,j_image - k:j_image + k + 1] * selem
                store_frame_i,store_frame_j = get_index(frame)
                if((store_frame_i == store_i and store_frame_j == store_j) == True): # Including for erosion
                    
                    # The two indices are completely the same, then this pixel should be set as 1
                    im_copy[i_image-k,j_image-k] = 1
                else:
                    im_copy[i_image-k,j_image-k] = 0
        return im_copy
    else:
        return -1

#   Dilation
def dilation(source,selem):
    # Copied image of the original one
    im_copy = source.copy()
    
    # Expand the image
    k = get_k(selem)
    expanded = expand_image(im_copy,k)
    
    # Get information from the structure element and the image
    # store_i,store_j = get_index(selem)
    (width_image,height_image)=np.shape(expanded)
    
    #print('shape of the original: ',np.shape(im_copy))
    #print('shape of the expanded: ',np.shape(expanded))

    if width_image >= 3 and height_image >= 3 and k >= 1:   
        # Shifting the filter over the pixels inside
        for i_image in np.arange(k,width_image - k):          # There is a problem where I wrote a wrong right end width_image + k
            for j_image in np.arange(k,height_image - k):     # Mention that width_image is the expanded one
                # print('i_image:{},j_image:{},k:{}'.format(i_image,j_image,k))  # Helped me to find the error
                # Element-wise multiplication to find nonzeros
                frame = expanded[i_image - k:i_image + k + 1,j_image - k:j_image + k + 1] * selem
                store_frame_i,store_frame_j = get_index(frame)
                if((len(store_frame_i) >= 1 and len(store_frame_j) >= 1) == True):  # Touching for dilation  
                    # The two indices are completely the same, then this pixel should be set as 1
                    im_copy[i_image-k,j_image-k] = 1
                else:
                    im_copy[i_image-k,j_image-k] = 0
        return im_copy
    else:
        return -1