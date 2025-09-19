from turtle import Turtle

ALIGN = "center"
FONT = ("Courier",20,"normal")
class Scoreboard(Turtle):

    #Initialize attributes for board
    def __init__(self):
        super().__init__()

        self.score = 0
        self.highscore = int(self.read_score())
        self.color("white")
        self.hideturtle()
        self.penup()
        self.goto(0,275)
        self.display_score()

    
    def display_score(self):
        self.clear()
        self.write(f"Score: {self.score} Highscore:{self.highscore}", align=ALIGN, font=FONT)

    # def game_over(self):
    #     self.goto(0,0)
    #     self.write("Game Over.", align=ALIGN, font=FONT)

    #Read score from score(data) file
    def read_score(self):
        with open ("data.txt", "r") as file:
            content = file.read()
            return content


    #Helper for updating score
    def write_score(self):
        with open ("data.txt", "w") as file:
            file.write(str(self.highscore))
    #Populate high score        
    def high_score(self):
        if self.score > self.highscore:
            self.highscore = self.score
            self.score = 0
            self.display_score()
            self.write_score()
    
    #Increment score        
    def increase_score(self):
        self.score += 1
        self.display_score()