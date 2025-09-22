
#Coffee machine implementation that outputs what coffee you may purchase given the ingredients and money inserted

#Menu and ingredient quantities used to make them
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

#Initialize ingredient quanities as resource pool
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

#Initialize money
money = 0

#Returns resource and money quanities left
def report_print(resources,money):

    for x in resources:
        print(f"{x}: {resources[x]}")
    print(f"Money: ${money}")


def remaining_resources(resources):

    water = resources["water"]
    milk = resources["milk"]
    coffee = resources["coffee"]



    return water,milk,coffee

    #returns the resources available

#Choice main that performs coffee production    
def choice_cost(menu,choice):

    cost = menu[choice]['cost']
    if choice == "espresso":
        ingredient_usage = menu[choice]['ingredients']
        water_usage = ingredient_usage['water']
        coffee_usage = ingredient_usage['coffee']
        milk_usage = 0
        return cost, water_usage, milk_usage, coffee_usage

    else:
        ingredient_usage = menu[choice]['ingredients']
        water_usage = ingredient_usage['water']
        milk_usage = ingredient_usage['milk']
        coffee_usage = ingredient_usage['coffee']



        return cost,water_usage,milk_usage,coffee_usage

    #returns a tuple with cost of coffee and how much resources it uses


#Helper to subtract usage for resources and validate if enough is left
def use_resources(resources,choice_test,money):

    if resources['water'] >= choice_test[1]:
        resources['water'] -= choice_test[1]
        change= money - choice_test[0]
        return change
    else:
        insufficient = "Sorry there is not enough water."
        return insufficient
    if resources['milk'] >= choice_test[2]:
        resources['milk'] -= choice_test[2]
        change = money - choice_test[0]
        return change
    else:
        insufficient = "Sorry there is not enough milk."
        return insufficient
    if resources['coffee'] >= choice_test[3]:
        resources['coffee'] -= choice_test[3]
        change = money - choice_test[0]
        return change
    else:
        insufficient = "Sorry there is not enough coffee."
        return insufficient

#Insertion of 'money' here via coin values
def coins_money(money, quarters,dimes,nickles,pennies):
    print("Please insert coins.")
    quarters =  0.25 * int(input("How many quarters?: "))
    nickles =  0.05 * int(input("How many nickles?:" ))
    pennies =  0.01 * int(input("How many pennies?:" ))
    dimes =  0.1 * int(input("How many dimes?:" ))

    money += quarters + nickles + pennies + dimes

    return money,quarters,nickles,pennies,dimes


money = 0
quarters = 0
nickles = 0
pennies = 0
dimes = 0

end_of_coffee = False

#Main loop to run coffee machine
while not end_of_coffee:

    selection = input("What would you like to drink? (espresso, latte, cappuccino):")

    if selection == "report":
        report_print(resources,money)

    elif selection == "espresso" or selection == "latte" or selection == "cappuccino":
        inserted_money = coins_money(money,quarters,nickles,pennies,dimes)
        money = inserted_money[0]
        coffee_choice_resource = choice_cost(MENU,selection)[0]
        coffee_choice_test = choice_cost(MENU,selection)

        if money >= coffee_choice_resource:

            result = use_resources(resources,coffee_choice_test,money)
            if type(result) == float:
                print(f"This is the change left: ${result}")
                print(f"Here is your {selection}. Enjoy!")
            else:
                print(result)
        else:
            print("Sorry, you don't have enough money.")



