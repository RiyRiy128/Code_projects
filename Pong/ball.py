from turtle import Turtle

#Ball class defines the behaviour of ball movement and positioning
class Ball(Turtle):
    def __init__(self):
        super().__init__()

        self.penup()
        self.shape("circle")
        self.color("white")
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1
    def move(self):

        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):

        self.y_move *= -1
        self.move_speed *= 0.6

    def bounce_x(self):

        self.x_move *= -1

    def reset_ball(self):

        self.goto(0, 0)
        self.bounce_x()
        self.move_speed = 0.1

    def ball_speed(self):
        if self.speed() < 10:
            new_speed = self.speed() + 1
            self.speed(new_speed)