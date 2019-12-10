def momentum_conservation_principle(object1,object2):
    m1 = object1.m
    m2 = object2.m
    tmp = object1.v
    object1.v = ((m1 - m2) / (m1 + m2)) * object1.v + (2 * m2 / (m1 + m2)) * object2.v
    object2.v = (2 * m1 / (m1 + m2)) * tmp + ((m2 - m1) / (m1 + m2)) * object2.v
