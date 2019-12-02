from visual import *
from variables import *

class Conical:
    def __init__(self,window):
        self.win = window
        self.angle = self.win.Ctrls[0].GetValue()
        self.mass = self.win.Ctrls[1].GetValue()
        self.length = self.win.Ctrls[2].GetValue()
        self.theta = degree_to_rad * self.angle
        self.r = self.length * cos(self.theta)

    def prepare(self):
        self.win.scene.center=(0,self.r/3,0)
        self.Ring = ring(pos=(0,0,0),axis=(0,1,0),radius=self.r,thickness=self.r/100,color=color.blue)
        self.Thread = curve(pos=[(self.r,0,0),(0,self.r-self.r/10,0)])
        self.Ball = sphere(pos=(self.r,0,0),radius=self.r/10,color=color.red)
        self.T=2*pi*sqrt((self.length*cos(self.theta)/g))
        self.t=0
        self.dt=0.02

    def run(self):
        while True:
            if not self.win.simulation_stopped:
                rate(100)
                self.Thread.pos[0]=(cos((self.t/self.T)*2*pi)*self.r,0,sin((self.t/self.T)*2*pi)*self.r)
                self.Ball.pos=(cos((self.t/self.T)*2*pi)*self.r,0,sin((self.t/self.T)*2*pi)*self.r)
                self.t=self.t+self.dt
            else:
                rate(10)