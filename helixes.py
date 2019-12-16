# -*- coding: utf-8 -*-
from visual import *

class Helixes:
    counter = 0
    def __init__(self,window):
        self.win = window

    def descriptionENG(self):
        return "There are two balls that don't move\nBalls are connected with helixes\nk is the elasticity factor"\
               "\nNumber means number of balls that move\nYou can also define mass of the balls\nDuring the simulation you will see"\
               "\nthe kinetic energy,potential energy and sum of the energy of all the balls\n" \
               "Possible starting positions of balls:"

    def descriptionPL(self):
        return u"Na krańcach są dwa słupki, które się nie poruszają\nŁączymy z nimi za pomocą sprężyn piłki, których liczbę można" \
               u"zdefiniować\nMożesz także zmienić masę kulek oraz współczynnik sprężystości k\n Na początku wychylamy kulki\n" \
               u"W trakcie symulacji widać Energie: potencjalną, kinetyczną i całkowitą\nMożliwości początkowego rozmieszczenia " \
               u"piłek:"

    def prepare(self):
        self.k = self.win.Ctrls[0].GetValue()
        self.quantity = int(self.win.Ctrls[1].GetValue()+1)
        self.mass = self.win.Ctrls[2].GetValue()
        self.variant = self.win.Ctrls[3].GetValue()
        self.air_res = self.win.Ctrls[4].GetValue()
        self.pole1 = box(pos=(-50, 0, 0), size=(2, 6, 1), color=color.red)
        self.ba=[self.pole1]
        self.d=100/self.quantity
        i=1
        self.f=[]
        while (i<self.quantity):
            self.a=sphere(pos=(-50+i*self.d,0,0),radius=1,color=color.blue)
            self.a.vel=vector(0,0,0)
            self.ba.append(self.a)
            self.f.append(self.a.vel)
            i=i+1
        self.pole2 = box(pos=(-50+i*self.d,0,0),size=(2,6,1),color=color.red)
        self.ba.append(self.pole2)
        self.f.append(vector(0,0,0))

        if self.variant == 1:
            self.ba[1].pos=(self.ba[1].pos.x,20,self.ba[1].pos.z)
        elif self.variant == 2:
            self.ba[1].pos = (self.ba[1].pos.x, 20, self.ba[1].pos.z)
            self.ba[-2].pos = (self.ba[-2].pos.x, -20, self.ba[-2].pos.z)
        elif self.variant == 3:
            self.ba[self.quantity/2].pos = (self.ba[self.quantity/2].pos.x, 20, self.ba[self.quantity/2].pos.z)
        self.he1=helix(pos=self.ba[0].pos,axis=self.ba[1].pos-self.ba[0].pos-(1,0,0),radius=1,coils=5,thicknes=0.4,color=color.green)
        self.he=[self.he1]
        i=1
        while i<self.quantity:
            self.h=helix(pos=self.ba[i].pos+(0.5,0,0),axis=self.ba[i+1].pos-self.ba[i].pos,radius=1,coils=5,thicknes=0.4,color=color.green)
            self.he.append(self.h)
            i=i+1
        self.t = 0
        self.dt=0.04

    def run(self):
        while true:
            if self.win.simulation_stopped is False:
                if self.t ==0:
                    sleep(2)
                Ek = 0
                Ep = 0
                rate(100)
                for i in range(0, self.quantity-1):
                    self.f[i] = self.k*(self.ba[i].pos+self.ba[i+2].pos)-2*self.ba[i+1].pos -\
                                self.air_res * self.ba[i+1].vel
                for i in range(1, self.quantity):
                    self.a = self.f[i-1]/self.mass
                    self.ba[i].vel = self.ba[i].vel+self.a*self.dt
                    self.ba[i].pos = self.ba[i].pos+self.ba[i].vel*self.dt
                for i in range(0, self.quantity):
                    self.he[i].pos = self.ba[i].pos
                    self.he[i].axis = self.ba[i+1].pos-self.ba[i].pos
                for i in range(1, self.quantity):
                    Ek += (self.mass * self.ba[i].vel.mag**2)/2
                for i in range(0, self.quantity):
                    Ep += (self.k * self.he[i].axis.y ** 2) / 2
                self.t = self.t + self.dt
                self.win.var_exec[0].SetLabel('Ep + Ek = ' + '%.2f'%(Ep + Ek))
                self.win.var_exec[1].SetLabel('Ep = ' + '%.2f' % Ep)
                self.win.var_exec[2].SetLabel('Ek = ' + '%.2f' % Ek)
            else:
                rate(10)