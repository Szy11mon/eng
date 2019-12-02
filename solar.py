from visual import *
from variables import *

class Solar:
    def __init__(self, window):
        self.win = window
        self.percent = self.win.Ctrls[0].GetValue()

    def prepare(self):
        self.sun = sphere(pos=(0, 0, 0), radius=10 ** 10, color=color.yellow)
        self.T = [curve(color=color.magenta), curve(color=color.green), curve(color=color.blue), curve(color=color.red)]
        self.planet1 = sphere(pos=(70 * (10 ** 9), 0, 0), radius=3 * 10 ** 9, color=color.magenta)
        self.planet2 = sphere(pos=(110 * (10 ** 9), 0, 0), radius=4 * 10 ** 9, color=color.green)
        self.planet3 = sphere(pos=(150 * (10 ** 9), 0, 0), radius=4.5 * 10 ** 9, color=color.blue)
        self.planet4 = sphere(pos=(250 * (10 ** 9), 0, 0), radius=3 * 10 ** 9, color=color.red)

        self.planet1.vel = vector(0, 47000, 0)
        self.planet2.vel = vector(0, 35000, 0)
        self.planet3.vel = vector(0, (self.percent/100)*30000, 0)
        self.planet4.vel = vector(0, 24000, 0)

        self.L = [self.planet1, self.planet2, self.planet3, self.planet4]

    def run(self):
        t=0
        dt = 3600
        while self.win.simulation.mode == 'Solar':
            if self.win.simulation_stopped == False:
                rate(1000)
                for i in range(0, 4):
                    a = vector(-G * M * (self.L[i].pos / (mag(self.L[i].pos) ** 3)))
                    self.L[i].vel = self.L[i].vel + a * dt
                    self.L[i].pos = self.L[i].pos + self.L[i].vel * dt
                    self.T[i].append(pos=self.L[i].pos,retain = 30000)
                t += dt
                if t % 86400 == 0:
                    self.win.var_exec[0].SetLabel('Days: ' + '%d' % (t/86400))
            else:
                rate(10)

