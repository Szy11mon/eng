from visual import *
from variables import *
import math


class Throw:

    def __init__(self, window):
        self.win = window

    @staticmethod
    def description():
        return "This is diagonal throw but with the influence of the air\nYou can set angle, starting velocity\n"\
               "and the coefficient of air resistance\nDuring the simulation you will see velocities in both directions\n"\
               "height and distance"

    def prepare(self):
        self.angle = self.win.Ctrls[0].GetValue()
        self.velocity = self.win.Ctrls[1].GetValue()
        self.air_res = self.win.Ctrls[2].GetValue()

        self.theta = degree_to_rad * self.angle
        self.win.scene.autoscale = False
        self.dist = (self.velocity * self.velocity * sin(2 * self.theta)) / g
        self.cannon = box(pos=(-(self.dist / 2), self.dist * 0.02, 0),
                          size=(self.dist * 0.04, self.dist * 0.04, self.dist * 0.04), color=color.red)
        self.Road = box(pos=vector(0, 0, 0), size=vector(self.dist * 1.4, self.dist / 100, 50), color=color.green,
                        opacity=0.3)
        self.cannon.rotate(angle=self.theta, origin=vector(-(self.dist / 2), self.dist * 0.02, 0), axis=vector(0, 0, 1))
        if self.angle < 70:
            self.win.scene.range = (self.velocity * self.velocity / g) * sin(2 * self.theta)
            self.win.scene.center = (0, sqrt((self.velocity * self.velocity) * sin(self.theta) ** 2) / (2 * g) * 2, 0)
        else:
            self.win.scene.range = (self.velocity * self.velocity / g) * sin(2 * self.theta) * 1.5
            self.win.scene.center = (0, sqrt((self.velocity * self.velocity) * sin(self.theta) ** 2) / (2 * g) * 6, 0)
        self.ball = sphere(
            pos=(self.cannon.pos.x + self.dist * 0.02, self.cannon.pos.y + self.dist * 0.02, self.cannon.pos.z),
            radius=self.dist * 0.02,
            color=color.blue, make_trail=True)
        self.VX = arrow(pos=self.ball.pos + (self.dist * 0.01, 0, 0), axis=(0.1 * self.dist, 0, 0),
                        shaftwidth=0.01 * self.dist, color=color.red)
        self.VY = arrow(pos=self.ball.pos + (0, self.dist * 0.01, 0), axis=(0.1 * self.dist, 0, 0),
                        shaftwidth=0.01 * self.dist, color=color.yellow)
        self.VY.rotate(angle=degree_to_rad * 90, origin=self.ball.pos + (0, self.dist * 0.01, 0), axis=vector(0, 0, 1))
        if self.air_res != 0:
            self.v = vector(self.velocity * math.exp(-self.air_res * 0) * cos(self.theta),
                            (self.velocity * sin(self.theta) + (g / self.air_res))
                            * math.exp(-self.air_res * 0) - g / self.air_res, 0)
        else:
            self.v = vector(self.velocity * cos(self.theta),
                            self.velocity * sin(self.theta) - g * 0, 0)
        self.dt = 0.0005
        self.t = 0
        self.ball.trail_object.color = color.yellow

    def run(self):
        start_ball = self.ball.pos
        start_VX = self.VX.pos
        start_VY = self.VY.pos
        counter = 0
        rotate_y = False
        while self.ball.pos.y > self.cannon.pos.y:
            if not self.win.simulation_stopped:
                rate(100 * self.velocity)
                if self.air_res != 0:
                    self.ball.v = vector(self.velocity * math.exp(-self.air_res * self.t) * cos(self.theta),
                                         (self.velocity * sin(self.theta) + (g / self.air_res))
                                         * math.exp(-self.air_res * self.t) - g / self.air_res, 0)
                else:
                    self.ball.v = vector(self.velocity * cos(self.theta),
                                         self.velocity * sin(self.theta) - g * self.t, 0)

                self.ball.pos = start_ball + self.ball.v * self.dt
                self.VX.pos = start_VX + self.ball.v * self.dt
                self.VY.pos = start_VY + self.ball.v * self.dt
                self.VY.length = abs(0.1 * self.dist * (self.ball.v.y / self.v.y))
                self.VX.length = 0.1 * self.dist * (self.ball.v.x / self.v.x)
                if self.ball.v.y < 0 and rotate_y == False:
                    self.VY.rotate(angle=degree_to_rad * 180, origin=self.ball.pos, axis=vector(0, 0, 1))
                    rotate_y = True
                self.t = self.t + self.dt

                counter = counter + 1
                if counter % 50 is 0:
                    self.win.var_exec[3].SetLabel('Vx(m/s) = ' + '%.2f' % self.ball.v.x)
                    self.win.var_exec[2].SetLabel('Vy(m/s) = ' + '%.2f' % self.ball.v.y)
                    self.win.var_exec[1].SetLabel('h(m) = ' + '%.2f' % (self.ball.pos.y - self.cannon.pos.y))
                    self.win.var_exec[0].SetLabel('x(m) = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x))
            else:
                while True:
                    rate(10)
        self.win.var_exec[3].SetLabel('Vx(m/s) = ' + '%.2f' % self.ball.v.x)
        self.win.var_exec[2].SetLabel('Vy(m/s) = ' + '%.2f' % self.ball.v.y)
        self.win.var_exec[1].SetLabel('h(m) = 0')
        self.win.var_exec[0].SetLabel('x(m) = ' + '%.2f' % (self.ball.pos.x - self.cannon.pos.x))
