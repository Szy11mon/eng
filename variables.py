import numpy as np
g=9.806
degree_to_rad = 0.01745329252
M=2*(10**30)
G=6.7*(10**-11)

def toRadian(angle):
    return degree_to_rad*angle
def toAngle(radian):
    return radian/degree_to_rad