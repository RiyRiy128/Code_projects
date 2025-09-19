import turtle
import colorgram
import turtle as t
import random
t.colormode(255)


#Extracts the colour pallete from the image in the project folder
colours = colorgram.extract('image.jpg',30)

rgbList = []

#Map the colours for turtle
for colour in colours:
    r = colour.rgb.r
    g = colour.rgb.g
    b = colour.rgb.b
    rgbList.append((r,g,b))

print(rgbList)
# colours = [(218, 154, 109), (131, 172, 195), (213, 131, 150), (223, 71, 90), (238, 209, 100), (27, 119, 153), (124, 181, 155), (39, 122, 87), (26, 165, 201), (237, 163, 177), (217, 84, 75), (144, 83, 59), (152, 65, 84), (237, 169, 157), (48, 166, 133), (170, 148, 69), (178, 185, 214), (160, 209, 177), (6, 89, 109), (26, 90, 59), (25, 54, 76), (150, 207, 221), (51, 58, 87), (96, 125, 176), (233, 213, 8), (213, 12, 45)]

johnny = turtle.Turtle()
johnny.hideturtle()
johnny.speed("fastest")
johnny.penup()
johnny.setposition(-200,-100)

#Draw the Hirsch painting
for i in range(0,10):
    for i in range(0,10):
        johnny.dot(20, random.choice(rgbList))
        johnny.forward(50)


    johnny.setx(-200)
    johnny.sety(johnny.ycor() + 50)

screen = t.Screen()
screen.exitonclick()