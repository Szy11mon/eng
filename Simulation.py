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
    def __init__(self, window, mode=''):
        self.win = window
        self.mode = mode

    def reset(self):
        for i in self.win.scene.objects:
            i.visible = False

    def changeMode(self,mode):
        if self.mode != mode:
            self.mode = mode
            code = self.mode + '(self.win)'
            self.sim = eval(code)
            self.win.simulation_stopped = True
            self.win.description.SetLabel(self.sim.description())
            self.win.description.Show()
            if self.win.scene:
                self.win.scene.delete()
            self.win.same_sim = False
        else:
            pass

    def run(self):
        self.win.description.Hide()
        if not self.win.same_sim:
            self.win.SetDisplay()
            self.win.scene.background = color.black
            self.sim.prepare()
            self.win.simulation_started = True
            self.sim.run()
        else:
            self.reset()
            self.sim.prepare()
            self.sim.run()

    def resume(self):
        self.sim.run()

