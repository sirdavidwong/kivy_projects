from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class StartButton(Widget):
    visible = True

    def show(self):
        self.visible = True
        self.canvas.opacity = 1

    def hide(self):
        self.visible = False
        self.canvas.opacity = 0


class PongBall(Widget):

    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand..just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    start_button = ObjectProperty(None)

    def serve_ball(self, vel=Vector(4, 0).rotate(randint(0, 360))):
        self.ball.velocity = vel

    def reset(self):
        self.ball.center = self.center
        self.ball.velocity = (0, 0)
        self.start_button.show()

    def on_touch_down(self, touch):
        if self.start_button.visible:
            if touch.x < self.width / 2 + 10 and \
            touch.x > self.width / 2 - 10 and \
            touch.y < self.height / 2 + 25 and \
            touch.y > self.height / 2 - 25:
                self.start_button.hide()
                self.serve_ball()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def update(self, dt):
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off the top or the bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # track points made
        if self.ball.x < self.x:
            self.player2.score += 1
            self.reset()
        if self.ball.x > self.width:
            self.player1.score += 1
            self.reset()


class PongApp(App):
    def build(self):
        game = PongGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
