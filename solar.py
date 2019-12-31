# -*- coding: utf-8 -*-
from visual import *
from variables import *


class Solar:
    def __init__(self, window):
        self.win = window

    def description(self):
        if self.win.PL:
            return u"Symulacja naszego układu słonecznego\nMożesz wybrać procent prędkości Ziemi z jaką będzie" \
               u"się poruszać\nU dołu ekranu możesz śledzić liczbę dni, które upłynęły\nPrzyspieszenie planety" \
               u"opisane jest wzorem a = GM/r^2\nMożesz zmienić potęgę r w tym wzorze\nZmian lepiej dokonywać o setne " \
               u"części,\nbo nawet wtedy można zaobserwować bardzo ciekawe zjawisko"
        else:
            return "This simulation shows our solar system\nYou can pick with how much of its actual speed\n" \
                   "the Earth will move\nThe number of days that passed is displayed\nThe acceleration of the planet" \
                   "is described by formula: a = GM/r^2\nYou can change the power in that formula\nDo it only by" \
                   " 0.01 or so, cause even then You will see shocking results"

    def prepare(self):
        self.percent = self.win.Ctrls[0].GetValue()
        self.power = self.win.Ctrls[1].GetValue()
        self.sun = sphere(pos=(0, 0, 0), radius=10 ** 10, color=color.yellow)
        self.T = [curve(color=color.magenta), curve(color=color.green), curve(color=color.blue), curve(color=color.red)]
        self.planet1 = sphere(pos=(70 * (10 ** 9), 0, 0), radius=3 * 10 ** 9, color=color.magenta)
        self.planet2 = sphere(pos=(110 * (10 ** 9), 0, 0), radius=4 * 10 ** 9, color=color.green)
        self.planet3 = sphere(pos=(150 * (10 ** 9), 0, 0), radius=4.5 * 10 ** 9, color=color.blue)
        self.planet4 = sphere(pos=(250 * (10 ** 9), 0, 0), radius=3 * 10 ** 9, color=color.red)

        self.planet1.vel = vector(0, 47000, 0)
        self.planet2.vel = vector(0, 35000, 0)
        self.planet3.vel = vector(0, (self.percent/100)*30000, 0)
        self.planet4.vel = vector(0, 24000, 0)

        self.L = [self.planet1, self.planet2, self.planet3, self.planet4]

    def run(self):
        t=0
        dt = 3600
        while self.win.simulation.mode == 'Solar':
            if not self.win.simulation_stopped:
                rate(1000)
                for i in range(0, 4):
                    a = vector(-G * M * (self.L[i].pos / (mag(self.L[i].pos) ** self.power)))
                    self.L[i].vel = self.L[i].vel + a * dt
                    self.L[i].pos = self.L[i].pos + self.L[i].vel * dt
                    self.T[i].append(pos=self.L[i].pos)
                t += dt
                if t % 86400 == 0:
                    if self.win.PL:
                        self.win.var_exec[0].SetLabel('Dni: ' + '%d' % (t/86400))
                    else:
                        self.win.var_exec[0].SetLabel('Days: ' + '%d' % (t / 86400))
            else:
                rate(10)

