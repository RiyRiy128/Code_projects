from turtle import Turtle

#_Initialize attribute values initial snake parameters
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
class Snake:

    def __init__(self):

        self.snake = []
        self.create_snake()
        self.head = self.snake[0]
        self.tail = self.snake[-1]

    def create_snake(self):

        for position in STARTING_POSITIONS:
            self.add_segment(position)

    #defines extension of snake
    def add_segment(self, position):
        new_segment = Turtle(shape="square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.snake.append(new_segment)

    #Snake length increase
    def extend(self):
        self.add_segment(self.tail.position())

    #Move coordinates and segments 
    def move(self):

        for seg_num in range(len(self.snake) - 1, 0, -1):
            new_segment_x = self.snake[seg_num - 1].xcor()
            new_segment_y = self.snake[seg_num - 1].ycor()
            self.snake[seg_num].goto(new_segment_x, new_segment_y)
        self.head.forward(MOVE_DISTANCE)


    #Movement set helper functions
    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    #Snake death
    def reset_snake(self):
        for seg in self.snake:
            seg.hideturtle()
        self.snake.clear()
        self.create_snake()
        self.head = self.snake[0]