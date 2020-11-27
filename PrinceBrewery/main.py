# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Implement Python Switch Case Statement using Dictionary


def state1():
    print("Close all valves and pumps")
    return 2
def state2():
    print("Fill HLT start")
    return 3
def state3():
    print("Initial heating for meshing 67 degrees")
    return 4
def state4():
    print("Fill mesh")
    return 5
def state5():
    print("FILL HLT for circulation")
    return 6
def state6():
    print("Heating HLT 80 degrees")
    return 7
def state7():
    print("Execute meshing")
    return 8
def state8():
    print("Circulation")
    return 9
def state9():
    print("Fill boil and heat")
    return 10
def state10():
    print("Rinse")
    return 11
def state11():
    print("Boil 90 min")
    return 12
def state12():
    print("Fill yeast bucket")
    return 0
def default():
    return "Brew finished"

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

def switch(state):
    return switcher.get(state, default)()

if __name__ == '__main__':
    state = 1
    while (state < 13):
        state = switch(state)
        print("next state is: " + str(state))

