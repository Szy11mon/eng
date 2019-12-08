from visual import *
from variables import *

class Pendulum:
    def __init__(self,window):
        self.win = window

    @staticmethod
    def description():
        text(text="This is a simulation of simple pendulum\nFirts of them works according to physics\n"
                  "\nthe second one uses sin(a)=a\nYou can choose length of the thread\nand starting inclination"
                  "\nThe simulation displays both angles during its run",
             align='center', depth=-0.2, color=color.green)

    def prepare(self):
        self.angle = self.win.Ctrls[0].GetValue()
        self.length = self.win.Ctrls[1].GetValue()
        self.g = self.win.Ctrls[2].GetValue()
        self.line1=curve(pos=[(-5,0,0),(-1,0,0),(-3,0,0),(-3,-6,0)])
        self.theta = toRadian(self.angle)
        self.win.scene.autoscale = False
        self.win.scene.range = 12

        self.ba1=sphere(pos=(self.length*np.sin(self.theta)-3,-self.length*np.cos(self.theta),0),radius=0.2,color=color.red)
        self.line3=curve(pos=[(-3,0,0),self.ba1.pos])


        self.line2=curve(pos=[(1,0,0),(5,0,0),(3,0,0),(3,-6,0)])
        self.ba2=sphere(pos=(self.length*np.sin(self.theta)+3,-self.length*np.cos(self.theta),0),radius=0.2,color=color.red)
        self.line4=curve(pos=[(3,0,0),self.ba2.pos])

    def run(self):
        V1 = 0
        V2 = 0
        counter = 0
        dt = 0.0005
        fi1 = self.theta
        fi2 = self.theta
        while true:
            if self.win.simulation_stopped == False:
                rate(1000)
                a1=(-self.g/self.length)*sin(fi1)
                print sin(fi1)
                print fi1
                V1=V1+a1*dt
                fi1=fi1+V1*dt
                self.ba1.pos=(self.length*np.sin(fi1)-3,-self.length*np.cos(fi1),0)
                self.line3.pos=((-3,0,0),self.ba1.pos)
                a2 = (-self.g / self.length) * fi2
                print sin(fi2)
                print fi2
                V2 = V2 + a2 * dt
                fi2 = fi2 + V2 * dt
                self.ba2.pos = (self.length * np.sin(fi2)+3, -self.length * np.cos(fi2), 0)
                self.line4.pos = ((3, 0, 0), self.ba2.pos)
                counter +=1
                if counter%50 is 0:
                    self.win.var_exec[0].SetLabel('angle2 = ' + '%.2f'% abs(toAngle(fi1)))
                    self.win.var_exec[1].SetLabel('angle1 = ' + '%.2f' % abs(toAngle(fi2)))
            else:
                while True:
                    rate(10)