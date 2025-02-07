def days_to_units(num, conversion_unit):
    if conversion_unit == "hours":
        return f"{num} days is {num * 24} hours"
    elif conversion_unit == "minutes":
        return f"{num} days is {num * 60 * 24} minutes"
    else:
        return "unsupported unit"


def validate_and_execute(days_dic):
    try:

        number_wanted = int(days_dic["days"])
        # we only want to do conversions only for positive integers
        if number_wanted > 0:
            cv = days_to_units(number_wanted, days_dic["unit"])
            print(cv)
        elif number_wanted == 0:
            print("You have entered a 0, please use valid positive numbers ")
        else:
            print("You have entered a negative number, only enter a positive number")

    except ValueError:
        print("Your input was not a valid number try again")


user_input_message = "Hey user, enter a number of days and conversion units! (to quit enter exit):\n"
