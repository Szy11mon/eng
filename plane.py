from visual import *
from variables import *

class Plane:
    dist = 0
    def __init__(self,window):
        self.win =window

    def description(self):
        text(text="This is simple inclined plane\nAngle defines how steep the plane is"
                  "\nYou can also define mass of the block and plane length\nFriction is a coefficient between 0 and 1"
                  "\nthat says how much the floor reacts on block\nAir resistance is also a coefficient"
                  "\nwhich defines how much the air influences acceleration ",
             align='center', depth=-0.2, color=color.green)

    def prepare(self):
        self.angle = self.win.Ctrls[0].GetValue()
        self.mass = self.win.Ctrls[1].GetValue()
        self.length = self.win.Ctrls[2].GetValue()
        self.friction = self.win.Ctrls[3].GetValue()
        self.air_res = self.win.Ctrls[4].GetValue()
        self.win.scene.autoscale = False
        self.win.scene.range = self.length
        self.theta = degree_to_rad * self.angle
        k = sqrt(self.length)*2
        self.inclinedPlane = box(pos=(0, 0, 0), size=(self.length, 0.02*k, 0.02*k), color=color.green, opacity=0.3)
        self.cart = box(size=(0.2*k, 0.12*k, 0.06*k), color=color.blue)
        #self.sc1.GetValue() * 0.01745329252) < self.sc4.GetValue()

        # Define parameters
        self.cart.m = self.mass  # mass of cart in kg
        self.cart.pos = vector(self.length / 2. - 0.1*k, 0.06*k,
                          0)  # initial position of the cart in(x, y, z) form, units are in meters
        self.cart.v = vector(0, 0, 0)  # initial velocity of car in (vx, vy, vz) form, units are m/s

        # angle of inclined plane relative to the horizontal

        # rotate the cart and the inclined plane based on the specified angle
        self.inclinedPlane.rotate(angle=self.theta, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
        self.cart.rotate(angle=self.theta, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
        self.FN = arrow(pos=self.cart.pos, axis=(0.2*k, 0, 0), shaftwidth=0.01*self.length,color = color.red)
        self.FY = arrow(pos=self.cart.pos, axis=(0.2*k, 0, 0), shaftwidth=0.01*self.length,color=color.yellow)
        self.FT = arrow(pos=self.cart.pos - (-0.1*k,0.05*k,0), axis=(0.2*k*self.friction*(1/tan(self.theta)), 0, 0), shaftwidth=0.01*self.length,color=color.magenta)
        self.FP = arrow(pos=self.cart.pos + (0.1*k, 0.05 * k, 0), axis=(0, 0, 0),shaftwidth=0.01*self.length,color=color.cyan)
        self.FX = arrow(pos=self.cart.pos + (0.1*k,0,0), axis=(0.2 * k, 0, 0), shaftwidth=0.01 * self.length)
        self.FN.rotate(angle=degree_to_rad * (self.angle + 90), origin=self.cart.pos,axis=vector(0,0,1))
        self.FY.rotate(angle=degree_to_rad * (self.angle + 270), origin=self.cart.pos, axis=vector(0, 0, 1))
        self.FT.rotate(angle = self.theta, origin=self.cart.pos, axis=vector(0, 0, 1))
        self.FP.rotate(angle=self.theta, origin=self.cart.pos, axis=vector(0, 0, 1))
        self.FX.rotate(angle=degree_to_rad * (self.angle + 180), origin=self.cart.pos , axis=vector(0, 0, 1))
        self.Fnet = norm(self.inclinedPlane.axis)
        self.Fnet.mag = self.cart.m * g * (sin(self.theta) - cos(self.theta) * self.friction)
        self.arr_len = 0.2*k - 0.2*k*self.friction*(1/tan(self.theta))
        self.arr_len = -self.FX.axis.x - self.FT.axis.x

        # Define time parameters
        self.t = 0  # starting time
        self.dt = 0.0005  # time step units are s

    def run(self):
        counter = 0
        while self.dist < self.length:  # while the cart's y-position is greater than 0 (above the ground)
            if self.win.simulation_stopped == False:
                rate(1000)

                Fnet = norm(self.inclinedPlane.axis)
                # set the magnitude to the component of the gravitational force parallel to the inclined plane
                Fnet.mag = self.cart.m * g * (sin(self.theta) - cos(self.theta) * self.friction) - self.air_res * self.cart.v.mag2

                # Newton's 2nd Law
                self.cart.v = self.cart.v + (Fnet / self.cart.m * self.dt)

                # Position update
                self.cart.pos = self.cart.pos - self.cart.v * self.dt
                self.FN.pos = self.FN.pos - self.cart.v * self.dt
                self.FY.pos = self.FY.pos - self.cart.v * self.dt
                self.FT.pos = self.FT.pos - self.cart.v * self.dt
                self.FX.pos = self.FX.pos - self.cart.v * self.dt
                tmp = ((self.Fnet.mag - Fnet.mag) / self.Fnet.mag) * self.arr_len
                self.FP.axis = (tmp,tmp/self.FX.axis.x*self.FX.axis.y,0)
                self.FP.pos = self.FP.pos - self.cart.v * self.dt
                counter = counter +1
                self.dist = self.dist + self.cart.v.mag*self.dt
                # Time update
                if counter%50 is 0:
                    self.win.var_exec[0].SetLabel('time(s) = ' + '%.2f'%self.t)
                    self.win.var_exec[1].SetLabel('V(m/s) = ' + '%.2f' % self.cart.v.mag)
                    self.win.var_exec[2].SetLabel('a(m/s^2) = ' + '%.2f' % (Fnet.mag/self.mass))
                self.t = self.t + self.dt
            else:
                while True:
                    rate(10)
