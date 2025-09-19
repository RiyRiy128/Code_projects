import time
from turtle import Screen
from player import Player
from car_manager import CarManager
import random
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
scoreboard = Scoreboard()


screen.onkeypress(player.move_up,"w")
screen.listen()



game_is_on = True

car_manager = CarManager()

while game_is_on:

    #Stagger and generate car objects randomly. If not too many objects are created
    if random.randint(1,8) ==1:
        car_manager.create_car()
    #move all the cars forward
    car_manager.move_forward()

    #detect collisions with cars
    for car in car_manager.cars:
        if player.distance(car) < 30:
            scoreboard.game_over()
            game_is_on = False

    #detect finish line
    if player.ycor() > 280:
        scoreboard.increase_level()
        scoreboard.update_score()
        player.reset_position()
        car_manager.increase_speed()

    #remove the cars from memory/list
    for car in car_manager.cars:
        if car.xcor() < -320:
            index = car_manager.cars.index(car)
            car.hideturtle()
            car.clear()
            car_manager.cars.pop(index)
            del car


    time.sleep(0.1)
    screen.update()


screen.exitonclick()