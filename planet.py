from visual import *
from variables import *

class Planet:
    def __init__(self, window):
        self.win = window
    def prepare(self):

        self.sun = sphere(pos=(0, 0, 0), radius=10 ** 10, color=color.yellow)
        self.percent = self.win.sc1.GetValue()
        self.T = curve(color=color.magenta)
        self.planet = sphere(pos=(150 * (10 ** 9), 0, 0), radius=4.5 * 10 ** 9, color=color.magenta)
        self.win.scene.autoscale = False
        self.win.scene.range = 10**11*4
        self.planet.vel = vector(0, 22000, 0)

    def run(self):
        t=0
        dt = 3600
        while self.win.simulation.mode == 'Planet':
            if self.win.simulation_stopped == False:
                rate(1000)
                a = vector(-G * M * (self.planet.pos / (mag(self.planet.pos) ** 3)))
                self.planet.vel = self.planet.vel + a * dt
                self.planet.pos = self.planet.pos + self.planet.vel * dt
                self.T.append(pos=self.planet.pos,retain = 30000)
                t += dt
                if t % 86400 == 0:
                    self.win.var1.SetLabel('Days: ' + '%d' % (t/86400))
            else:
                rate(10)

