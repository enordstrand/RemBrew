from time import sleep

def coundtdown():
    global my_timer
    my_timer = 5
    for x in range(5):
        my_timer = my_timer - 1
        sleep(1)
    print("out of time")
