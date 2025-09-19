from turtle import Turtle, Screen
import time
from snake import Snake
from Food import Food
from scoreboard import Scoreboard
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake game")
screen.tracer(0)


#Initialize Snake
snake = Snake()

#Initialize food 
food = Food()

#Initialize scoreboard
scoreboard = Scoreboard()


#Initialize screen
screen.listen()
screen.onkey(snake.up,"Up")
screen.onkey(snake.down,"Down")
screen.onkey(snake.left,"Left")
screen.onkey(snake.right,"Right")
game_is_on = True


while game_is_on:
    screen.update()
    time.sleep(0.1)

    snake.move()

    
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        # game_is_on = False
        scoreboard.high_score()
        snake.reset_snake()

    for segment in snake.snake[1:]:
        if snake.head.distance(segment) < 10:
            # game_is_on = False
            scoreboard.high_score()
            snake.reset_snake()

screen.exitonclick()