# -*- coding: utf-8 -*-
from visual import *
from variables import *


class Planet:
    def __init__(self, window):
        self.win = window

    def description(self):
        if self.win.PL:
            return u"Symulacja ruchu Merkurego wokół słońca\nMożna wybrać procent jego naturalnej prędkości,\n" \
               u"a także modyfikować odległość od słońca, wartość stałej grawitacji oraz masę Słońca"
        else:
            return "This simulation shows a single planet\nYou can define its velocity\n" \
                   "as well as modify distance from the sun\nand change value of constants M and G"

    def prepare(self):
        self.sun = sphere(pos=(0, 0, 0), radius=10 ** 10, color=color.yellow)
        self.vel_percent = self.win.Ctrls[0].GetValue() / 100
        self.dist_percent = self.win.Ctrls[1].GetValue() / 100
        self.G_percent = self.win.Ctrls[2].GetValue() / 100
        self.M_percent = self.win.Ctrls[3].GetValue() / 100
        self.T = curve(color=color.magenta)
        self.planet = sphere(pos=(self.dist_percent * 70 * (10 ** 9), 0, 0), radius=4.5 * 10 ** 9, color=color.magenta)
        self.win.scene.autoscale = False
        self.win.scene.range = 10 ** 11 * 4
        self.planet.vel = vector(0, self.vel_percent * 40000, 0)
        self.vel_vector = arrow(pos=self.planet.pos,
                                axis=(self.planet.vel.x * (9.3 ** 6), self.planet.vel.y * (9.3 ** 6), 0),
                                shaftwidth=3000000000, opacity=1, color=color.green)
        self.F_vector = arrow(pos=self.planet.pos,
                              axis=(-self.planet.vel.y * (9.3 ** 6), self.planet.vel.x * (9.3 ** 6), 0),
                              shaftwidth=3000000000, opacity=1, color=color.blue)

    def run(self):
        t = 0
        dt = 3600
        while self.win.simulation.mode == 'Planet':
            if self.win.simulation_stopped is False:
                rate(1000)
                a = vector(-self.win.Ctrls[2].GetValue() / 100 * G * self.win.Ctrls[3].GetValue() / 100 * M * (
                            self.planet.pos / (mag(self.planet.pos) ** 3)))
                self.planet.vel = self.planet.vel + a * dt
                self.planet.pos = self.planet.pos + self.planet.vel * dt
                self.T.append(pos=self.planet.pos, retain=30000)
                self.vel_vector.pos = self.planet.pos
                self.vel_vector.axis = (self.planet.vel.x * (9.3 ** 6), self.planet.vel.y * (9.3 ** 6), 0)
                self.F_vector.pos = self.planet.pos
                self.F_vector.axis = (-self.planet.vel.y * (9.3 ** 6), self.planet.vel.x * (9.3 ** 6), 0)
                t += dt
                if t % 86400 == 0:
                    if self.win.PL:
                        self.win.var_exec[0].SetLabel('Dni: ' + '%d' % (t / 86400))
                    else:
                        self.win.var_exec[0].SetLabel('Days: ' + '%d' % (t / 86400))
                    self.win.var_exec[1].SetLabel('V = ' + '%.2f' % (self.planet.vel.mag / 1000) + ' [km/s]')
            else:
                rate(10)
