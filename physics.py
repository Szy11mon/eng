from visual import *
from variables import *


def momentum_conservation_principle(object1,object2):
    m1 = object1.m
    m2 = object2.m
    tmp = object1.v
    object1.v = ((m1 - m2) / (m1 + m2)) * object1.v + (2 * m2 / (m1 + m2)) * object2.v
    object2.v = (2 * m1 / (m1 + m2)) * tmp + ((m2 - m1) / (m1 + m2)) * object2.v


def rotate_object(item, angle, origin):
    rotate_angle = 0.01745329252*angle
    item.rotate(angle=rotate_angle, origin=origin, axis=(0, 0, 1))
    
    
def cart_velocity(cart, theta, friction, air_res, dt):
    f = norm(cart.axis)
    f = f * (cart.m * g * (
                sin(theta) - cos(theta) * friction) - air_res * cart.v.mag2)
    cart.v = cart.v + (f / cart.m * dt)
    if cart.v.y < 0:
        cart.v = vector(0, 0, 0)
    return f
