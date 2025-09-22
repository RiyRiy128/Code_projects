from turtle import Screen,Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
screen.tracer(0)



screen.bgcolor("black")
screen.setup(width=800, height=600)

paddle_one = Paddle((350,0))
paddle_two = Paddle((-350,0))
ball = Ball()
scoreboard = Scoreboard()


screen.onkey(paddle_one.move_up, "Up")
screen.onkey(paddle_one.move_down,"Down")
screen.onkey(paddle_two.move_up, "w")
screen.onkey(paddle_two.move_down,"s")

screen.listen()

game_is_on = True

while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    #detect wall collision
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    #detect paddle collision
    if ball.distance(paddle_one) < 50 and ball.xcor() > 320 or ball.distance(paddle_two) < 50 and ball.xcor() < -320:
        ball.bounce_x()
        #ball.ball_speed()


    #detect if ball goes outside boundary
    if ball.xcor() > 380:
        ball.reset_ball()
        scoreboard.update_l_score()
    if ball.xcor() < -380:
        ball.reset_ball()
        scoreboard.update_r_score()
screen.exitonclick()



