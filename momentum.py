from visual import *
from variables import *

class Momentum:

    def __init__(self,window):
        self.win = window
        self.V0 = self.win.Ctrls[0].GetValue()
        self.mass1 = self.win.Ctrls[1].GetValue()
        self.mass2 = self.win.Ctrls[2].GetValue()
        self.number = int(self.win.Ctrls[3].GetValue())

    def prepare(self):
        self.balls=[]
        if self.mass1 > self.mass2:
            r1 = 2*(log10(self.mass1 / self.mass2) + 1)
            r2 = 2
        else:
            r2 = 2 * (log10(self.mass2 / self.mass1) + 1)
            r1 = 2
        ball1 = sphere(pos=(-50,r1, 0), radius = r1, color=color.blue)
        ball1.v = vector(self.V0,0,0)
        ball1.m=self.mass1
        self.balls.append(ball1)
        for i in range(self.number):
            ball = sphere(pos=(-50+(i+1)*15,r2,0),radius=r2,color=color.green)
            ball.m = self.mass2
            ball.v = vector(0,0,0)
            self.balls.append(ball)
        self.win.scene.autoscale = False
        self.win.scene.range = 54
        self.road = box(pos=(0,0,0),size=(110,0.1,5),color=color.red)
        self.win.scene.center = (0,8,0)

    def run(self):
        t=0
        dt=0.005
        while True:
            if self.win.simulation_stopped == False:
                rate(1000)
                for i in range(self.number):
                    if self.balls[i].pos.x > self.balls[i+1].pos.x - self.balls[i].radius -self.balls[i+1].radius:
                        m1=self.balls[i].m
                        m2=self.balls[i+1].m
                        tmp = self.balls[i].v
                        print tmp
                        self.balls[i].v = ((m1 - m2)/(m1+m2))*self.balls[i].v + (2*m2/(m1+m2))*self.balls[i+1].v
                        self.balls[i+1].v = (2*m1/(m1+m2))*tmp + ((m2-m1)/(m1+m2))*self.balls[i+1].v
                for i in range(self.number+1):
                    self.balls[i].pos=self.balls[i].pos + self.balls[i].v * dt
                t = t + dt
            else:
                while True:
                    rate(10)