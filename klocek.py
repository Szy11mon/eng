from visual import *
from variables import *
import wx

class Block:

    def __init__(self,window):
        self.win = window
        self.V0 = self.win.Ctrls[0].GetValue()
        self.mass = self.win.Ctrls[1].GetValue()

    def prepare(self):
        scale = log10(self.mass/1)+1
        print scale
        self.win.scene.autoscale = False
        self.win.scene.range = 21
        self.block1 = box(pos=(0, 1*scale, 0), size=(2*scale, 2*scale, 0.06), color=color.blue)
        self.block2 = box(pos=(-10,1,0),size=(2,2,0.06),color=color.green)
        self.road = box(pos=(0,0,0),size=(40,0.05,0.05),color=color.red)
        self.wall = box(pos=(-20, 10, 0), size=(0.05, 20, 0.05), color=color.red)
        self.win.scene.center = (0,8,0)
        self.block1.v = vector(-self.V0, 0, 0)
        self.block2.v = vector(0,0,0)

    def run(self):
        t = 0
        dt = 0.005
        counter=0
        self.win.var_exec[0].SetLabel('hits: 0')
        while True:
            if self.win.simulation_stopped == False:
                rate(1000)
                if self.block1.pos.x < self.block2.pos.x + 1+(self.block1.size.x/2):
                    counter+=1
                    tmp = self.block1.v
                    self.block1.v = ((self.mass - 1)/(self.mass+1))*self.block1.v + (2/(self.mass+1))*self.block2.v
                    self.block2.v = (2*self.mass/(1+self.mass))*tmp + ((1-self.mass)/(1+self.mass))*self.block2.v
                    self.win.var_exec[0].SetLabel('hits: ' + '%d' % counter)
                if self.block2.pos.x < -19:
                    counter +=1
                    self.win.var_exec[0].SetLabel('hits: ' + '%d' % counter)
                    self.block2.v = -self.block2.v
                self.block1.pos=self.block1.pos + self.block1.v * dt
                self.block2.pos=self.block2.pos + self.block2.v * dt
                t = t + dt
            else:
                while True:
                    rate(10)