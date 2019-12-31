# -*- coding: utf-8 -*-
# import wx
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
    PL = True

    def __init__(self):
        window.__init__(self, title="Dynamics", _make_panel=True, width = self.screen_size[0],
                        height=self.screen_size[1])

        self.fullscreen = True
        self.set_variables_panel()
        self.set_menu()
        self.set_start()

    def set_menu(self):

        font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)

        self.planeButton = wx.Button(self.panel, label=u'Równia Pochyła', pos=(0.01 * self.screen_size[0], 0.1 * self.screen_size[1]),
                                     size=(0.1*self.screen_size[0], 0.035*self.screen_size[1]))
        self.planeButton.SetFont(font)

        self.planeButton.Bind(wx.EVT_BUTTON, self.on_plane)
        self.pendulumButton = wx.Button(self.panel, label=u'Wahadło', pos=(0.12 * self.screen_size[0], 0.1 * self.screen_size[1]),
                                        size=(0.1*self.screen_size[0], 0.035*self.screen_size[1]))
        self.pendulumButton.SetFont(font)

        self.pendulumButton.Bind(wx.EVT_BUTTON, self.on_pendulum)

        self.throwButton = wx.Button(self.panel, label=u'Rzut Ukośny', pos=(0.01 * self.screen_size[0], 0.15 * self.screen_size[1]),
                                     size=(0.1*self.screen_size[0], 0.035*self.screen_size[1]))

        self.throwButton.Bind(wx.EVT_BUTTON, self.on_throw)
        self.throwButton.SetFont(font)

        self.helixButton = wx.Button(self.panel, label=u'Drgania', pos=(0.12 * self.screen_size[0], 0.15 * self.screen_size[1]),
                                     size=(0.1*self.screen_size[0], 0.035*self.screen_size[1]))

        self.helixButton.Bind(wx.EVT_BUTTON, self.on_helix)
        self.helixButton.SetFont(font)

        self.momentumButton = wx.Button(self.panel, label=u'Zachowanie Pędu', pos=(0.01 * self.screen_size[0], 0.2 * self.screen_size[1]),
                                        size=(0.1*self.screen_size[0], 0.035*self.screen_size[1]))
        self.momentumButton.SetFont(font)

        self.momentumButton.Bind(wx.EVT_BUTTON, self.on_momentum)

        self.momentum2Button = wx.Button(self.panel, label=u'Działo Galilejskie', pos=(0.12 * self.screen_size[0], 0.2 * self.screen_size[1]),
                                         size=(0.1*self.screen_size[0], 0.035*self.screen_size[1]))
        self.momentum2Button.SetFont(font)

        self.momentum2Button.Bind(wx.EVT_BUTTON, self.on_momentum2)

        self.planetButton = wx.Button(self.panel, label='Planeta', pos=(0.01 * self.screen_size[0], 0.25 * self.screen_size[1]),
                                      size=(0.1*self.screen_size[0], 0.035*self.screen_size[1]))

        self.planetButton.Bind(wx.EVT_BUTTON, self.on_planet)
        self.planetButton.SetFont(font)

        self.blockButton = wx.Button(self.panel, label=u'Liczba PI',
                                     pos=(0.12 * self.screen_size[0], 0.25 * self.screen_size[1]),
                                     size=(0.1*self.screen_size[0], 0.035*self.screen_size[1]))
        self.blockButton.SetFont(font)

        self.blockButton.Bind(wx.EVT_BUTTON, self.on_block)

        self.solarButton = wx.Button(self.panel, label=u'Układ Słoneczny',
                                     pos=(0.01 * self.screen_size[0], 0.3 * self.screen_size[1]),
                                     size=(0.1*self.screen_size[0], 0.035*self.screen_size[1]))
        self.solarButton.SetFont(font)

        self.solarButton.Bind(wx.EVT_BUTTON, self.on_solar)

        self.runButton = wx.Button(self.panel, label='START', pos=(0.01 * self.screen_size[0], 0.05 * self.screen_size[1]),
                                   size=(0.07*self.screen_size[0], 0.035*self.screen_size[1]))

        self.runButton.Bind(wx.EVT_BUTTON, self.on_run)
        self.runButton.SetFont(font)

        self.pauseButton = wx.Button(self.panel, label=u'PAUZA', pos=(0.08 * self.screen_size[0], 0.05 * self.screen_size[1]),
                                     size=(0.07*self.screen_size[0], 0.035*self.screen_size[1]))

        self.pauseButton.Bind(wx.EVT_BUTTON, self.on_pause)
        self.pauseButton.SetFont(font)

        self.resumeButton = wx.Button(self.panel, label=u'WZNÓW', pos=(0.15 * self.screen_size[0], 0.05 * self.screen_size[1]),
                                      size=(0.07*self.screen_size[0], 0.035*self.screen_size[1]))

        self.win.Bind(wx.EVT_CLOSE, self.on_close)

        self.resumeButton.Bind(wx.EVT_BUTTON, self.on_resume)
        self.resumeButton.SetFont(font)

        self.englishButton = wx.Button(self.panel, label='ANGIELSKI',
                                 pos=(0.08 * self.screen_size[0], 0.01 * self.screen_size[1]),
                                       size=(0.07*self.screen_size[0], 0.035*self.screen_size[1]))

        self.englishButton.Bind(wx.EVT_BUTTON, self.on_english)
        self.englishButton.SetFont(font)

        self.polishButton = wx.Button(self.panel, label='POLSKI',
                                  pos=(0.15 * self.screen_size[0], 0.01 * self.screen_size[1]),
                                      size=(0.07*self.screen_size[0], 0.035*self.screen_size[1]))

        self.polishButton.Bind(wx.EVT_BUTTON, self.on_polish)
        self.polishButton.SetFont(font)

    def set_variables_panel(self):
        self.simulation = Simulation(self)
        font_ctrl = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        font_var = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        font_exec = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        self.parameters_text = wx.StaticText(self.panel, label='Parametry Symulacji:', pos=(0.01*self.screen_size[0], 0.36*self.screen_size[1]))
        self.parameters_text.SetFont(font_var)
        self.parameters_text.Hide()
        y = 0.36 * self.screen_size[1]
        for i in range(6):
            self.var_start.append(wx.StaticText(self.panel, label='', pos=(0.01*self.screen_size[0], y + 0.04*(i+1)*self.screen_size[1])))
            self.var_start[i].Hide()
            self.var_start[i].SetFont(font_var)
            self.Ctrls.append(wx.SpinCtrlDouble(self.panel, value='0', pos=(0.12*self.screen_size[0], y + 0.04*(i+1)*self.screen_size[1]), size=(0.09*self.screen_size[0], -1)))
            self.Ctrls[i].Hide()
            self.Ctrls[i].SetFont(font_ctrl)
            self.var_exec.append(wx.StaticText(self.panel, label='', pos=((0.86-i*0.15)*self.screen_size[0], 0.87*self.screen_size[1])))
            self.var_exec[i].Hide()
            self.var_exec[i].SetFont(font_exec)
            self.legend.append(wx.StaticText(self.panel, label='', pos=(0.01*self.screen_size[0],0.6*self.screen_size[1] + 0.04*(i+1)*self.screen_size[1])))
            self.legend[i].SetFont(font)
        self.language = wx.StaticText(self.panel, label=u'Język', pos=(0.01*self.screen_size[0], 0.01 * self.screen_size[1]))
        self.language.SetFont(font)
        png1 = wx.Image('variants.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.variants = []
        variants = wx.StaticBitmap(self.panel, -1, png1, (0.35 * self.screen_size[0], 0.3 * self.screen_size[1]),
                                        (png1.GetWidth(), png1.GetHeight()))
        self.variants.append(variants)
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        variants2 = wx.StaticText(self.panel,label='\n1\n\n\n\n\n2\n\n\n\n3\n\n\n\n4',pos=(0.3 * self.screen_size[0],0.3 * self.screen_size[1]))
        variants2.SetFont(font)
        self.variants.append(variants2)
        for i in self.variants:
            i.Hide()

    def set_start(self):
        txt = u'Witaj w aplikacji do symulacji dynamiki!\nPo wybraniu jednej z opcji dostępnych z '\
              u'lewej strony\nmożna przeczytać opis i dostosować parametry.\nW trakcie każdej z'\
              u' symulacji u dołu ekranu można śledzić\nwartości parametrów istotnych dla prze'\
              u'prowadzanego doświadczenia.\nAplikacja dostępna jest w dwóch wersjach językowych.'
        self.description = wx.StaticText(self.panel, label=txt,
                                         pos=(0.3 * self.screen_size[0], 0.05 * self.screen_size[1]))
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.description.SetFont(font)

    def on_close(self, event):
        if self.PL:
            dlg = wx.MessageDialog(self.win,
                                   u"Czy naprawdę chcesz wyjść ?",
                                   u"Wyjście",
                                   wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        else:
            dlg = wx.MessageDialog(self.win,
                                   "Do you really want to close this application?",
                                   "Exit",
                                   wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            exit()

    def on_run(self, event):
        self.simulation_stopped = False
        if self.mode == self.simulation.mode and self.mode_changed is False:
            self.same_sim = True
        self.mode = self.simulation.mode
        if self.mode != '':
            self.simulation.run()

    def on_pause(self, event):
        if self.simulation is None or self.simulation_stopped is True:
            pass
        else:
            self.simulation_stopped = True

    def on_resume(self, event):
        if self.simulation is None or self.simulation_stopped is False:
            pass
        else:
            self.simulation_stopped = False
            self.simulation.resume()

    def set_display(self):
        self.scene = display(window=self, x=0.22*self.screen_size[0], y=0, width=0.8*self.screen_size[0],
                             height=0.85*self.screen_size[1], autoscale=True, centre=vector(0,0,0))
        self.scene_destroyed = False

    def on_plane(self, event):
        if self.PL:
            symbol = u'Kąt [' + u"\u00b0" + ']'
            self.set_labels(self.var_start, symbol, 'Masa [kg]', u'Długość [m]', 'Tarcie', u'Opór powietrza')
            self.set_labels(self.var_exec, 'czas', 'V', 'a')
            self.set_legend((u'-> Siła normalna', 'red'), (u'-> Siła nacisku', 'gray'), (u'-> Siła spychająca', 'orange'),
                            ('-> Tarcie', 'magenta'), (u'-> Opór powietrza', 'cyan'))
        else:
            symbol = 'Angle [' + u"\u00b0" + ']'
            self.set_labels(self.var_start, symbol, 'Mass [kg]', 'Length [m]', 'Friction', 'Air Resistance')
            self.set_labels(self.var_exec, 'time', 'V', 'a')
            self.set_legend(('-> Normal force', 'red'), ('-> Pressure force', 'gray'), ('-> Pushing force', 'orange'),
                            ('-> Friction', 'magenta'), ('-> Air resistance', 'cyan'))
        self.set_ranges((1, 89), (1, 100), (1, 1000), (0, 1), (0, 5))
        self.set_default_values(45, 10, 10, 0, 0)
        self.set_default_positions()
        if event is not None:
            self.simulation.change_mode('Plane')

    def on_pendulum(self, event):
        if self.PL:
            symbol = u'Kąt [' + u"\u00b0" + ']'
            self.set_labels(self.var_start, symbol, u'Długość [m]', 'g [m/s^2]', u'Opór powietrza')
            self.set_labels(self.var_exec, u'kąt1', u'kąt2')
            self.set_legend((u'kąt1 - kąt2', 'blue'))
        else:
            symbol = 'Angle [' + u"\u00b0" + ']'
            self.set_labels(self.var_start, symbol, 'Length [m]', 'g [m/s^2]', 'Air Resistance')
            self.set_labels(self.var_exec, 'angle2', 'angle1')
            self.set_legend(('angle1 - angle2', 'blue'))
        self.set_ranges((0, 180), (0, 1), (0, 20), (0, 1))
        self.set_default_values(45, 1, 9.8, 0)
        self.set_default_positions()
        if event is not None:
            self.simulation.change_mode('Pendulum')

    def on_throw(self, event):
        if self.PL:
            symbol = u'Kąt [' + u"\u00b0" + ']'
            self.set_labels(self.var_start, symbol, u'Prędkość [m/s]', u'Opór Powietrza', u'Potęga')
            self.set_labels(self.var_exec, u'odległość', u'wysokość', 'Vy', 'Vx')
            self.set_positions((0.82 * self.screen_size[0], 0.87 * self.screen_size[1]),
                               (0.65 * self.screen_size[0], 0.87 * self.screen_size[1]),
                               (0.51 * self.screen_size[0], 0.87 * self.screen_size[1]),
                               (0.37 * self.screen_size[0], 0.87 * self.screen_size[1]))
        else:
            symbol = 'Angle [' + u"\u00b0" +']'
            self.set_labels(self.var_start, symbol, 'Velocity [m/s]', 'Air Resistance', 'Power')
            self.set_labels(self.var_exec, 'distance', 'height', 'Vy', 'Vx')
            self.set_positions((0.82 * self.screen_size[0], 0.87 * self.screen_size[1]),
                               (0.67 * self.screen_size[0], 0.87 * self.screen_size[1]),
                               (0.53 * self.screen_size[0], 0.87 * self.screen_size[1]),
                               (0.39 * self.screen_size[0], 0.87 * self.screen_size[1]))
        self.set_ranges((1, 89), (1, 100), (0, 100), (0, 5))
        self.set_legend(('-> Vx', 'red'), ('-> Vy', 'magenta'))
        self.set_default_values(45, 50, 0, 0)
        if event is not None:
            self.simulation.change_mode('Throw')

    def on_block(self, event):
        if self.PL:
            self.set_labels(self.var_start, u'Prędkość [m/s]', 'Masa [kg]', )
            self.set_labels(self.var_exec, u'uderzenia')
        else:
            self.set_labels(self.var_start, 'V [m/s]', 'Mass[kg]', )
            self.set_labels(self.var_exec, 'hits')
        self.set_ranges((1, 5), (1, 10 ** 12))
        self.set_default_values(1, 100)
        self.set_positions((0.80 * self.screen_size[0], 0.87 * self.screen_size[1]))
        self.set_legend()
        if event is not None:
            self.simulation.change_mode('Block')

    def on_helix(self, event):
        if self.PL:
            self.set_labels(self.var_start, 'k', u'ilość', 'Masa [kg]', 'Wariant', u'Opór Powietrza', 'g [m/s^2]')
            self.set_labels(self.var_exec, 'Ep + Ek', 'Ep', 'Ek')
        else:
            self.set_labels(self.var_start, 'k', 'Number', 'Mass [kg]', 'Variant', 'Air Resistance', 'g [m/s^2]')
            self.set_labels(self.var_exec, 'Ep + Ek', 'Ep', 'Ek')
        self.set_ranges((0, 10), (1, 30), (0, 30), (1, 4), (0, 5), (0, 100))
        self.set_default_values(1, 8, 10, 1, 0, 0)
        self.set_legend()
        self.set_positions((0.82*self.screen_size[0], 0.87*self.screen_size[1]), (0.67*self.screen_size[0], 0.87*self.screen_size[1]),
                           (0.52*self.screen_size[0], 0.87*self.screen_size[1]))
        if event is not None:
            self.simulation.change_mode('Helix')

    def on_solar(self, event):
        if self.PL:
            self.set_labels(self.var_start, u"% V Ziemi", u"Potęga")
            self.set_labels(self.var_exec, 'Dni')
            self.set_legend(('Merkury', 'magenta'), ('Mars', 'green'), ('Ziemia', 'blue'), ('Wenus', 'red'))
        else:
            self.set_labels(self.var_start, "% of Earth's V", 'Power')
            self.set_labels(self.var_exec, 'Days')
            self.set_legend(('Mercury', 'magenta'), ('Mars', 'green'), ('Earth', 'blue'), ('Venus', 'red'))
        self.set_ranges((0, 200), (0, 4))
        self.set_default_values(100, 3)
        self.set_default_positions()
        if event is not None:
            self.simulation.change_mode('Solar')

    def on_momentum(self, event):
        if self.PL:
            self.set_labels(self.var_start, u'Prędkość [m/s]', 'Masa1 [kg]', 'Masa2 [kg]', u'Ilość')
            self.set_labels(self.var_exec, 'V2', 'V1')
        else:
            self.set_labels(self.var_start, 'Velocity [m/s]', 'Mass1 [kg]', 'Mass2 [kg]', 'Number')
            self.set_labels(self.var_exec, 'V2', 'V1')
        self.set_ranges((0, 100), (0, 1000), (0, 1000), (1, 30))
        self.set_default_values(1, 1, 1, 10)
        self.set_default_positions()
        self.set_legend()
        if event is not None:
            self.simulation.change_mode('Momentum')

    def on_momentum2(self, event):
        if self.PL:
            self.set_labels(self.var_start, 'Masa1 [kg]', 'Masa2 [kg]', 'Masa3 [kg]', 'Masa4 [kg]', u'Wysokość2 [m]')
            self.set_labels(self.var_exec, u'Wysokość2', u'Wysokość1')
            self.set_legend((u'Wysokość1', 'green'), (u'Wysokość2', 'blue'))
        else:
            self.set_labels(self.var_start, 'Mass1 [kg]', 'Mass2 [kg]', 'Mass3 [kg]', 'Mass4 [kg]', 'Height [m]')
            self.set_labels(self.var_exec, 'Height2', 'Height1')
            self.set_legend(('Height1', 'green'), ('Height2', 'blue'))
        self.set_ranges((1, 10 ** 7), (1, 10 ** 7), (1, 10 ** 7), (1, 10 ** 7), (1, 30))
        self.set_default_values(1000, 100, 10, 1, 5)
        self.set_positions((0.80 * self.screen_size[0], 0.87 * self.screen_size[1]),
                           ((0.60 * self.screen_size[0], 0.87 * self.screen_size[1])))
        if event is not None:
            self.simulation.change_mode('Momentum2')

    def on_planet(self, event):
        if self.PL:
            self.set_labels(self.var_start, u'% Prędkości', u'% Odległości', u'% stałej G', u'% Masy Słońca')
            self.set_labels(self.var_exec, 'Dni', 'V')
            self.set_legend((u'Początkowe wartości:', 'black'), ('V = 40 [km/s]', 'black'), (u'Odległość = 70 000 000 [km]', 'black'),
                            (u'-> Prędkość', 'green'), (u'-> Siła dośrodkowa', 'blue'))
        else:
            self.set_labels(self.var_start, '% of Velocity', '% of Distance', '% of G', "% of Sun's Mass")
            self.set_labels(self.var_exec, 'days', 'V')
            self.set_legend(('Initial Values:', 'black'), ('V = 40 [km/s]', 'black'), ('Distance = 70 000 000 [km]', 'black'),
                            ('-> Velocity', 'green'), ('-> Centripetal Force', 'blue'))
        self.set_ranges((0, 200), (0, 200), (0, 200), (0, 200))
        self.set_default_values(100, 100, 100, 100)
        self.set_default_positions()
        if event is not None:
            self.simulation.change_mode('Planet')

    def set_labels(self, txt_list, *texts):
        i = 0
        for txt in texts:
            txt_list[i].SetLabel(txt)
            txt_list[i].Show()
            i += 1
        while i < 6:
            txt_list[i].SetLabel('')
            i += 1
        self.parameters_text.Show()

    def set_ranges(self, *ranges):
        i = 0
        for low, high in ranges:
            self.Ctrls[i].SetRange(low, high)
            self.Ctrls[i].Show()
            i += 1
        while i < 6:
            self.Ctrls[i].Hide()
            i += 1

    def set_default_values(self, *values):
        i = 0
        for value in values:
            self.Ctrls[i].SetValue(value)
            i += 1

    def set_legend(self, *values):
        i = 0
        for txt, hue in values:
            self.legend[i].SetLabel(txt)
            self.legend[i].SetForegroundColour(colors[hue])
            self.legend[i].Show()
            i += 1
        while i < 5:
            self.legend[i].SetLabel('')
            i += 1

    def on_english(self, event):
        if self.PL is True:
            self.PL = False
            self.set_language()

    def on_polish(self, event):
        if self.PL is False:
            self.PL = True
            self.set_language()

    def set_language(self):
        if self.PL:
            self.description.SetLabel(u'Witaj w aplikacji do symulacji dynamiki!\nPo wybraniu jednej z opcji dostępnych z '
                                      u'lewej strony\nmożna przeczytać opis i dostosować parametry.\nW trakcie każdej z'
                                      u' symulacji u dołu ekranu można śledzić\nwartości parametrów istotnych dla prze'
                                      u'prowadzanego doświadczenia.')
            self.planeButton.SetLabel(u'Równia Pochyła')
            self.pendulumButton.SetLabel(u'Wahadło')
            self.throwButton.SetLabel(u'Rzut Ukośny')
            self.blockButton.SetLabel(u'Liczba PI')
            self.helixButton.SetLabel(u'Drgania')
            self.solarButton.SetLabel(u'Układ Słoneczny')
            # self.conicalButton.SetLabel(u'Wahadło Stożkowe')
            self.momentumButton.SetLabel(u'Zachowanie Pędu')
            self.momentum2Button.SetLabel(u'Działo Galilejskie')
            self.planetButton.SetLabel(u'Planeta')
            self.parameters_text.SetLabel(u'Parametry Symulacji:')
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
            self.momentum2Button.SetLabel('Galilean Cannon')
            self.planetButton.SetLabel('Planet')
            self.parameters_text.SetLabel('Parameters:')
            self.runButton.SetLabel('RUN')
            self.pauseButton.SetLabel('PAUSE')
            self.resumeButton.SetLabel('RESUME')
            self.englishButton.SetLabel('ENGLISH')
            self.polishButton.SetLabel('POLISH')
            self.language.SetLabel('Language')
        if self.simulation.mode != '':
            self.simulation.description()
            tmp = 'self.on_' + self.simulation.mode.lower() + '(None)'
            eval(tmp)

    def set_positions(self, *positions):
        i = 0
        for x, y in positions:
            self.var_exec[i].SetPosition((x, y))
            i += 1

    def set_default_positions(self):
        for i in range(6):
            self.var_exec[i].SetPosition(((0.86 - i * 0.15) * self.screen_size[0], 0.87 * self.screen_size[1]))



if __name__ == '__main__':
    w = MainWindow()
