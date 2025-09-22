import random
import turtle
from turtle import Turtle
from random import randint

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10

#The screen width is 600, cars are generated off screen and move left
#cars are generated along the y-axis


class CarManager(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.cars = []
        self.move_speed = STARTING_MOVE_DISTANCE
    def create_car(self):
        car = turtle.Turtle()
        car.shape("square")
        car.setheading(180)
        car.color(random.choice(COLORS))
        car.shapesize(stretch_wid=1, stretch_len=2)
        car.penup()
        car.goto(320,random.randint(-260,280))
        self.cars.append(car)
    def increase_speed(self):
        self.move_speed += MOVE_INCREMENT

    def move_forward(self):
        for car in self.cars:
            car.forward(self.move_speed)


