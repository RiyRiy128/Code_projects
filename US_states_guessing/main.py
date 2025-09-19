import turtle
import pandas

screen = turtle.Screen()
screen.title("U.S States")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

map_writer = turtle.Turtle()
text_box = turtle.Screen()


map_writer.penup()
map_writer.hideturtle()
map_writer.speed("fastest")

data = pandas.read_csv("50_states.csv")

# all_states = data["state"].values
all_states = data.state.to_list()
print(all_states)


correct_states_list = []



while len(correct_states_list) < 50:

    answer_state = text_box.textinput(title=f"{len(correct_states_list)}/50 States guessed",prompt="Give another state: ")

    if answer_state is None or answer_state == "exit":
        missing_states = []

        for state in all_states:
            if state not in correct_states_list:
                missing_states.append(state)
        # print(missing_states)
        # print(len(missing_states))
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("missing_states.csv")
        break

    if answer_state.capitalize() in all_states:
        # state_row = data[data["state"] == answer_state.capitalize()]
        state_row = data[data.state == answer_state.capitalize()]
        correct_states_list.append(answer_state.capitalize())
        map_writer.goto(int(state_row.x),int(state_row.y)) #could also convert it to int to resolve error
        map_writer.write(f"{answer_state.capitalize()}", align="center", font=("Courier", 8, "normal"))



screen.exitonclick()