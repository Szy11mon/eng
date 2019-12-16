# -*- coding: utf-8 -*-
from physics import *
from visual import *
from variables import *


class Momentum2:

    def __init__(self,window):
        self.win = window

    @staticmethod
    def descriptionENG():
        return "There are four balls\nYou can define their masses as height of the first ball\n" \
               "Distance between them is one meter\n" \
               "They fall beacause of the gravity force and bounce\nThis causes the lighttest ball to gain" \
               "height\nwhich You can check at the bottom"

    @staticmethod
    def descriptionPL():
        return u"Są cztery piłki\nMożesz wybrać ich masy, a także wysokość pierwszej z nich\n" \
               u"Oddalone są od siebie o metr\n" \
               u"Spadają one pod wpływem grawitacji i odbijają się od podłoża\nco powoduje nabranie bardzo dużej" \
               u"wysokości przez najlżejszą kulkę\nJej wysokość widać u dołu ekranu"

    def prepare(self):
        self.masses = [self.win.Ctrls[0].GetValue(), self.win.Ctrls[1].GetValue(), self.win.Ctrls[2].GetValue(),
                       self.win.Ctrls[3].GetValue()]
        self.height = self.win.Ctrls[4].GetValue()
        self.balls = []
        self.balls_alt = []
        if self.masses[0] > self.masses[1]:
            if self.masses[1] > self.masses[2]:
                if self.masses[2] > self.masses[3]:
                    r1 = 3*(log10(self.masses[0] / self.masses[3]) + 1)
                    r2 = 3*(log10(self.masses[1] / self.masses[3]) + 1)
                    r3 = 3*(log10(self.masses[2] / self.masses[3]) + 1)
                    r4 = 3
                else:
                    r1 = 3*(log10(self.masses[0] / self.masses[2]) + 1)
                    r2 = 3*(log10(self.masses[1] / self.masses[2]) + 1)
                    r3 = 3
                    r4 = 3*(log10(self.masses[3] / self.masses[2]) + 1)
            else:
                if self.masses[1] > self.masses[3]:
                    r1 = 3*(log10(self.masses[0] / self.masses[3]) + 1)
                    r2 = 3*(log10(self.masses[1] / self.masses[3]) + 1)
                    r3 = 3*(log10(self.masses[2] / self.masses[3]) + 1)
                    r4 = 3
                else:
                    r1 = 3*(log10(self.masses[0] / self.masses[1]) + 1)
                    r2 = 3
                    r3 = 3*(log10(self.masses[2] / self.masses[1]) + 1)
                    r4 = 3*(log10(self.masses[3] / self.masses[1]) + 1)
        else:
            if self.masses[0] > self.masses[2]:
                if self.masses[2] > self.masses[3]:
                    r1 = 3*(log10(self.masses[0] / self.masses[3]) + 1)
                    r2 = 3*(log10(self.masses[1] / self.masses[3]) + 1)
                    r3 = 3*(log10(self.masses[2] / self.masses[3]) + 1)
                    r4 = 3
                else:
                    r1 = 3 * (log10(self.masses[0] / self.masses[2]) + 1)
                    r2 = 3 * (log10(self.masses[1] / self.masses[2]) + 1)
                    r3 = 3
                    r4 = 3 * (log10(self.masses[3] / self.masses[2]) + 1)
            else:
                if self.masses[0] > self.masses[3]:
                    r1 = 3*(log10(self.masses[0] / self.masses[3]) + 1)
                    r2 = 3*(log10(self.masses[1] / self.masses[3]) + 1)
                    r3 = 3*(log10(self.masses[2] / self.masses[3]) + 1)
                    r4 = 3
                else:
                    r1 = 3
                    r2 = 3 * (log10(self.masses[1] / self.masses[0]) + 1)
                    r3 = 3 * (log10(self.masses[2] / self.masses[0]) + 1)
                    r4 = 3 * (log10(self.masses[3] / self.masses[0]) + 1)
        ball1 = sphere(pos=(150, self.height+r1, 0), radius=r1, color=color.blue)
        self.balls.append(ball1)
        ball2 = sphere(pos=(150, self.height+2*r1+r2 + 1, 0), radius=r2, color=color.blue)
        self.balls.append(ball2)
        ball3 = sphere(pos=(150, self.height+2*r1+2*r2+r3 + 1, 0), radius=r3, color=color.blue)
        self.balls.append(ball3)
        ball4 = sphere(pos=(150, self.height + 2 * r1 + 2 * r2 + 2 * r3 + r4 + 1, 0), radius=r4, color=color.blue)
        self.balls.append(ball4)
        ball1_alt = sphere(pos=ball1.pos - vector(200, 0, 0), radius=r1, color=color.green)
        self.balls_alt.append(ball1_alt)
        ball2_alt = sphere(pos=ball2.pos - vector(280, 0, 0), radius=r2, color=color.green)
        self.balls_alt.append(ball2_alt)
        ball3_alt = sphere(pos=ball3.pos - vector(360, 0, 0), radius=r3, color=color.green)
        self.balls_alt.append(ball3_alt)
        ball4_alt = sphere(pos=ball4.pos - vector(440, 0, 0), radius=r4, color=color.green)
        self.balls_alt.append(ball4_alt)
        for i in range(4):
            self.balls[i].v = vector(0, 0, 0)
            self.balls_alt[i].v = vector(0, 0, 0)
            self.balls[i].a = vector(0, -g, 0)
            self.balls_alt[i].a = vector(0, -g, 0)
            self.balls[i].m = self.masses[i]
            self.balls_alt[i].m = self.masses[i]

        self.win.scene.autoscale = False
        self.win.scene.range = 500
        road = box(pos=(0,0,0),size=(1000,1,10),color=color.red)
        self.win.scene.center = (0, 280, 0)

    def run(self):
        t=0
        dt=0.005
        counter = 0
        while True:
            if not self.win.simulation_stopped:
                rate(1000)
                for i in range(4):
                    self.balls[i].v = self.balls[i].v + self.balls[i].a * dt
                    self.balls_alt[i].v = self.balls_alt[i].v + self.balls_alt[i].a * dt
                for i in range(3):
                    if self.balls[i].pos.y > self.balls[i+1].pos.y - self.balls[i].radius - self.balls[i+1].radius:
                        momentum_conservation_principle(self.balls[i], self.balls[i+1])
                for i in range(4):
                    if self.balls[i].pos.y < 0 + self.balls[i].radius:
                        self.balls[i].v = -self.balls[i].v
                    if self.balls_alt[i].pos.y < 0 + self.balls_alt[i].radius:
                        self.balls_alt[i].v = -self.balls_alt[i].v
                for i in range(4):
                    self.balls[i].pos = self.balls[i].pos + self.balls[i].v * dt
                    self.balls_alt[i].pos = self.balls_alt[i].pos + self.balls_alt[i].v * dt
                # for i in range(3):
                #     if self.balls[i].pos.y > self.balls[i + 1].pos.y - self.balls[i].radius - self.balls[i + 1].radius:
                #         self.balls[i+1].pos.y = self.balls[i+1].pos.y + 0.001
                t = t + dt
                counter = counter + 1
                if counter % 50 == 0:
                    if self.win.PL:
                        self.win.var_exec[4].SetLabel(u'wysokość = ' + '%.2f' % self.balls[3].pos.y + ' [m]')
                    else:
                        self.win.var_exec[4].SetLabel('height = ' + '%.2f' % self.balls[3].pos.y + ' [m]')
                    self.win.var_exec[0].SetLabel('V1 = ' + '%.2f' % self.balls[0].v.y + '[m/s]')
                    self.win.var_exec[1].SetLabel('V2 = ' + '%.2f' % self.balls[1].v.y + '[m/s]')
                    self.win.var_exec[2].SetLabel('V3 = ' + '%.2f' % self.balls[2].v.y + '[m/s]')
                    self.win.var_exec[3].SetLabel('V4 = ' + '%.2f' % self.balls[3].v.y + '[m/s]')
            else:
                while True:
                    rate(10)