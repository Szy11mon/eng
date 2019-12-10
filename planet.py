from visual import *
from variables import *

class Planet:
    def __init__(self, window):
        self.win = window

    @staticmethod
    def description():
        return "This simulation shows a single planet\nYou can"

    def prepare(self):
        self.sun = sphere(pos=(0, 0, 0), radius=10 ** 10, color=color.yellow)
        self.percent = self.win.Ctrls[1].GetValue()
        self.T = curve(color=color.magenta)
        self.planet = sphere(pos=(self.percent*70 * (10 ** 7), 0, 0), radius=4.5 * 10 ** 9, color=color.magenta)
        self.win.scene.autoscale = False
        self.win.scene.range = 10**11*4
        self.planet.vel = vector(0, self.win.Ctrls[0].GetValue(), 0)

    def run(self):
        t=0
        dt = 3600
        while self.win.simulation.mode == 'Planet':
            if self.win.simulation_stopped == False:
                rate(1000)
                a = vector(-self.win.Ctrls[2].GetValue()/100*G * self.win.Ctrls[3].GetValue()/100*M * (self.planet.pos / (mag(self.planet.pos) ** 3)))
                self.planet.vel = self.planet.vel + a * dt
                self.planet.pos = self.planet.pos + self.planet.vel * dt
                self.T.append(pos=self.planet.pos, retain=30000)
                t += dt
                if t % 86400 == 0:
                    self.win.var_exec[0].SetLabel('Days: ' + '%d' % (t/86400))
                    self.win.var_exec[1].SetLabel('V(km/s) = ' + '%.2f' % (self.planet.vel.mag/1000))
            else:
                rate(10)

