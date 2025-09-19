import random
import turtle
from turtle import Turtle, Screen


jim = Turtle()
tim = Turtle()
harry = Turtle()
barney = Turtle()
steven = Turtle()
john = Turtle()

jim.shape("turtle")
john.shape("turtle")
tim.shape("turtle")
harry.shape("turtle")
barney.shape("turtle")
steven.shape("turtle")

turtles = [jim,tim,john,harry,barney,steven]
colours = ["red","blue","green","yellow","magenta","cyan"]


def move_forward():
    jim.forward(10)

def move_backward():
    jim.backward(10)

def turn_counter_clockwise():
    jim.left(10)

def turn_clockwise():
    jim.right(10)

def clear_drawing():
    jim.clear()
    jim.home()



for i in range(len(turtles)):
    turtles[i].color(colours[i])


start_pos_y = -200

for turtle in turtles:
    turtle.forward(10)



for turtle in turtles:
    turtle.penup()
    turtle.setposition(-420,start_pos_y)
    start_pos_y +=80

finish_line = 425

end = False
screen = Screen()
guess = screen.textinput("Guess which turtle wins:","Which turtle do you think will win?")
while not end:
    #all move forward by some random space
    for turtle in turtles:
        turtle.forward(random.randint(0,10))

    for turtle in turtles:
        if turtle.xcor() >= finish_line:
            winner = turtle.color()[0]
            end = True

print(guess)
print(f"The winner is {winner}!")
if winner == guess:
    print("Congratulations!")

# screen.onkey(key="w", fun=move_forward)
# screen.onkey(key="s", fun=move_backward)
# screen.onkey(key="a", fun=turn_counter_clockwise)
# screen.onkey(key="d", fun=turn_clockwise)
# screen.onkey(key="c", fun=clear_drawing)
#
# screen.listen()
screen.exitonclick()