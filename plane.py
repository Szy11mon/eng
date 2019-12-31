# -*- coding: utf-8 -*-
from visual import *
from variables import *
from physics import *


class Plane:
    def __init__(self, win):
        self.win = win

    def description(self):
        if self.win.PL:
            return u"Symulacja równi pochyłej.\nKąt definiuje nachylenie równi.\n" \
                   u"Można ustalić masę klocka oraz długość równi\nTarcie jest współczynikiem pomiędzy 0 a 1\n" \
                   u"który określa jak duży jest wpływ podłoża na klocek.\nOpór powietrza to współczynnik" \
                   u" określający\nwpływ powietrza na przyspieszenie."
        else:
            return "This is simple inclined plane\nAngle defines how steep the plane is" \
               "\nYou can also define mass of the block and plane length\nFriction is a coefficient between 0 and 1"\
               "\nthat says how much the floor reacts on block\nAir resistance is also a coefficient"\
               "\nwhich defines how much the air influences acceleration "


    def reset(self):
        pass

    def prepare(self):
        if self.win.PL:
            self.win.var_exec[0].SetLabel('czas = 0 [s]')
            self.win.var_exec[1].SetLabel('V = 0 [m/s]')
            self.win.var_exec[2].SetLabel('a = 0 [m/s^2]')
        else:
            self.win.var_exec[0].SetLabel('time = 0 [s]')
            self.win.var_exec[1].SetLabel('V = 0 [m/s]')
            self.win.var_exec[2].SetLabel('a = 0 [m/s^2]')
        self.dist = 0
        self.angle = self.win.Ctrls[0].GetValue()
        self.mass = self.win.Ctrls[1].GetValue()
        self.length = self.win.Ctrls[2].GetValue()
        self.friction = self.win.Ctrls[3].GetValue()
        self.air_res = self.win.Ctrls[4].GetValue()
        self.win.scene.autoscale = False
        self.win.scene.range = self.length * 1.1
        self.theta = degree_to_rad * self.angle
        k = sqrt(self.length) * (log10(self.length) + 1)
        self.inclinedPlane = box(pos=(0, 0, 0), size=(self.length, 0.02*k, 0.2*k), color=color.green, opacity=0.3)
        self.cart = box(size=(0.2*k, 0.12*k, 0.06*k), color=color.blue)

        self.cart.m = self.mass
        self.cart.pos = vector(self.length / 2. + 0.1*k, 0.06*k, 0)
        self.cart.v = vector(0, 0, 0)

        rotate_object(self.inclinedPlane, self.angle, (0,0,0))
        rotate_object(self.cart, self.angle, (0, 0, 0))

        floor = box(pos=(0, -self.length*sin(self.theta)/2, 0), size=(self.length*cos(self.theta), 0.02*k, 0.2*k),
                    color=color.green, opacity=0.3)
        wall = box(pos=(self.length*cos(self.theta)/2, 0, 0), size=(0.02*k, self.length*sin(self.theta), 0.2*k),
                   color=color.green, opacity=0.3)
        scalex = arrow(pos=(self.length*cos(self.theta)/2,  -self.length*sin(self.theta)/2 -0.05*self.length, -0.01*self.length),
                       axis=(-self.length*cos(self.theta), 0, 0),shaftwidth=0.02*k, color=color.white)
        scaley = arrow(pos=(self.length * cos(self.theta) / 2 + 0.05 * self.length, -self.length*sin(self.theta)/2, -0.01*self.length),
                       axis=(0, self.length*sin(self.theta), 0),
                       shaftwidth=0.02 * k, color=color.white)
        txtx = label(pos=(0,  -self.length*sin(self.theta)/2 - 0.1*self.length, 0),text='x', box=False,height=25,border=0)
        txty = label(pos=(self.length * cos(self.theta) / 2 + 0.1*self.length, 0, 0), text='y', box=False, height=25,
                     border=0)
        self.FN = arrow(pos=self.cart.pos + vector(0.06*k,0,0), axis=(0.2*k, 0, 0), shaftwidth=0.02*k,color = color.red)
        self.FY = arrow(pos=self.cart.pos + vector(0.06*k,0,0), axis=(0.2*k, 0, 0), shaftwidth=0.02*k,color=color.gray(0.5))
        self.FT = arrow(pos=self.cart.pos - (-0.1*k,0.05*k,0), axis=(0.2*k*self.friction*(1/tan(self.theta)), 0, 0), shaftwidth=0.02*k,color=color.magenta)
        self.FP = arrow(pos=self.cart.pos + (0.1*k, 0.05 * k, 0), axis=(0, 0, 0),shaftwidth=0.02*k, color=color.cyan)
        self.FX = arrow(pos=self.cart.pos + (0.1*k,0,0), axis=(0.2 * k, 0, 0), shaftwidth=0.02 * k, color=color.orange)
        rotate_object(self.FN, self.angle + 90, self.cart.pos)
        rotate_object(self.FY, self.angle + 270, self.cart.pos)
        rotate_object(self.FT, self.angle, self.cart.pos)
        rotate_object(self.FP, self.angle, self.cart.pos)
        rotate_object(self.FX, self.angle + 180, self.cart.pos)
        self.F = norm(self.inclinedPlane.axis)
        self.F.mag = self.cart.m * g * (sin(self.theta) - cos(self.theta) * self.friction)
        self.arr_len = 0.2*k - 0.2*k*self.friction*(1/tan(self.theta))
        self.arr_len = -self.FX.axis.x - self.FT.axis.x

        self.t = 0
        self.dt = 0.0005

    def run(self):
        counter = 0
        while self.dist < self.length:
            if not self.win.simulation_stopped:
                rate(1000)
                F = cart_velocity(self.cart, self.theta, self.friction, self.air_res, self.dt)

                self.cart.pos = self.cart.pos - self.cart.v * self.dt
                self.FN.pos = self.FN.pos - self.cart.v * self.dt
                self.FY.pos = self.FY.pos - self.cart.v * self.dt
                self.FT.pos = self.FT.pos - self.cart.v * self.dt
                self.FX.pos = self.FX.pos - self.cart.v * self.dt
                tmp = ((self.F.mag - F.mag) / self.F.mag) * self.arr_len
                self.FP.axis = (tmp, tmp/self.FX.axis.x*self.FX.axis.y, 0)
                self.FP.pos = self.FP.pos - self.cart.v * self.dt
                counter = counter + 1
                self.dist = self.dist + self.cart.v.mag*self.dt
                if counter % 50 is 0:
                    if self.win.PL:
                        self.win.var_exec[0].SetLabel('czas = ' + '%.2f'% self.t + ' [s]')
                    else:
                        self.win.var_exec[0].SetLabel('time = ' + '%.2f' % self.t + ' [s]')
                    self.win.var_exec[1].SetLabel('V = ' + '%.2f' % self.cart.v.mag + ' [m/s]')
                    self.win.var_exec[2].SetLabel('a = ' + '%.2f' % (F.mag / self.mass) + ' [m/s^2]')
                self.t = self.t + self.dt
            else:
                while True:
                    rate(10)



