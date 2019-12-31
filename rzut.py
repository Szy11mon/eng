# -*- coding: utf-8 -*-
from visual import *
from variables import *
import math


class Throw:

    def __init__(self, window):
        self.win = window

    def description(self):
        if self.win.PL:
            return u"Symulacja rzutu ukośnego z uwzględnieniem oporu powietrza\nMożesz wybrać kąt pod którym rzucane" \
               u"jest ciało\nprędkość początkową, a także współczynnik opoeu powietrza\nW trakcie symulacji możesz" \
               u"obserwować prędkości w obu kierunkach,\na także wysokość i odległość"
        else:
            return "This is diagonal throw but with the influence of the air\nYou can set angle, starting velocity\n" \
                   "and the coefficient of air resistance\nFunction of air resistance is defined v = v^x\n" \
                   "and Power variable lets You choose that x\nDuring the simulation you will see velocities in both directions\n" \
                   "height and distance"

    def prepare(self):
        self.angle = self.win.Ctrls[0].GetValue()
        self.velocity = self.win.Ctrls[1].GetValue()
        self.air_res = self.win.Ctrls[2].GetValue()
        self.theta = degree_to_rad * self.angle
        self.power = self.win.Ctrls[3].GetValue()
        hmax = ((self.velocity * sin(self.theta))**2)/(2*g)
        if self.angle < 75:
            self.scale = (self.velocity * self.velocity * sin(2 * self.theta)) / g
        else:
            self.scale = hmax*1.1
        self.win.scene.range = self.scale
        self.win.scene.center = (0, hmax/2, 0)
        # self.win.scene.autoscale = False
        self.cannon = box(pos=(-(self.scale / 2), self.scale * 0.02, 0),
                          size=(self.scale * 0.05, self.scale * 0.05, self.scale * 0.05), color=color.red, opacity=0.6)
        self.Road = box(pos=vector(0, 0, 0), size=vector(self.scale * 1.4, self.scale / 300, self.scale / 10), color=color.green,
                        opacity=0.3)
        scalex = arrow(pos=(-self.scale * 0.7, 0 - self.scale / 15, 0),
                       axis=(self.scale * 1.4, 0, 0), shaftwidth=0.01 * self.scale, color=color.white)
        scaley = arrow(pos=(-self.scale * 0.8, 0, 0),
                       axis=(0, hmax + 0.02 * self.scale, 0),
                       shaftwidth=0.01 * self.scale, color=color.white)
        txtx = label(pos=(0, 0 - self.scale / 10, 0), text='x', box=False, height=25, border=0, opacity=0)
        txty = label(pos=(-self.scale * 0.85, hmax / 2 + 0.01 * self.scale, 0), text='y', box=False, height=25, border=0)
        if self.air_res > 0:
            self.pot_trail = curve(color=color.cyan)
        self.ball = sphere(
            pos=(self.cannon.pos.x, self.cannon.pos.y, self.cannon.pos.z),
            radius=self.scale * 0.025,
            color=color.blue, make_trail=True)
        self.VX = arrow(pos=self.ball.pos + (self.scale * 0.02, 0, 0), axis=(0.1 * self.scale, 0, 0),
                        shaftwidth=0.01 * self.scale, color=color.red)
        self.VY = arrow(pos=self.ball.pos + (0, self.scale * 0.02, 0), axis=(0, 0.1 * self.scale, 0),
                        shaftwidth=0.01 * self.scale, color=color.magenta)
        self.ball.v = vector(self.velocity * cos(self.theta), self.velocity * sin(self.theta), 0)
        self.pot_vel = self.ball.v
        self.pot_pos = self.ball.pos
        self.dt = 0.0005
        self.t = 0
        self.ball.trail_object.color = color.yellow
        if self.win.PL:
            self.win.var_exec[1].SetLabel(u'wysokość = ' + '%.2f' % (self.ball.pos.y - self.cannon.pos.y) + ' [m]')
            self.win.var_exec[0].SetLabel(u'długość = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x) + ' [m]')
        else:
            self.win.var_exec[1].SetLabel('height = ' + '%.2f' % (self.ball.pos.y - self.cannon.pos.y) + ' [m]')
            self.win.var_exec[0].SetLabel('distance = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x) + ' [m]')
        self.win.var_exec[3].SetLabel('Vx = ' + '%.2f' % self.ball.v.x + ' [m/s]')
        self.win.var_exec[2].SetLabel('Vy = ' + '%.2f' % self.ball.v.y + ' [m/s]')
        self.pos = self.ball.pos

    def run(self):
        counter = 0
        rotate_y = False
        while self.pot_pos.y > 0:
            if not self.win.simulation_stopped:
                rate(100 * self.velocity)
                if self.ball.pos.y >= self.cannon.pos.y:
                    self.ball.v = self.ball.v - self.air_res * mag(self.ball.v) ** self.power * (self.ball.v/mag(self.ball.v)) * self.dt \
                                  - vector(0, 1, 0) * g * self.dt
                    self.ball.pos = self.ball.pos + self.ball.v * self.dt
                    self.VX.pos = self.VX.pos + self.ball.v * self.dt
                    self.VY.pos = self.VY.pos + self.ball.v * self.dt
                    self.VY.axis = (0, 0.1 * self.scale * (self.ball.v.y / (self.velocity * sin(self.theta))), 0)
                    self.VX.length = 0.1 * self.scale * (self.ball.v.x / (self.velocity * cos(self.theta)))
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
                        self.win.var_exec[1].SetLabel('height = ' + '%.2f' % (self.ball.pos.y - self.cannon.pos.y) + ' [m]')
                        self.win.var_exec[0].SetLabel('distance = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x) + ' [m]')
                    self.win.var_exec[3].SetLabel('Vx = ' + '%.2f' % self.ball.v.x + ' [m/s]')
                    self.win.var_exec[2].SetLabel('Vy = ' + '%.2f' % self.ball.v.y + ' [m/s]')
            else:
                while True:
                    rate(10)
        if self.win.PL:
            self.win.var_exec[1].SetLabel(u'wysokość = 0.00 [m]')
            self.win.var_exec[0].SetLabel(u'długość = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x) + ' [m]')
        else:
            self.win.var_exec[1].SetLabel('height = 0.00 [m]')
            self.win.var_exec[0].SetLabel('distance = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x) + ' [m]')
        self.win.var_exec[3].SetLabel('Vx = ' + '%.2f' % self.ball.v.x + ' [m/s]')
        self.win.var_exec[2].SetLabel('Vy = ' + '%.2f' % self.ball.v.y + ' [m/s]')
