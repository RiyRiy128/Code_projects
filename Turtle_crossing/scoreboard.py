from turtle import Turtle


FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()

        self.hideturtle()
        self.score = 0
        self.color("black")
        self.penup()
        self.level = 1
        self.update_score()

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", align="center", font=FONT)

    def increase_level(self):
        self.level += 1
    def update_score(self):
        self.clear()
        self.goto(-235, 260)
        self.write(f"Level: {self.level}", align="center", font=FONT)
