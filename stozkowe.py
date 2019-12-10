from visual import *
from variables import *

class Conical:
    def __init__(self,window):
        self.win = window

    @staticmethod
    def description():
        return "This is conical pendulum\nYou can define angle,length and mass\nYou can "\
               "see that the mass doesn't affect the period"

    def prepare(self):
        self.angle = self.win.Ctrls[0].GetValue()
        self.mass = self.win.Ctrls[1].GetValue()
        self.length = self.win.Ctrls[2].GetValue()
        self.theta = degree_to_rad * self.angle
        self.r = self.length * cos(self.theta)
        self.win.scene.center=(0,self.r/3,0)
        self.Ring = ring(pos=(0,0,0),axis=(0,1,0),radius=self.r,thickness=self.r/100,color=color.blue)
        self.Thread = curve(pos=[(self.r,0,0),(0,self.r-self.r/10,0)])
        self.Ball = sphere(pos=(self.r,0,0),radius=self.r/10,color=color.red)
        self.T=2*pi*sqrt((self.length*cos(self.theta)/g))
        self.t=0
        self.dt=0.002

    def run(self):
        counter = 0
        while True:
            if not self.win.simulation_stopped:
                rate(1000)
                self.Thread.pos[0]=(cos((self.t/self.T)*2*pi)*self.r,0,sin((self.t/self.T)*2*pi)*self.r)
                self.Ball.pos=(cos((self.t/self.T)*2*pi)*self.r,0,sin((self.t/self.T)*2*pi)*self.r)
                if counter%50 is 0:
                    self.win.var_exec[0].SetLabel('x = ' + '%.2f' % self.Ball.pos.x)
                    self.win.var_exec[1].SetLabel('z = ' + '%.2f' % self.Ball.pos.z)
                self.t = self.t + self.dt
                counter += 1
            else:
                rate(10)