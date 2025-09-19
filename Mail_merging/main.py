PLACEHOLDER = '[name]'
#read the names in the invited list

# with open("Input/Names/invited_names.txt","r") as file:
#     LIST_OF_NAMES = file.readlines()
#
# new_list = []
# #remove the white spaces-new lines
# for name in LIST_OF_NAMES:
#     index = LIST_OF_NAMES.index(name)
#     new_name = name.strip()
#     LIST_OF_NAMES[index] = new_name
#
# #create a method that reads the template letter
#
# def read_letter():
#     with open("Input/Letters/starting_letter.txt","r") as file:
#         content = file.readlines()
#     return content
# #A method that replaces the placeholder and writes a letter out
# def write_letter(letter, name):
#     for line in letter:
#         if line.__contains__("[name]"):
#             line = line.replace("[name]",name)
#         with open("Output/ReadyToSend/"+name+"_letter.txt","a") as file:
#             file.write(line)
#
# #write each letter from sample template
# for names in LIST_OF_NAMES:
#     write_letter(read_letter(),names)


#alternate (better simpler code sigh)

with open("Input/Names/invited_names.txt","r") as file:
    v2_names = file.readlines()

with open("Input/Letters/starting_letter.txt","r") as v2_file:
    v2_contents = v2_file.read()

    for names in v2_names:
        stripped_name = names.strip()
        v2_contents = v2_contents.replace(PLACEHOLDER,stripped_name)

        with open("Output/ReadyToSend/"+stripped_name+"_letter.txt","a") as file:
            file.write(v2_contents)

