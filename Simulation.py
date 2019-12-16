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

    def description(self):
        if self.win.PL:
            self.win.description.SetLabel(self.sim.descriptionPL())
        else:
            self.win.description.SetLabel(self.sim.descriptionENG())

    def changeMode(self, mode):
        if self.mode != mode:
            self.win.mode_changed = True
            self.mode = mode
            if self.mode == 'Helixes':
                for i in self.win.variants:
                    i.Show()
            else:
                for i in self.win.variants:
                    i.Hide()
            code = self.mode + '(self.win)'
            self.sim = eval(code)
            self.win.simulation_stopped = True
            self.description()
            self.win.description.Show()
            if not self.win.scene_destroyed:
                self.win.scene.delete()
                self.win.scene_destroyed = True
            self.win.same_sim = False
        else:
            pass

    def run(self):
        self.win.mode_changed = False
        self.win.description.Hide()
        for i in self.win.variants:
            i.Hide()
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

