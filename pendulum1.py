# -*- coding: utf-8 -*-
from visual import *
from variables import *
import numpy as np


class Pendulum:
    def __init__(self, window):
        self.win = window

    def description(self):
        if self.win.PL:
            return u"Symulacja prostego wahadła matematycznego.\nRuch pierwszego obliczony jest na w " \
               u"stadardowy sposób,\nnatomiast drugie używa uproszczenia sin(a) = a.\nMożna wybrać początkowe wychylenie," \
               u"a także długość nici.\nW trakcie symulacji, u dołu ekranu, można śledzić wychylenie obydwu wahadeł"
        else:
            return "This is a simulation of simple pendulum.\nFirts of them works normally,\n" \
                   "the second one uses sin(a)=a.\nYou can choose length of the thread\nand starting inclination." \
                   "\nThe simulation displays both angles during its run."

    def prepare(self):
        self.angle = self.win.Ctrls[0].GetValue()
        self.length = self.win.Ctrls[1].GetValue()
        self.g = self.win.Ctrls[2].GetValue()
        self.air_res = self.win.Ctrls[3].GetValue()
        self.line1=curve(pos=[(-1.5,0,0),(-0.5,0,0),(-1,0,0),(-1,-2,0)],radius=0.01)
        if self.angle == 180:
            self.theta = np.pi
        else:
            self.theta = toRadian(self.angle)

        self.ba1=sphere(pos=(self.length*np.sin(self.theta)-1,-self.length*np.cos(self.theta),0.02),radius=0.1,color=color.red)
        self.line3=curve(pos=[(-1,0,0),self.ba1.pos],radius=0.01)

        txt = label(pos=(1, 0.1, 0), text='sin(a) = a',box=False, height=20)
        time_axis = arrow(pos=(-2.4, 0.5, 0), axis=(4.8, 0, 0), shaftwidth=0.015, opacity=1)
        if self.win.PL:
            time_text = label(pos=(0, 0.38, 0), text='czas', box=False, height=25)
        else:
            time_text = label(pos=(0, 0.38, 0), text='time', box=False, height=25)
        self.line2=curve(pos=[(0.5,0,0),(1.5,0,0),(1,0,0),(1,-2,0)], radius=0.01)
        self.ba2=sphere(pos=(self.length*np.sin(self.theta)+1,-self.length*np.cos(self.theta),0.02),radius=0.1,color=color.red)
        self.line4=curve(pos=[(1,0,0),self.ba2.pos], radius=0.01)
        self.fi1 = self.theta
        self.fi2 = self.theta
        self.V1 = 0
        self.V2 = 0
        self.counter = 0

    def run(self):
        dt = 0.0005
        graph1 = curve(color=color.blue, radius=0.015)
        # graph2 = curve(color=color.green)
        while True:
            if not self.win.simulation_stopped:
                rate(1000)
                a1 = (-self.g / self.length) * sin(self.fi1) - (self.air_res * self.V1)
                self.V1 = self.V1 + a1 * dt
                self.fi1 = self.fi1 + self.V1 * dt
                self.ba1.pos = (self.length * np.sin(self.fi1) - 1, -self.length * np.cos(self.fi1), 0)
                self.line3.pos = ((-1, 0, 0), self.ba1.pos)
                a2 = (-self.g / self.length) * self.fi2 - (self.air_res * self.V2)
                self.V2 = self.V2 + a2 * dt
                self.fi2 = self.fi2 + self.V2 * dt
                self.ba2.pos = (self.length * np.sin(self.fi2) + 1, -self.length * np.cos(self.fi2), 0)
                self.line4.pos = ((1, 0, 0), self.ba2.pos)
                graph1.append(pos=vector(-2.2 + self.counter * 0.0001, (self.fi1 - self.fi2) * 0.05 + 1, 0))
                # graph1.append(pos=vector(-2.2 + self.counter * 0.0001, self.fi1 / hmax * 0.2 + 1.2, 0))
                # graph2.append(pos=vector(-2.2 + self.counter * 0.0001, self.fi2 / hmax * 0.2 + 0.4, 0))
                self.counter += 1
                if self.counter == 45000:
                    self.counter = 0
                    graph1.append(pos=vector(-2.2 + self.counter * 0.0001, (self.fi1 - self.fi2) * 0.05 + 1, 0), retain=1)
                    # graph2.append(pos=vector(-2.2 + self.counter * 0.0001, sin(self.fi2) / hmax * 0.2 + 0.4, 0), retain=1)
                symbol = '[' + u"\u00b0" + ']'
                if self.counter % 50 is 0:
                    if self.win.PL:
                        self.win.var_exec[1].SetLabel(u'kąt1 = ' + '%.2f' % (toAngle(self.fi1)) + symbol)
                        self.win.var_exec[0].SetLabel(u'kąt2 = ' + '%.2f' % (toAngle(self.fi2)) + symbol)
                    else:
                        self.win.var_exec[1].SetLabel('angle1 = ' + '%.2f' % (toAngle(self.fi1)) + symbol)
                        self.win.var_exec[0].SetLabel('angle2 = ' + '%.2f' % (toAngle(self.fi2)) + symbol)
            else:
                while True:
                    rate(10)
