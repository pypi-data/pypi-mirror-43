#H#######################################################################
# FILENAME :        __init__.c             
# 
# DESIGN REF: https://python-packaging.readthedocs.io/en/latest/minimal.html
#
# DESCRIPTION :
#       This file is to make Python treat the directories as containing
#       packages; this is done to prevent directories with a common name, 
#       such as string, from unintentionally hiding valid modules that 
#       occur later on the module search path.
#
# PUBLIC FUNCTIONS :
#       joke()
#
# NOTES :
#       This file can be simply empty and the function is just for fun.
#
#       Copyright: .  All rights reserved.
# 
# AUTHOR :          Jinhang <jinhang.d.zhu@gmail.com>
# VERSION :         1.1    
# START DATE :      07 Mar. 2019
#
# CHANGES :
#
# NO    VERSION     DATE        WHO     DETAIL
# 1     1.0         07 Mar. 19  J.Z     Initialization
# 2     1.1         08 Mar. 19  J.Z     Uploading using sdist
#
#H#

def greet():
    return ('I AM HERE.')