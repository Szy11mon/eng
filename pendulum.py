# -*- coding: utf-8 -*-
from visual import *
from variables import *
import numpy as np

class Pendulum:
    def __init__(self,window):
        self.win = window

    @staticmethod
    def descriptionENG():
        return "This is a simulation of simple pendulum\nFirts of them works according to physics\n"\
               "the second one uses sin(a)=a\nYou can choose length of the thread\nand starting inclination"\
               "\nThe simulation displays both angles during its run"

    @staticmethod
    def descriptionPL():
        return u"Symulacja prostego wahadła matematycznego\nRuch pierwszego obliczony jest na podstawie równania" \
               u"różniczkowego\nnatomiast drugie używa uproszczenia sin(a) = a\n Możesz wybrać początkowe wychylenie," \
               u"a także długość nici\nW trakcie symulacji możesz śledzić wychylenie obydwu wahadeł"

    def prepare(self):
        self.angle = self.win.Ctrls[0].GetValue()
        self.length = self.win.Ctrls[1].GetValue()
        self.g = self.win.Ctrls[2].GetValue()
        self.air_res = self.win.Ctrls[3].GetValue()
        self.line1=curve(pos=[(-1.5,0,0),(-0.5,0,0),(-1,0,0),(-1,-2,0)])
        if self.angle == 180:
            self.theta = np.pi
        else:
            self.theta = toRadian(self.angle)

        self.ba1=sphere(pos=(self.length*np.sin(self.theta)-1,-self.length*np.cos(self.theta),0),radius=0.1,color=color.red)
        self.line3=curve(pos=[(-1,0,0),self.ba1.pos])

        txt = label(pos=(1, 0.1, 0), text='sin(a) = a',box=False, height=20)
        time_axis = arrow(pos=(-2.4, 0.9, 0), axis=(4.8, 0, 0), shaftwidth=0.03, opacity=1)
        txt_graph = text(pos=(-2.3, 0.2, 0), text='sin(a)=a', box=False, height=0.1, depth=0.01, axis=(0, 1, 0))
        if self.win.PL:
            time_text = label(pos=(0, 0.75, 0), text='czas', box=False, height=25)
        else:
            time_text = label(pos=(0, 0.75, 0), text='time', box=False, height=25)
        self.line2=curve(pos=[(0.5,0,0),(1.5,0,0),(1,0,0),(1,-2,0)])
        self.ba2=sphere(pos=(self.length*np.sin(self.theta)+1,-self.length*np.cos(self.theta),0),radius=0.1,color=color.red)
        self.line4=curve(pos=[(1,0,0),self.ba2.pos])

    def run(self):
        V1 = 0
        V2 = 0
        counter = 0
        dt = 0.0005
        fi1 = self.theta
        fi2 = self.theta
        graph1 = curve(color=color.blue)
        graph2 = curve(color=color.green)
        if self.angle < 90:
            hmax = abs(sin(self.theta))
        else:
            hmax =1
        print hmax
        while true:
            if self.win.simulation_stopped is False:
                rate(1000)
                a1 = (-self.g/self.length)*sin(fi1) - (self.air_res * V1)
                V1 = V1 + a1 * dt
                fi1 = fi1+V1*dt
                self.ba1.pos = (self.length*np.sin(fi1)-1, -self.length*np.cos(fi1), 0)
                self.line3.pos = ((-1, 0, 0), self.ba1.pos)
                a2 = (-self.g / self.length) * fi2 - (self.air_res * V2)
                V2 = V2 + a2 * dt
                fi2 = fi2 + V2 * dt
                self.ba2.pos = (self.length * np.sin(fi2)+1, -self.length * np.cos(fi2), 0)
                self.line4.pos = ((1, 0, 0), self.ba2.pos)
                graph1.append(pos=vector(-2.2+counter*0.0001, sin(fi1)/hmax*0.2+1.2, 0))
                graph2.append(pos=vector(-2.2+counter*0.0001, sin(fi2)/hmax*0.2+0.4, 0))
                counter += 1
                if counter == 48000:
                    counter = 0
                    graph1.append(pos=vector(-2.2 + counter * 0.0001, sin(fi1) / hmax * 0.2 + 1.2, 0), retain=1)
                    graph2.append(pos=vector(-2.2 + counter * 0.0001, sin(fi2) / hmax * 0.2 + 0.4, 0), retain=1)
                symbol = '[' + u"\u00b0" + ']'
                if counter%50 is 0:
                    if self.win.PL:
                        self.win.var_exec[1].SetLabel(u'kąt1 = ' + '%.2f'% abs(toAngle(fi1)) + symbol)
                        self.win.var_exec[0].SetLabel(u'kąt2 = ' + '%.2f' % abs(toAngle(fi2)) + symbol)
                    else:
                        self.win.var_exec[1].SetLabel('angle1 = ' + '%.2f' % abs(toAngle(fi1)) + symbol)
                        self.win.var_exec[0].SetLabel('angle2 = ' + '%.2f' % abs(toAngle(fi2)) + symbol)
            else:
                while True:
                    rate(10)