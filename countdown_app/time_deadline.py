from datetime import datetime

# the date is a string, so you have to use datetime module
# use datetime.strptime to change it to a date
user_input = ""
while user_input != "exit":
    user_input = input("enter your goal with a deadline, separated by colon (type exit to stop)\n")
    input_list = user_input.split(":")
    goal = input_list[0]
    deadline_date = input_list[1]
    date = datetime.strptime(deadline_date, "%m.%d.%Y")

# calculate how may days from now till deadline

    today = datetime.today()
    math = date - today
    print(f"dear user for your goal of {goal} is {math.days} days\n")
