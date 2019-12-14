# -*- coding: utf-8 -*-
from visual import *
from variables import *
import math


class Throw:

    def __init__(self, window):
        self.win = window

    @staticmethod
    def descriptionENG():
        return "This is diagonal throw but with the influence of the air\nYou can set angle, starting velocity\n"\
               "and the coefficient of air resistance\nFunction of air resistance is defined v = v^x\n" \
               "and Power variable lets You choose that x\nDuring the simulation you will see velocities in both directions\n"\
               "height and distance"

    @staticmethod
    def descriptionPL():
        return u"Symulacja rzutu ukośnego z uwzględnieniem oporu powietrza\n Możesz wybrać kąt pod którym rzucane" \
               u"jest ciało\nprędkość początkową, a także współczynnik opoeu powietrza\nW trakcie symulacji możesz" \
               u"obserwować prędkości w obu kierunkach,\n a także wysokość i odległość"

    def prepare(self):
        self.angle = self.win.Ctrls[0].GetValue()
        self.velocity = self.win.Ctrls[1].GetValue()
        self.air_res = self.win.Ctrls[2].GetValue()
        self.theta = degree_to_rad * self.angle
        self.power = self.win.Ctrls[3].GetValue()
        hmax = ((self.velocity * sin(self.theta))**2)/(2*g)
        self.win.scene.center = (0, hmax/2, 0)
        self.win.scene.autoscale = False
        self.dist = (self.velocity * self.velocity * sin(2 * self.theta)) / g
        self.cannon = box(pos=(-(self.dist / 2), self.dist * 0.02, 0),
                          size=(self.dist * 0.04, self.dist * 0.04, self.dist * 0.04), color=color.red)
        self.Road = box(pos=vector(0, 0, 0), size=vector(self.dist * 1.4, self.dist / 300, self.dist/10), color=color.green,
                        opacity=0.3)
        scalex = arrow(pos=(-self.dist * 0.7, -sqrt(hmax)*self.velocity/60, 0),
                       axis=(self.dist * 1.4, 0, 0), shaftwidth=0.01 * self.dist, color=color.white)
        scaley = arrow(pos=(-self.dist * 0.8, 0, 0),
                        axis=(0, hmax, 0),
                        shaftwidth=0.01 * self.dist, color=color.white)
        txtx = label(pos=(0, -sqrt(hmax)*self.velocity/40, 0), text='x', box=False, height=25, border=0,opacity=0)
        txty = label(pos=(-self.dist * 0.85, hmax/2, 0), text='y', box=False, height=25,border=0)
        if self.angle < 70:
            self.win.scene.range = (self.velocity * self.velocity / g) * sin(2 * self.theta)
            self.win.scene.center = (0, hmax/2, 0)
        else:
            self.win.scene.range = (self.velocity * self.velocity / g) * sin(2 * self.theta) * 1.5
            self.win.scene.center = (0, hmax/2, 0)
        if self.air_res > 0:
            self.pot_trail = curve(color=color.cyan)
        self.ball = sphere(
            pos=(self.cannon.pos.x + self.dist * 0.02, self.cannon.pos.y + self.dist * 0.02, self.cannon.pos.z),
            radius=self.dist * 0.02,
            color=color.blue, make_trail=True)
        self.VX = arrow(pos=self.ball.pos + (self.dist * 0.02, 0, 0), axis=(0.1 * self.dist, 0, 0),
                        shaftwidth=0.01 * self.dist, color=color.red)
        self.VY = arrow(pos=self.ball.pos + (0, self.dist * 0.02, 0), axis=(0.1 * self.dist, 0, 0),
                        shaftwidth=0.01 * self.dist, color=color.magenta)
        self.VY.rotate(angle=degree_to_rad * 90, origin=self.ball.pos + (0, self.dist * 0.02, 0), axis=vector(0, 0, 1))
        self.ball.v = vector(self.velocity * cos(self.theta), self.velocity * sin(self.theta), 0)
        self.pot_vel = self.ball.v
        self.pot_pos = self.ball.pos
        self.dt = 0.0005
        self.t = 0
        self.ball.trail_object.color = color.yellow

    def run(self):
        counter = 0
        rotate_y = False
        while self.pot_pos.y > 0:
            if not self.win.simulation_stopped:
                rate(100 * self.velocity)
                if self.ball.pos.y > self.cannon.pos.y:
                    self.ball.v = self.ball.v - self.air_res * vector(self.ball.v.x**self.power,
                                                                      abs(self.ball.v.y)**self.power,
                                                                      self.ball.v.z**self.power) * self.dt
                    self.ball.v.y = self.ball.v.y - g*self.dt
                    self.ball.pos = self.ball.pos + self.ball.v * self.dt
                    self.VX.pos = self.VX.pos + self.ball.v * self.dt
                    self.VY.pos = self.VY.pos + self.ball.v * self.dt
                    self.VY.length = abs(0.1 * self.dist * (self.ball.v.y / (self.velocity * sin(self.theta))))
                    self.VX.length = 0.1 * self.dist * (self.ball.v.x / (self.velocity * cos(self.theta)))
                if self.ball.v.y < 0 and rotate_y is False:
                    self.VY.rotate(angle=degree_to_rad * 180, origin=self.ball.pos, axis=vector(0, 0, 1))
                    rotate_y = True
                self.t = self.t + self.dt
                self.pot_vel.y = self.pot_vel.y - g*self.dt
                self.pot_pos = self.pot_pos + self.pot_vel*self.dt
                if self.air_res > 0:
                    self.pot_trail.append(self.pot_pos)

                counter = counter + 1
                if counter % 50 is 0:
                    if self.win.PL:
                        self.win.var_exec[1].SetLabel(u'wysokość = ' + '%.2f' % (self.ball.pos.y - self.cannon.pos.y) + ' [m]')
                        self.win.var_exec[0].SetLabel(u'długość = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x) + ' [m]')
                    else:
                        self.win.var_exec[1].SetLabel('h = ' + '%.2f' % (self.ball.pos.y - self.cannon.pos.y) + ' [m]')
                        self.win.var_exec[0].SetLabel('x = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x) + ' [m]')
                    self.win.var_exec[3].SetLabel('Vx = ' + '%.2f' % self.ball.v.x + ' [m/s]')
                    self.win.var_exec[2].SetLabel('Vy = ' + '%.2f' % self.ball.v.y + ' [m/s]')
            else:
                while True:
                    rate(10)
        if self.win.PL:
            self.win.var_exec[1].SetLabel(u'wysokość = 0 [m]')
            self.win.var_exec[0].SetLabel(u'długość = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x) + ' [m]')
        else:
            self.win.var_exec[1].SetLabel('h = 0 [m]')
            self.win.var_exec[0].SetLabel('x = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x) + ' [m]')
        self.win.var_exec[3].SetLabel('Vx = ' + '%.2f' % self.ball.v.x + ' [m/s]')
        self.win.var_exec[2].SetLabel('Vy = ' + '%.2f' % self.ball.v.y + ' [m/s]')
