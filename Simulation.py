from rzut import *
from plane import *
from klocek import *
from helixes import *
from solar import *
from stozkowe import *
from pendulum import *
from momentum import *
from momentum2 import *
from planet import *


class Simulation(object):
    def __init__(self, window,mode=''):
        self.win=window
        self.mode=mode

    def changeMode(self,mode):
        self.mode = mode

    def description(self):
        str = self.mode + '(self.win)'
        self.sim = eval(str)
        self.win.scene.delete()
        self.win.SetDisplay()
        self.sim.description()

    def run(self):
        self.win.scene.delete()
        self.win.SetDisplay()
        self.win.scene.background = color.black
        self.win.scene.center = (0, 0, 0)
        str = self.mode + '(self.win)'
        self.sim = eval(str)
        self.sim.prepare()
        self.win.simulation_started = True
        self.sim.run()

    def resume(self):
        self.sim.run()

