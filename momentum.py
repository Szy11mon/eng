# -*- coding: utf-8 -*-
from visual import *
from variables import *
from physics import *


class Momentum:

    def __init__(self, window):
        self.win = window

    @staticmethod
    def descriptionENG():
        return "There is one ball and up to 5 balls on its path\nYou can define velocity of the first ball\n"\
               "as well as its mass and mass of the remaining balls\nYou can see velocity of the first and second ball"

    @staticmethod
    def descriptionPL():
        return u"Jest jedna piłka na której drodze stoją kolejne piłki, których liczbę możesz wybrać\n" \
               u"Możesz także wybrać masę pierwszej kulki i wszystkich kolejnych\nU dołu ekranu możesz" \
               u"śledzić prędkość pierwszej i drugiej piłki"

    def prepare(self):
        self.V0 = self.win.Ctrls[0].GetValue()
        self.mass1 = self.win.Ctrls[1].GetValue()
        self.mass2 = self.win.Ctrls[2].GetValue()
        self.number = int(self.win.Ctrls[3].GetValue())
        self.balls=[]
        if self.mass1 > self.mass2:
            r1 = (log10(self.mass1 / self.mass2) + 1)
            r2 = 1
        else:
            r2 = (log10(self.mass2 / self.mass1) + 1)
            r1 = 1
        ball1 = sphere(pos=(-50, r1, 0), radius=r1, color=color.blue)
        ball1.v = vector(self.V0, 0, 0)
        ball1.m = self.mass1
        self.balls.append(ball1)
        for i in range(self.number):
            ball = sphere(pos=(-45 + (i+1)*(2*r2+0.7), r2, 0),radius=r2,color=color.green)
            ball.m = self.mass2
            ball.v = vector(0,0,0)
            self.balls.append(ball)
        self.win.scene.autoscale = False
        self.win.scene.range = 52
        road = box(pos=(0, 0, 0),size=(110, 0.1, 5), color=color.red)
        self.win.scene.center = (0, 8, 0)

    def run(self):
        t = 0
        dt = 0.005
        counter = 0
        while True:
            if not self.win.simulation_stopped:
                rate(1000)
                for i in range(self.number):
                    if self.balls[i].pos.x > self.balls[i+1].pos.x - self.balls[i].radius -self.balls[i+1].radius:
                        momentum_conservation_principle(self.balls[i], self.balls[i+1])
                for i in range(self.number+1):
                    self.balls[i].pos = self.balls[i].pos + self.balls[i].v * dt
                if counter % 50 == 0:
                    self.win.var_exec[0].SetLabel('V2 = ' + '%.2f' % self.balls[1].v.x + ' [m/s]')
                    self.win.var_exec[1].SetLabel('V1 = ' + '%.2f' % self.balls[0].v.x + ' [m/s]')
                t = t + dt
                counter = counter + 1
            else:
                while True:
                    rate(10)