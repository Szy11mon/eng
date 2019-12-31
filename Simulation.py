from rzut import *
from plane import *
from klocek import *
from helixes import *
from solar import *
from stozkowe import *
from pendulum1 import *
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
        self.win.description.SetLabel(self.sim.description())

    def change_mode(self, mode):
        self.win.mode_changed = True
        self.mode = mode
        if self.mode == 'Helix':
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

    def run(self):
        self.win.mode_changed = False
        self.win.description.Hide()
        for i in self.win.variants:
            i.Hide()
        if not self.win.same_sim:
            self.win.set_display()
            self.win.scene.background = color.black
            self.sim.prepare()
            self.win.simulation_started = True
            self.sim.run()
        else:
            self.win.scene.delete()
            self.win.scene_destroyed = True
            self.win.set_display()
            self.win.scene.background = color.black
            # self.reset()
            self.sim.prepare()
            self.sim.run()

    def resume(self):
        self.sim.run()

