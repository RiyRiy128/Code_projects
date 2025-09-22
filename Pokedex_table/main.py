# import another_module
#
# print(another_module.another_module)
#
# from turtle import Turtle,Screen
#
# johnny = Turtle()
# johnny.shape("turtle")
# johnny.color("red")
#
# my_screen = Screen()
# print(my_screen.canvheight)
# my_screen.exitonclick()


#Essentially just maps the Pokemon out by their element type in a table
from prettytable import PrettyTable

table = PrettyTable()

table.add_column("Pokemon Name",["Pikachu","Squirtle","Charmander"], align = "l")
table.add_column("Type",["Electric","Water","Fire"], align = "l")
align = "c"



print(table)



