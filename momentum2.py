from visual import *
from variables import *

class Momentum2:

    def __init__(self,window):
        self.win = window
        self.mass1 = self.win.Ctrls[0].GetValue()
        self.mass2 = self.win.Ctrls[1].GetValue()
        self.mass3 = self.win.Ctrls[2].GetValue()
        self.height = self.win.Ctrls[3].GetValue()
        self.dist = self.win.Ctrls[4].GetValue()
        self.balls = []
    def prepare(self):
        if self.mass1 > self.mass2:
            if self.mass2 > self.mass3:
                r1 = 4*(log10(self.mass1 / self.mass3) + 1)
                r2 = 4*(log10(self.mass2 / self.mass3) + 1)
                r3 = 4
            else:
                r1 = 4 * (log10(self.mass1 / self.mass2) + 1)
                r2 = 4
                r3 = 4 * (log10(self.mass3 / self.mass2) + 1)
        else:
            r1 = 2
            r2 = 2 * (log10(self.mass2 / self.mass1) + 1)
            r3 = 2 * (log10(self.mass3 / self.mass1) + 1)
        ball1 = sphere(pos=(0,self.height, 0), radius = r1, color=color.blue)
        ball1.a = vector(0,-g,0)
        ball1.v = vector(0,0,0)
        ball1.m=self.mass1
        ball2 = sphere(pos=(0, self.height+self.dist, 0), radius=r2, color=color.blue)
        ball2.a = vector(0, -g, 0)
        ball2.v = vector(0, 0, 0)
        ball2.m = self.mass2
        ball3 = sphere(pos=(0, self.height+2*self.dist, 0), radius=r3, color=color.blue)
        ball3.a = vector(0, -g, 0)
        ball3.v = vector(0, 0, 0)
        ball3.m = self.mass3
        self.balls.append(ball1)
        self.balls.append(ball2)
        self.balls.append(ball3)
        self.win.scene.autoscale = False
        self.win.scene.range = 200
        road = box(pos=(0,0,0),size=(300,1,1),color=color.red)
        self.win.scene.center = (0,100,0)

    def run(self):
        t=0
        dt=0.005
        while True:
            if not self.win.simulation_stopped:
                rate(1000)
                for i in range(3):
                    self.balls[i].v = self.balls[i].v + self.balls[i].a * dt
                for i in range(2):
                    if self.balls[i].pos.y > self.balls[i+1].pos.y - self.balls[i].radius - self.balls[i+1].radius:
                        m1=self.balls[i].m
                        m2=self.balls[i+1].m
                        tmp = self.balls[i].v
                        print tmp
                        self.balls[i].v = ((m1 - m2)/(m1+m2))*self.balls[i].v + (2*m2/(m1+m2))*self.balls[i+1].v
                        self.balls[i+1].v = (2*m1/(m1+m2))*tmp + ((m2-m1)/(m1+m2))*self.balls[i+1].v
                    if self.balls[i].pos.y <0 + self.balls[i].radius:
                        self.balls[i].v = -self.balls[i].v
                for i in range(3):
                    self.balls[i].pos=self.balls[i].pos + self.balls[i].v * dt
                t = t + dt
            else:
                while True:
                    rate(10)