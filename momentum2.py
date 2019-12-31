# -*- coding: utf-8 -*-
from physics import *
from visual import *
from variables import *


class Momentum2:

    def __init__(self, window):
        self.win = window

    def description(self):
        if self.win.PL:
            return u"Są cztery piłki.\nMożesz wybrać ich masy, a także wysokość pierwszej z nich.\n" \
               u"Oddalone są od siebie o metr.\n" \
               u"Spadają one pod wpływem grawitacji i odbijają się od podłoża\nco powoduje nabranie bardzo dużej" \
               u"wysokości przez najlżejszą kulkę\nJej wysokość widać u dołu ekranu."
        else:
            return "There are four balls\nYou can define their masses as height of the first ball\n" \
                   "Distance between them is one meter\n" \
                   "They fall beacause of the gravity force and bounce\nThis causes the lighttest ball to gain" \
                   "height\nwhich You can check at the bottom"

    def prepare(self):
        self.masses = [self.win.Ctrls[0].GetValue(), self.win.Ctrls[1].GetValue(), self.win.Ctrls[2].GetValue(),
                       self.win.Ctrls[3].GetValue()]
        self.height = self.win.Ctrls[4].GetValue()
        self.balls = []
        self.balls_alt = []
        if self.masses[0] > self.masses[1]:
            if self.masses[1] > self.masses[2]:
                if self.masses[2] > self.masses[3]:
                    r1 = 5*(log10(self.masses[0] / self.masses[3]) + 1)
                    r2 = 5*(log10(self.masses[1] / self.masses[3]) + 1)
                    r3 = 5*(log10(self.masses[2] / self.masses[3]) + 1)
                    r4 = 5
                else:
                    r1 = 5*(log10(self.masses[0] / self.masses[2]) + 1)
                    r2 = 5*(log10(self.masses[1] / self.masses[2]) + 1)
                    r3 = 5
                    r4 = 5*(log10(self.masses[3] / self.masses[2]) + 1)
            else:
                if self.masses[1] > self.masses[3]:
                    r1 = 5*(log10(self.masses[0] / self.masses[3]) + 1)
                    r2 = 5*(log10(self.masses[1] / self.masses[3]) + 1)
                    r3 = 5*(log10(self.masses[2] / self.masses[3]) + 1)
                    r4 = 5
                else:
                    r1 = 5*(log10(self.masses[0] / self.masses[1]) + 1)
                    r2 = 5
                    r3 = 5*(log10(self.masses[2] / self.masses[1]) + 1)
                    r4 = 5*(log10(self.masses[3] / self.masses[1]) + 1)
        else:
            if self.masses[0] > self.masses[2]:
                if self.masses[2] > self.masses[3]:
                    r1 = 5*(log10(self.masses[0] / self.masses[3]) + 1)
                    r2 = 5*(log10(self.masses[1] / self.masses[3]) + 1)
                    r3 = 5*(log10(self.masses[2] / self.masses[3]) + 1)
                    r4 = 5
                else:
                    r1 = 5 * (log10(self.masses[0] / self.masses[2]) + 1)
                    r2 = 5 * (log10(self.masses[1] / self.masses[2]) + 1)
                    r3 = 5
                    r4 = 5 * (log10(self.masses[3] / self.masses[2]) + 1)
            else:
                if self.masses[0] > self.masses[3]:
                    r1 = 5*(log10(self.masses[0] / self.masses[3]) + 1)
                    r2 = 5*(log10(self.masses[1] / self.masses[3]) + 1)
                    r3 = 5*(log10(self.masses[2] / self.masses[3]) + 1)
                    r4 = 5
                else:
                    r1 = 5
                    r2 = 5 * (log10(self.masses[1] / self.masses[0]) + 1)
                    r3 = 5 * (log10(self.masses[2] / self.masses[0]) + 1)
                    r4 = 5 * (log10(self.masses[3] / self.masses[0]) + 1)
        ball1 = sphere(pos=(150, self.height+r1, 0), radius=r1, color=color.blue)
        self.balls.append(ball1)
        ball2 = sphere(pos=(150, self.height+2*r1+r2, 0), radius=r2, color=color.blue)
        self.balls.append(ball2)
        ball3 = sphere(pos=(150, self.height+2*r1+2*r2+r3, 0), radius=r3, color=color.blue)
        self.balls.append(ball3)
        ball4 = sphere(pos=(150, self.height + 2 * r1 + 2 * r2 + 2 * r3 + r4, 0), radius=r4, color=color.blue)
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
            self.balls_alt[i].h = self.balls_alt[i].pos.y - self.balls_alt[i].radius

        self.win.scene.autoscale = False
        self.win.scene.range = 600
        road = box(pos=(0,0,0),size=(1000,1,10),color=color.red)
        self.win.scene.center = (0, 280, 0)
        self.t = 0
        if self.win.PL:
            self.win.var_exec[0].SetLabel(u'Wysokość2 = ' + '%.2f' % self.balls[3].pos.y + ' [m]')
            self.win.var_exec[1].SetLabel(u'Wysokość1 = ' + '%.2f' % self.balls_alt[3].pos.y + ' [m]')
        else:
            self.win.var_exec[0].SetLabel('Height2 = ' + '%.2f' % self.balls[3].pos.y + ' [m]')
            self.win.var_exec[1].SetLabel('Height1 = ' + '%.2f' % self.balls_alt[3].pos.y + ' [m]')

    def run(self):
        dt = 0.005
        counter = 0
        while True:
            if not self.win.simulation_stopped:
                if self.t == 0:
                    sleep(2)
                rate(1000)
                for i in range(4):
                    self.balls[i].v = self.balls[i].v + self.balls[i].a * dt
                    self.balls_alt[i].v = self.balls_alt[i].v + self.balls_alt[i].a * dt
                for i in range(3):
                    if self.balls[i].pos.y > self.balls[i+1].pos.y - self.balls[i].radius - self.balls[i+1].radius:
                        momentum_conservation_principle(self.balls[i], self.balls[i+1])
                for i in range(3):
                    if self.balls[i].pos.y > self.balls[i+1].pos.y - self.balls[i].radius - self.balls[i+1].radius:
                        self.balls[i+1].pos.y = self.balls[i].pos.y + self.balls[i+1].radius + self.balls[i].radius + 0.001
                for i in range(4):
                    if self.balls[i].pos.y < 0 + self.balls[i].radius:
                        self.balls[i].v = -self.balls[i].v
                    if self.balls_alt[i].pos.y < 0 + self.balls_alt[i].radius:
                        self.balls_alt[i].v.y = sqrt(2*g*self.balls_alt[i].h)
                for i in range(4):
                    self.balls[i].pos = self.balls[i].pos + self.balls[i].v * dt
                    self.balls_alt[i].pos = self.balls_alt[i].pos + self.balls_alt[i].v * dt
                self.t = self.t + dt
                counter = counter + 1
                if counter % 50 == 0:
                    if self.win.PL:
                        self.win.var_exec[0].SetLabel(u'Wysokość2 = ' + '%.2f' % self.balls[3].pos.y + ' [m]')
                        self.win.var_exec[1].SetLabel(u'Wysokość1 = ' + '%.2f' % self.balls_alt[3].pos.y + ' [m]')
                    else:
                        self.win.var_exec[0].SetLabel('Height2 = ' + '%.2f' % self.balls[3].pos.y + ' [m]')
                        self.win.var_exec[1].SetLabel('Height1 = ' + '%.2f' % self.balls_alt[3].pos.y + ' [m]')
            else:
                while True:
                    rate(10)