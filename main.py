import wx  # wx.Frame etc
import os  # To get path for "Open file"
from Simulation import *
from visual import *
import numpy as np

class MainWindow(window):
    """
    This class is baseclass for MainWindow. MainWindow panels
    are implemented in their own classes. MainWindow implements
    filemenu and its functionality and sizers for different
    """
    # ID LIST FOR BUTTONS
    ID_RUN_BUTTON = wx.NewId()
    ID_PAUSE_BUTTON = wx.NewId()
    ID_TOOLBAR = wx.NewId()
    screen_size = wx.GetDisplaySize()

    # Simulation
    simulation = None
    simulation_speed = 0
    simulation_timestep = 0
    same_sim = False
    mode = ''
    frequency = 0

    # Flags
    toolbarheight = 10
    state_saved = False
    scene = None
    simulation_started = False
    simulation_stopped = False
    debug_mode = False

    # Datapanel
    statusbar = None
    button_list = None

    following = None

    var_start = []
    var_exec = []
    Ctrls = []
    variant = ''

    def __init__(self, title, debug=False):
        window.__init__(self, title="Dynamics", _make_panel=True, width = self.screen_size[0],
                        height = self.screen_size[1] ) # kw _make_panel=False

        self.fullscreen = True
        self.SetVariablesPanel()
        self.SetMenubar()

    def SetMenubar(self):
        filemenu = wx.Menu()

        menuItem = filemenu.Append(wx.ID_EXIT, "&Exit",
                                   "Terminate the program")
        self.win.Bind(wx.EVT_MENU, self.OnExit, menuItem)

        planeButton = wx.Button(self.panel, label='Inclined Plane', pos=(10, 40))

        planeButton.Bind(wx.EVT_BUTTON, self.OnPlane)

        pendulumButton = wx.Button(self.panel, label='Pendulum', pos=(10, 80))

        pendulumButton.Bind(wx.EVT_BUTTON, self.OnPendulum)

        throwButton = wx.Button(self.panel, label='Throw', pos=(10, 120))

        throwButton.Bind(wx.EVT_BUTTON, self.OnThrow)

        blockButton = wx.Button(self.panel, label='Block', pos=(10, 160))

        blockButton.Bind(wx.EVT_BUTTON, self.OnBlock)

        helixButton = wx.Button(self.panel, label='Helix', pos=(10, 200))

        helixButton.Bind(wx.EVT_BUTTON, self.OnHelix)

        solarButton = wx.Button(self.panel, label='Solar System', pos=(10, 240))

        solarButton.Bind(wx.EVT_BUTTON, self.OnSolar)

        conicalButton = wx.Button(self.panel, label='Conical Pendulum', pos=(10, 280))

        conicalButton.Bind(wx.EVT_BUTTON, self.OnConical)

        momentumButton = wx.Button(self.panel, label='Momentum', pos=(10, 320))

        momentumButton.Bind(wx.EVT_BUTTON, self.OnMomentum)

        momentum2Button = wx.Button(self.panel, label='Momentum2', pos=(10, 360))

        momentum2Button.Bind(wx.EVT_BUTTON, self.OnMomentum2)

        planetButton = wx.Button(self.panel, label='Planet', pos=(10, 400))

        planetButton.Bind(wx.EVT_BUTTON, self.OnPlanet)

        runButton = wx.Button(self.panel, label='RUN', pos=(10, 0))

        runButton.Bind(wx.EVT_BUTTON, self.OnRun)

        pauseButton = wx.Button(self.panel, label='PAUSE', pos=(120, 0))

        pauseButton.Bind(wx.EVT_BUTTON, self.OnPause)

        resumeButton = wx.Button(self.panel, label='RESUME', pos=(210, 0))

        resumeButton.Bind(wx.EVT_BUTTON, self.OnResume)

        menuBar = wx.MenuBar()

        menuBar.Append(filemenu, "&File")

        self.win.SetMenuBar(menuBar)
        if self.debug_mode:
            print("...done!")


    def SetVariablesPanel(self):
        self.simulation = Simulation(self)
        for i in range(5):
            self.var_start.append(wx.StaticText(self.panel, label='', pos=(0.08*self.screen_size[0], 0.04*(i+1)*self.screen_size[1])))
            self.var_start[i].Hide()
            self.Ctrls.append(wx.SpinCtrlDouble(self.panel, value='0', pos=(0.14*self.screen_size[0], 0.04*(i+1)*self.screen_size[1]), size=(60, -1)))
            self.Ctrls[i].Hide()
            self.var_exec.append(wx.StaticText(self.panel, label='', pos=((0.9-i*0.1)*self.screen_size[0], 0.86*self.screen_size[1])))
            self.var_exec[i].Hide()
        self.description = wx.StaticText(self.panel, label='Pick one simulation from the list', pos=(0.4*self.screen_size[0], 0.1*self.screen_size[1]))
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.description.SetFont(font)

    def OnExit(self, event):
        dlg = wx.MessageDialog(self.win,
                               "Do you really want to close this application?",
                               "Confirm Exit",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            exit()

    def OnRun(self, event):
        self.simulation_stopped = False
        if self.mode == self.simulation.mode:
            self.same_sim = True
        self.mode = self.simulation.mode
        self.simulation.run()

    def OnPause(self, event):
        if self.simulation is None or self.simulation_stopped == True:
            pass
        else:
            self.simulation_stopped = True

    def OnResume(self,event):
        if self.simulation is None or self.simulation_stopped == False:
            pass
        else:
            self.simulation_stopped = False
            self.simulation.resume()


    def SetDisplay(self):
        self.scene = display(window=self, x=0.2*self.screen_size[0], y=0, width=0.8*self.screen_size[0],
                             height=0.85*self.screen_size[1], autoscale=True, centre=vector(0,0,0))


    def OnPlane(self,event):
        symbol = 'Angle(' + u"\u00b0" + ')'
        self.SetLabels(self.var_start, symbol ,'Mass(kg)', 'Length(m)', 'Friction', 'Air Resistance')
        self.SetLabels(self.var_exec, 'time(s)', 'V(m/s)', 'a(m/s^2)', '')
        self.SetRanges((10, 80), (1, 100), (1, 100), (0, 1), (0, 1))
        self.SetDefaultValues(45, 10, 10, 0, 0)
        self.simulation.changeMode('Plane')

    def OnPendulum(self,event):
        symbol = 'Angle(' + u"\u00b0" + ')'
        self.SetLabels(self.var_start, symbol, 'Length(m)', 'g(m/s^2)')
        self.SetLabels(self.var_exec, 'angle2', 'angle1', '', '')
        self.SetRanges((10, 350), (1, 6), (0, 20))
        self.SetDefaultValues(45, 4, g)
        self.simulation.changeMode('Pendulum')

    def OnThrow(self,event):
        symbol = 'Angle(' + u"\u00b0" +')'
        self.SetLabels(self.var_start, symbol, 'Velocity(m/s)', 'Air Resistance')
        self.SetLabels(self.var_exec, 'x(m)', 'h(m)', 'Vy(m/s)', 'Vx(m/s)')
        self.SetRanges((10, 80), (10, 300), (0, 5))
        self.SetDefaultValues(45, 50, 0)
        self.simulation.changeMode('Throw')

    def OnBlock(self,event):
        self.SetLabels(self.var_start, 'V(m/s)', 'Mass(kg)',)
        self.SetLabels(self.var_exec, 'hits')
        self.SetRanges((1, 5), (1, 10**12))
        self.SetDefaultValues(1,100)
        self.simulation.changeMode('Block')

    def OnHelix(self,event):
        self.SetLabels(self.var_start, 'k', 'Number', 'Mass(kg)')
        self.SetLabels(self.var_exec, 'Ep + Ek', 'Ep', 'Ek')
        self.SetRanges((0, 1), (1, 30), (0, 30))
        self.SetDefaultValues(1, 1, 10)
        self.simulation.changeMode('Helixes')

    def OnSolar(self,event):
        self.SetLabels(self.var_start, "% of Earth's V")
        self.SetLabels(self.var_exec, 'Days')
        self.SetRanges((0, 200))
        self.SetDefaultValues(100)
        self.simulation.changeMode('Solar')

    def OnConical(self,event):
        symbol = 'Angle(' + u"\u00b0" + ')'
        self.SetLabels(self.var_start, symbol, 'Mass(kg)', 'Length')
        self.SetLabels(self.var_exec, 'x(m)', 'z(m)')
        self.SetRanges((1, 89), (1, 100), (0, 20))
        self.SetDefaultValues(45, 1, 5)
        self.simulation.changeMode('Conical')

    def OnMomentum(self,event):
        self.SetLabels(self.var_start, 'V(m/s)', 'Mass1(kg)', 'Mass2(kg)', 'Number')
        self.SetLabels(self.var_exec, 'V1(m/s)', 'V2(m/s)')
        self.SetRanges((1, 5), (1, 1000), (1, 1000), (1, 5))
        self.SetDefaultValues(2, 10, 1)
        self.simulation.changeMode('Momentum')

    def OnMomentum2(self,event):
        self.SetLabels(self.var_start, 'Mass1(kg)', 'Mass2(kg)', 'Mass3(kg)', 'Height(m)', 'Distance(m)')
        self.SetLabels(self.var_exec, 'V1(m/s)', 'V2(m/s)', 'V3(m/s)', 'height(m)')
        self.SetRanges((1, 10**7), (1, 10**7), (1, 10**7), (1, 50), (1, 50))
        self.SetDefaultValues(100, 10, 1, 20, 20)
        self.simulation.changeMode('Momentum2')

    def OnPlanet(self,event):
        self.SetLabels(self.var_start, 'Velocity', '% of Distance', '% of G', '% of M')
        self.SetLabels(self.var_exec, 'days', 'V(m/s)')
        self.SetRanges((10000, 80000), (80, 120), (80, 120), (80, 120))
        self.SetDefaultValues(40000, 100, 100,100)
        self.simulation.changeMode('Planet')

    def SetLabels(self, txt_list, *texts):
        i = 0
        for txt in texts:
            txt_list[i].SetLabel(txt)
            txt_list[i].Show()
            i += 1
        while i < 5:
            txt_list[i].SetLabel('')
            i += 1

    def SetRanges(self,*ranges):
        i = 0
        for low, high in ranges:
            self.Ctrls[i].SetRange(low, high)
            self.Ctrls[i].Show()
            i += 1
        while i < 5:
            self.Ctrls[i].Hide()
            i += 1

    def SetDefaultValues(self, *values):
        i = 0
        for value in values:
            self.Ctrls[i].SetValue(value)
            i += 1


if __name__ == '__main__':
    w = MainWindow("Dynamics")
