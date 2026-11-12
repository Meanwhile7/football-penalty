__version__ = "1.0.0"

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
import random
import math

class FootballGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.shots = 0
        self.max_shots = 5
        self.ball_x = 0.5
        self.ball_y = 0.16
        self.ball_vx = 0
        self.ball_vy = 0
        self.shooting = False
        self.keeper_x = 0.5
        self.keeper_dir = 1
        self.message = "Tap above the ball to shoot!"
        self.game_over = False
        self.hud = Label(text="", font_size="18sp", bold=True,
                         size_hint=(1, None), height=42,
                         pos_hint={"x": 0, "top": 1},
                         color=(1, 1, 1, 1))
        self.add_widget(self.hud)
        self.result = Label(text="", font_size="25sp", bold=True,
                            size_hint=(1, None), height=50,
                            pos_hint={"center_x": .5, "center_y": .52},
                            color=(1, 1, 0, 1))
        self.add_widget(self.result)
        self.bind(size=self.redraw, pos=self.redraw)
        Clock.schedule_interval(self.update, 1/60)

    def field(self):
        return self.x, self.y, self.width, self.height

    def redraw(self, *args):
        if self.width <= 0 or self.height <= 0:
            return
        x, y, w, h = self.field()
        self.canvas.clear()
        with self.canvas:
            # Grass and alternating stripes
            Color(0.08, 0.48, 0.19, 1)
            Rectangle(pos=(x, y), size=(w, h))
            for i in range(8):
                if i % 2 == 0:
                    Color(0.10, 0.54, 0.22, 1)
                    Rectangle(pos=(x, y + i*h/8), size=(w, h/8))
            # Goal and net
            gl, gr = x+w*.27, x+w*.73
            gy, gh = y+h*.66, h*.19
            Color(1, 1, 1, 1)
            Line(rectangle=(gl, gy, gr-gl, gh), width=2)
            for i in range(1, 9):
                xx = gl + (gr-gl)*i/9
                Line(points=[xx, gy, xx, gy+gh], width=1)
            for i in range(1, 5):
                yy = gy + gh*i/5
                Line(points=[gl, yy, gr, yy], width=1)
            # Midfield / penalty spot
            Line(points=[x+w*.08, y+h*.47, x+w*.92, y+h*.47], width=1)
            Color(1, 1, 1, 1)
            Ellipse(pos=(x+w*.5-3, y+h*.155-3), size=(6, 6))
            # Goalkeeper
            kx = x + self.keeper_x*w
            Color(0.12, 0.25, 0.9, 1)
            Rectangle(pos=(kx-w*.045, gy+h*.08), size=(w*.09, h*.065))
            Color(1, .72, .52, 1)
            Ellipse(pos=(kx-w*.018, gy+h*.14), size=(w*.036, h*.036))
            # Ball
            bx = x + self.ball_x*w
            by = y + self.ball_y*h
            Color(1, 1, 1, 1)
            Ellipse(pos=(bx-w*.018, by-h*.024), size=(w*.036, h*.048))
            Color(0, 0, 0, 1)
            Line(circle=(bx, by, w*.018), width=1)
        self.hud.text = f"⚽  PENALTY SHOOTOUT     GOALS: {self.score}     SHOTS: {self.shots}/{self.max_shots}"
        self.hud.pos = (x, y+h-45)
        self.result.text = self.message if self.game_over else ""

    def on_touch_down(self, touch):
        if self.game_over:
            self.score = 0
            self.shots = 0
            self.game_over = False
            self.message = "New game! Take your shot."
            self.reset_ball()
            self.redraw()
            return True
        if self.shooting or self.shots >= self.max_shots:
            return True
        x, y, w, h = self.field()
        if not self.collide_point(*touch.pos):
            return False
        target_x = max(.29, min(.71, (touch.x-x)/w))
        target_y = max(.68, min(.88, (touch.y-y)/h))
        dx = target_x - self.ball_x
        dy = target_y - self.ball_y
        length = max(.01, math.sqrt(dx*dx + dy*dy))
        self.ball_vx = dx/length * .95
        self.ball_vy = dy/length * .95
        self.shooting = True
        self.shots += 1
        self.message = "SHOOT!"
        return True

    def reset_ball(self):
        self.ball_x, self.ball_y = .5, .16
        self.ball_vx = self.ball_vy = 0
        self.shooting = False

    def update(self, dt):
        if self.shooting:
            self.ball_x += self.ball_vx * dt
            self.ball_y += self.ball_vy * dt
            self.keeper_x += self.keeper_dir * .42 * dt
            if self.keeper_x > .68:
                self.keeper_x, self.keeper_dir = .68, -1
            elif self.keeper_x < .32:
                self.keeper_x, self.keeper_dir = .32, 1

            # Ball reaches keeper/goal area
            if self.ball_y >= .66:
                if abs(self.ball_x-self.keeper_x) < .075 and self.ball_y < .79:
                    self.message = "SAVED! The keeper got it."
                    self.finish_shot()
                elif .27 < self.ball_x < .73 and self.ball_y >= .82:
                    self.score += 1
                    self.message = "GOOOAL!!!"
                    self.finish_shot()
                elif self.ball_x <= .27 or self.ball_x >= .73 or self.ball_y > .88:
                    self.message = "MISSED! Try again."
                    self.finish_shot()
            if self.ball_x < .02 or self.ball_x > .98 or self.ball_y > .98:
                self.message = "MISSED!"
                self.finish_shot()
        self.redraw()

    def finish_shot(self):
        self.shooting = False
        if self.shots >= self.max_shots:
            self.game_over = True
            self.message = f"FULL TIME!  FINAL SCORE: {self.score}/5  -  TAP TO RESTART"
        else:
            self.reset_ball()

class FootballApp(App):
    def build(self):
        self.title = "Football Penalty"
        root = FloatLayout()
        root.add_widget(FootballGame())
        return root

if __name__ == "__main__":
    FootballApp().run()
