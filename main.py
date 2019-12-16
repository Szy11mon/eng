# -*- coding: utf-8 -*-
import wx
import os
from Simulation import *
from visual import *
import numpy as np



class MainWindow(window):

    screen_size = wx.GetDisplaySize()

    simulation = None
    same_sim = False
    scene_destroyed = True
    mode = ''
    mode_changed = False

    scene = None
    simulation_started = False
    simulation_stopped = False

    legend = []
    var_start = []
    var_exec = []
    Ctrls = []
    variant = ''
    PL = False

    def __init__(self):
        window.__init__(self, title="Dynamics", _make_panel=True, width = self.screen_size[0],
                        height=self.screen_size[1])

        self.fullscreen = True
        self.SetVariablesPanel()
        self.SetMenubar()
        self.SetStart()

    def SetMenubar(self):
        filemenu = wx.Menu()

        menuItem = filemenu.Append(wx.ID_EXIT, "&Exit",
                                   "Terminate the program")
        self.win.Bind(wx.EVT_MENU, self.OnExit, menuItem)

        self.planeButton = wx.Button(self.panel, label='Inclined Plane', pos=(0.01 * self.screen_size[0], 0.1 * self.screen_size[1]),
                                     size=(110, 27))

        self.planeButton.Bind(wx.EVT_BUTTON, self.OnPlane)

        self.pendulumButton = wx.Button(self.panel, label='Pendulum', pos=(0.01 * self.screen_size[0], 0.14 * self.screen_size[1]),
                                        size=(110, 27))

        self.pendulumButton.Bind(wx.EVT_BUTTON, self.OnPendulum)

        self.throwButton = wx.Button(self.panel, label='Diagonal Throw', pos=(0.01 * self.screen_size[0], 0.18 * self.screen_size[1]),
                                     size=(110, 27))

        self.throwButton.Bind(wx.EVT_BUTTON, self.OnThrow)

        self.helixButton = wx.Button(self.panel, label='Oscillations', pos=(0.01 * self.screen_size[0], 0.22 * self.screen_size[1]),
                                     size=(110, 27))

        self.helixButton.Bind(wx.EVT_BUTTON, self.OnHelix)

        self.momentumButton = wx.Button(self.panel, label='Momentum', pos=(0.01 * self.screen_size[0], 0.26 * self.screen_size[1]),
                                        size=(110, 27))

        self.momentumButton.Bind(wx.EVT_BUTTON, self.OnMomentum)

        self.momentum2Button = wx.Button(self.panel, label='Galileo Cannon', pos=(0.01 * self.screen_size[0], 0.3 * self.screen_size[1]),
                                         size=(110, 27))

        self.momentum2Button.Bind(wx.EVT_BUTTON, self.OnMomentum2)

        self.planetButton = wx.Button(self.panel, label='Planet', pos=(0.01 * self.screen_size[0], 0.34 * self.screen_size[1]),
                                      size=(110, 27))

        self.planetButton.Bind(wx.EVT_BUTTON, self.OnPlanet)

        self.blockButton = wx.Button(self.panel, label='PI Number',
                                     pos=(0.01 * self.screen_size[0], 0.38 * self.screen_size[1]),
                                     size=(110, 27))

        self.blockButton.Bind(wx.EVT_BUTTON, self.OnBlock)

        self.solarButton = wx.Button(self.panel, label='Solar System',
                                     pos=(0.01 * self.screen_size[0], 0.42 * self.screen_size[1]),
                                     size=(110, 27))

        self.solarButton.Bind(wx.EVT_BUTTON, self.OnSolar)

        # self.conicalButton = wx.Button(self.panel, label='Conical Pendulum',
        #                                pos=(0.01 * self.screen_size[0], 0.46 * self.screen_size[1]))
        #
        # self.conicalButton.Bind(wx.EVT_BUTTON, self.OnConical)

        self.runButton = wx.Button(self.panel, label='RUN', pos=(0.01 * self.screen_size[0], 0.06 * self.screen_size[1]))

        self.runButton.Bind(wx.EVT_BUTTON, self.OnRun)

        self.pauseButton = wx.Button(self.panel, label='PAUSE', pos=(0.07 * self.screen_size[0], 0.06 * self.screen_size[1]))

        self.pauseButton.Bind(wx.EVT_BUTTON, self.OnPause)

        self.resumeButton = wx.Button(self.panel, label='RESUME', pos=(0.13 * self.screen_size[0], 0.06 * self.screen_size[1]))

        self.resumeButton.Bind(wx.EVT_BUTTON, self.OnResume)

        self.englishButton = wx.Button(self.panel, label='ENGLISH',
                                 pos=(0.07 * self.screen_size[0], 0.02 * self.screen_size[1]))

        self.englishButton.Bind(wx.EVT_BUTTON, self.OnEnglish)

        self.polishButton = wx.Button(self.panel, label='POLISH',
                                  pos=(0.13 * self.screen_size[0], 0.02 * self.screen_size[1]))

        self.polishButton.Bind(wx.EVT_BUTTON, self.OnPolish)

        menuBar = wx.MenuBar()

        menuBar.Append(filemenu, "&File")

        self.win.SetMenuBar(menuBar)


    def SetVariablesPanel(self):
        self.simulation = Simulation(self)
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        y = 0.06 * self.screen_size[1]
        for i in range(6):
            self.var_start.append(wx.StaticText(self.panel, label='', pos=(0.09*self.screen_size[0], y + 0.04*(i+1)*self.screen_size[1])))
            self.var_start[i].Hide()
            self.Ctrls.append(wx.SpinCtrlDouble(self.panel, value='0', pos=(0.15*self.screen_size[0], y + 0.04*(i+1)*self.screen_size[1]), size=(60, -1)))
            self.Ctrls[i].Hide()
            self.var_exec.append(wx.StaticText(self.panel, label='', pos=((0.9-i*0.1)*self.screen_size[0], 0.86*self.screen_size[1])))
            self.var_exec[i].Hide()
            self.var_exec[i].SetFont(font)
            self.legend.append(wx.StaticText(self.panel, label='', pos=(0.01*self.screen_size[0],0.6*self.screen_size[1] + 0.04*(i+1)*self.screen_size[1])))
            self.legend[i].SetFont(font)
        self.language = wx.StaticText(self.panel, label='Language', pos=(0.01*self.screen_size[0], 0.02 * self.screen_size[1]))
        self.language.SetFont(font)
        png1 = wx.Image('variants.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.variants = []
        variants = wx.StaticBitmap(self.panel, -1, png1, (0.45 * self.screen_size[0], 0.35 * self.screen_size[1]),
                                        (png1.GetWidth(), png1.GetHeight()))
        self.variants.append(variants)
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        variants2 = wx.StaticText(self.panel,label='1\n\n\n\n2\n\n\n\n\n3\n\n\n\n4',pos=(0.4 * self.screen_size[0],0.35 * self.screen_size[1]))
        variants2.SetFont(font)
        self.variants.append(variants2)
        for i in self.variants:
            i.Hide()
    def SetStart(self):
        txt = 'Welcome to dynamics simulation!\nPick one of the options on the left\n' \
                'to read the description and pick parameters'
        self.description = wx.StaticText(self.panel, label=txt,
                                         pos=(0.4 * self.screen_size[0], 0.05 * self.screen_size[1]))
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
        if self.mode == self.simulation.mode and self.mode_changed is False:
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
        self.scene_destroyed = False


    def OnPlane(self,event):
        if self.PL:
            symbol = u'Kąt[' + u"\u00b0" + ']'
            self.SetLabels(self.var_start, symbol, 'Masa[kg]', u'Długość[m]', 'Tarcie', u'Opór powietrza')
            self.SetLabels(self.var_exec, 'czas', 'V', 'a')
            self.SetLegend((u'-> Siła nacisku', 'red'), ('-> Fy', 'gray'), ('-> Fx', 'orange'), ('-> tarcie', 'magenta'),
                           (u'-> opór powietrza', 'cyan'))
        else:
            symbol = 'Angle[' + u"\u00b0" + ']'
            self.SetLabels(self.var_start, symbol, 'Mass[kg]', 'Length[m]', 'Friction', 'Air Resistance')
            self.SetLabels(self.var_exec, 'time', 'V', 'a')
            self.SetLegend(('-> N', 'red'), ('-> Fy', 'gray'), ('-> Fx', 'orange'), ('-> f', 'magenta'),
                           ('-> air', 'cyan'))
        self.SetRanges((10, 80), (1, 100), (1, 100), (0, 1), (0, 1))
        self.SetDefaultValues(45, 10, 10, 0, 0)
        self.simulation.changeMode('Plane')

    def OnPendulum(self,event):
        if self.PL:
            symbol = u'Kąt[' + u"\u00b0" + ']'
            self.SetLabels(self.var_start, symbol, u'Długość[m]', 'g[m/s^2]', u'Opór powietrza')
            self.SetLabels(self.var_exec, u'kąt1', u'kąt2')
        else:
            symbol = 'Angle[' + u"\u00b0" + ']'
            self.SetLabels(self.var_start, symbol, 'Length[m]', 'g[m/s^2]', 'Air Resistance')
            self.SetLabels(self.var_exec, 'angle2', 'angle1')
        self.SetRanges((0, 180), (0, 1), (0, 20), (0, 1))
        self.SetDefaultValues(45, 1, g, 0)
        self.SetLegend()
        self.simulation.changeMode('Pendulum')

    def OnThrow(self,event):
        if self.PL:
            symbol = u'Kąt[' + u"\u00b0" + ']'
            self.SetLabels(self.var_start, symbol, u'Prędkość[m/s]', u'Opór Powietrza', u'Potęga')
            self.SetLabels(self.var_exec, u'odległość', u'wysokość', 'Vy', 'Vx')
        else:
            symbol = 'Angle[' + u"\u00b0" +']'
            self.SetLabels(self.var_start, symbol, 'Velocity[m/s]', 'Air Resistance', 'Power')
            self.SetLabels(self.var_exec, 'distance', 'height', 'Vy', 'Vx')
        self.SetRanges((1, 89), (1, 100), (0, 5), (0, 5))
        self.SetLegend(('-> Vx', 'red'), ('-> Vy', 'magenta'))
        self.SetDefaultValues(45, 50, 0, 0)
        self.simulation.changeMode('Throw')

    def OnBlock(self,event):
        if self.PL:
            self.SetLabels(self.var_start, u'Prędkość[m/s]', 'Masa[kg]', )
            self.SetLabels(self.var_exec, u'uderzenia')
        else:
            self.SetLabels(self.var_start, 'V(m/s)', 'Mass(kg)',)
            self.SetLabels(self.var_exec, 'hits')
        self.SetRanges((1, 5), (1, 10**12))
        self.SetDefaultValues(1, 100)
        self.SetLegend()
        self.simulation.changeMode('Block')

    def OnHelix(self,event):
        if self.PL:
            self.SetLabels(self.var_start, 'k', u'ilość', 'Masa[kg]', 'Wariant', u'Opór Powietrza', 'g[m/s^2]')
            self.SetLabels(self.var_exec, 'Ep + Ek', 'Ep', 'Ek')
        else:
            self.SetLabels(self.var_start, 'k', 'Number', 'Mass[kg]', 'Variant', 'Air Resistance', 'g[m/s^2]')
            self.SetLabels(self.var_exec, 'Ep + Ek', 'Ep', 'Ek')
        self.SetRanges((0, 1), (1, 30), (0, 30), (1, 4), (0, 5), (0,100))
        self.SetDefaultValues(1, 8, 10, 1, 0, 0)
        self.SetLegend()
        self.simulation.changeMode('Helixes')

    def OnSolar(self,event):
        if self.PL:
            self.SetLabels(self.var_start, u"% Prędkości Ziemi", u"Potęga")
            self.SetLabels(self.var_exec, 'Dni')
        else:
            self.SetLabels(self.var_start, "% of Earth's V", 'Power')
            self.SetLabels(self.var_exec, 'Days')
        self.SetRanges((0, 200), (0, 4))
        self.SetDefaultValues(100, 2)
        self.SetLegend()
        self.simulation.changeMode('Solar')

    def OnConical(self,event):
        symbol = 'Angle(' + u"\u00b0" + ')'
        self.SetLabels(self.var_start, symbol, 'Mass(kg)', 'Length')
        self.SetLabels(self.var_exec, 'x(m)', 'z(m)')
        self.SetRanges((1, 89), (1, 100), (0, 20))
        self.SetDefaultValues(45, 1, 5)
        self.SetLegend()
        self.simulation.changeMode('Conical')

    def OnMomentum(self,event):
        if self.PL:
            self.SetLabels(self.var_start, u'Prędkość[m/s]', 'Masa1[kg]', 'Masa2[kg]', u'Ilość')
            self.SetLabels(self.var_exec, 'V1', 'V2')
        else:
            self.SetLabels(self.var_start, 'Velocity[m/s]', 'Mass1[kg]', 'Mass2[kg]', 'Number')
            self.SetLabels(self.var_exec, 'V1', 'V2')
        self.SetRanges((0, 2), (1, 1000), (1, 1000), (1, 30))
        self.SetDefaultValues(1, 1, 1, 10)
        self.SetLegend()
        self.simulation.changeMode('Momentum')

    def OnMomentum2(self,event):
        if self.PL:
            self.SetLabels(self.var_start, 'Masa1[kg]', 'Masa2[kg]', 'Masa3[kg]', 'Masa4[kg]' u'Wysokość[m]')
            self.SetLabels(self.var_exec, 'V1', 'V2', 'V3', 'V4', u'wysokość')
        else:
            self.SetLabels(self.var_start, 'Mass1[kg]', 'Mass2[kg]', 'Mass3[kg]', 'Mass4[kg]', 'Height[m]')
            self.SetLabels(self.var_exec, 'V1', 'V2', 'V3', 'V4', 'height')
        self.SetRanges((1, 10**7), (1, 10**7), (1, 10**7), (1, 10**7), (1, 5))
        self.SetDefaultValues(1000, 100, 10, 1, 1)
        self.SetLegend()
        self.simulation.changeMode('Momentum2')

    def OnPlanet(self,event):
        if self.PL:
            self.SetLabels(self.var_start, u'% Prędkości', u'% Odległości', u'% stałej G', u'% Masy Słońca')
            self.SetLabels(self.var_exec, 'Dni', 'V')
            self.SetLegend((u'Początkowe wartości:\nV = 40 [km/s]\nOdległość = 70 000 000 [km]', 'black'))
        else:
            self.SetLabels(self.var_start, '% of Velocity', '% of Distance', '% of G', "% of Sun's Mass")
            self.SetLabels(self.var_exec, 'days', 'V')
            self.SetLegend(('Initial Values:\nV = 40 [km/s]\nDistance = 70 000 000 [km]', 'black'))
        self.SetRanges((0, 200), (0, 200), (0, 200), (0, 200))
        self.SetDefaultValues(100, 100, 100, 100)
        self.simulation.changeMode('Planet')

    def SetLabels(self, txt_list, *texts):
        i = 0
        for txt in texts:
            txt_list[i].SetLabel(txt)
            txt_list[i].Show()
            i += 1
        while i < 6:
            txt_list[i].SetLabel('')
            i += 1

    def SetRanges(self,*ranges):
        i = 0
        for low, high in ranges:
            self.Ctrls[i].SetRange(low, high)
            self.Ctrls[i].Show()
            i += 1
        while i < 6:
            self.Ctrls[i].Hide()
            i += 1

    def SetDefaultValues(self, *values):
        i = 0
        for value in values:
            self.Ctrls[i].SetValue(value)
            i += 1

    def SetLegend(self, *values):
        i = 0
        for txt, hue in values:
            self.legend[i].SetLabel(txt)
            self.legend[i].SetForegroundColour(colors[hue])
            self.legend[i].Show()
            i += 1
        while i < 5:
            self.legend[i].SetLabel('')
            i += 1

    def OnEnglish(self, event):
        if self.PL is True:
            self.PL = False
            self.SetLanguage()

    def OnPolish(self, event):
        if self.PL is False:
            self.PL = True
            self.SetLanguage()

    def SetLanguage(self):
        if self.PL:
            self.description.SetLabel(u'Witaj w aplikacji do symulacji dynamiki!\nWybierz jedną z opcji dostępnych z '
                                      u'lewej strony,\naby przeczytać opis i dostosować parametry')
            self.planeButton.SetLabel(u'Równia Pochyła')
            self.pendulumButton.SetLabel(u'Wahadło')
            self.throwButton.SetLabel(u'Rzut Ukośny')
            self.blockButton.SetLabel(u'Liczba PI')
            self.helixButton.SetLabel(u'Drgania')
            self.solarButton.SetLabel(u'Układ Słoneczny')
            # self.conicalButton.SetLabel(u'Wahadło Stożkowe')
            self.momentumButton.SetLabel(u'Zachowanie Pędu')
            self.momentum2Button.SetLabel(u'Działo Galileusza')
            self.planetButton.SetLabel(u'Planeta')
            self.runButton.SetLabel(u'START')
            self.pauseButton.SetLabel(u'PAUZA')
            self.resumeButton.SetLabel(u'WZNÓW')
            self.englishButton.SetLabel(u'ANGIELSKI')
            self.polishButton.SetLabel(u'POLSKI')
            self.language.SetLabel(u'Język')
        else:
            self.description.SetLabel('Welcome to dynamics simulation!\nPick one of the options on the left\n'
                'to read the description and pick parameters')
            self.planeButton.SetLabel('Inclined Plane')
            self.pendulumButton.SetLabel('Pendulum')
            self.throwButton.SetLabel('Diagonal Throw')
            self.blockButton.SetLabel('PI Number')
            self.helixButton.SetLabel('Oscillations')
            self.solarButton.SetLabel('Solar System')
            # self.conicalButton.SetLabel('Conical')
            self.momentumButton.SetLabel('Momentum')
            self.momentum2Button.SetLabel('Galileo Cannon')
            self.planetButton.SetLabel('Planet')
            self.runButton.SetLabel('RUN')
            self.pauseButton.SetLabel('PAUSE')
            self.resumeButton.SetLabel('RESUME')
            self.englishButton.SetLabel('ENGLISH')
            self.polishButton.SetLabel('POLISH')
            self.language.SetLabel('Language')
        if self.simulation.mode != '':
            self.simulation.description()
            tmp = 'self.On' + self.simulation.mode + '(None)'
            eval(tmp)


if __name__ == '__main__':
    w = MainWindow()
