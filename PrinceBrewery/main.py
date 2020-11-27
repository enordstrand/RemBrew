# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Implement Python Switch Case Statement using Dictionary


def state1():
    print("IT IS MONDAY")
    return "tuesday"
def state2():
    return "wednesday"
def state3():
    return "thursday"
def state4():
    return "friday"
def state5():
    return "saturday"
def state6():
    return "sunday"
def state7():
    return "sunday"
def state8():
    return "sunday"
def state9():
    return "sunday"
def state10():
    return "sunday"
def state11():
    return "sunday"
def state12():
    return "sunday"
def default():
    return "Incorrect day"

switcher = {
    1: state1,
    2: state2,
    3: state3,
    4: state4,
    5: state5,
    6: state6,
    7: state7,
    8: state8,
    9: state9,
    10: state10,
    11: state11,
    12: state12
    }

def switch(dayOfWeek):
    return switcher.get(dayOfWeek, default)()

    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    state = 1
    while (True):
        switch(state)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

