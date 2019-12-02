from visual import *

class Helixes:
    counter = 0
    def __init__(self,window):
        self.win = window
        self.k = self.win.Ctrls[0].GetValue()
        self.quantity = int(self.win.Ctrls[1].GetValue())
        self.mass = self.win.Ctrls[2].GetValue()

    def description(self):
        text(text='Number of helixes\nk is the elasticity factor',
             align='center', depth=-0.2, color=color.green)

    def prepare(self):
        self.ba1 = sphere(pos=(-50,0,0),radius=1,color=color.red)
        self.ba=[self.ba1]
        self.d=100/self.quantity
        i=1
        self.f=[]
        while (i<self.quantity):
            self.a=sphere(pos=(-50+i*self.d,0,0),radius=1,color=color.blue)
            self.a.vel=vector(0,0,0)
            self.ba.append(self.a)
            self.f.append(self.a.vel)
            i=i+1
        self.ba2 = sphere(pos=(-50+i*self.d,0,0),radius=1,color=color.red)
        self.ba.append(self.ba2)
        self.f.append(vector(0,0,0))

        self.ba[1].pos=(self.ba[1].pos.x,20,self.ba[1].pos.z)
        self.ba[self.quantity-1].pos=(self.ba[self.quantity-1].pos.x,20,self.ba[1].pos.z)

        self.he1=helix(pos=self.ba[0].pos,axis=self.ba[1].pos-self.ba[0].pos-(1,0,0),radius=1,coils=3,thicknes=0.05,color=color.green)
        self.he=[self.he1]
        i=1
        while (i<self.quantity):
            self.h=helix(pos=self.ba[i].pos+(0.5,0,0),axis=self.ba[i+1].pos-self.ba[i].pos,radius=1,coils=3,thicknes=0.05,color=color.green)
            self.he.append(self.h)
            i=i+1
        self.t = 0
        self.dt=0.04

    def run(self):
        counter = 0
        while true:
            if self.win.simulation_stopped == False:
                Ek = 0
                Ep = 0
                rate(100)
                for i in range(0,self.quantity-1):
                    self.f[i]=self.k*(self.ba[i].pos+self.ba[i+2].pos)-2*self.ba[i+1].pos
                for i in range(1,self.quantity):
                    self.a=self.f[i-1]/self.mass
                    self.ba[i].vel=self.ba[i].vel+self.a*self.dt
                    self.ba[i].pos=self.ba[i].pos+self.ba[i].vel*self.dt
                for i in range(0,self.quantity):
                    self.he[i].pos=self.ba[i].pos
                    self.he[i].axis=self.ba[i+1].pos-self.ba[i].pos
                for i in range(1,self.quantity):
                    Ek += (self.mass * self.ba[i].vel.y**2)/2
                    Ep += (self.k * self.ba[i].pos.y ** 2)/2
                self.t = self.t + self.dt
                counter = counter + 1
                print 'Ek ' + str(Ek)
                print 'Ep ' + str(Ep)
                self.win.var_exec[0].SetLabel('Ep + Ek = ' + '%.2f'%(Ep + Ek))
                self.win.var_exec[1].SetLabel('Ep = ' + '%.2f' % Ep)
                self.win.var_exec[2].SetLabel('Ek = ' + '%.2f' % Ek)
            else:
                rate(10)