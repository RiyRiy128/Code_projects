# with open("./weather_data.csv", "r") as file:
#     data = file.readlines()
#
# print(data)

# import csv
#
# with open("./weather_data.csv", "r") as file:
#     data = csv.reader(file)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#
# print(temperatures)

import pandas

# data = pandas.read_csv("weather_data.csv")
#
# print(data)
#
# # max_temp_index = data[data.temp == data.temp.max()].index
# max_temp_row = data[data.temp == data.temp.max()]
# print(max_temp_row)
#
# #f = C*1.8 + 32
#
# monday_temp = (data[data.day =="Monday"].temp)*(1.8) + 32
#
# print(monday_temp)
#
# data_dict = {
#     "Students" : ["Amy", "Bob", "Charlie"],
#     "Scores" : [76,80,50]
# }
#
# v2_data = pandas.DataFrame(data_dict)
# v2_data.to_csv("student_score.csv")
# print(v2_data)



#Essentially this logic reads census data for squirrels in central park and maps how many of the particular types of squirrels were seen
data = pandas.read_csv('2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv')

# print(data)

count_gray = data['Primary_Fur_Color'].value_counts()['Gray']
count_black = data['Primary_Fur_Color'].value_counts()['Cinnamon']
count_cinnamon = data['Primary_Fur_Color'].value_counts()['Black']

data_dict = {
    "fur color" : ["Gray", "Cinnamon", "Black"],
    "Count" : [count_gray,count_cinnamon,count_black]
}


new_data = pandas.DataFrame(data_dict)
new_data.to_csv('Squirrel_count.csv')
print(new_data)

