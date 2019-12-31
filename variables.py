import numpy as np
g = 9.806
degree_to_rad = 0.01745329252
M=2*(10**30)
G=6.7*(10**-11)

colors = {
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'magenta': (255, 0, 255),
    'cyan': (0, 255, 255),
    'orange': (255, 165, 0),
    'gray': (128, 128, 128),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'black': (0, 0, 0)
}


def toRadian(angle):
    return degree_to_rad*angle

def toAngle(radian):
    return radian/degree_to_rad