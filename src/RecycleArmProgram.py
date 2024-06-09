import random

# Nour and Ismail
global containers_used
containers_used = []  # tracks the container ids so they are not reused


def container_generator():
    global container  # set container variable to global to access it among all functions
    while len(containers_used) <= 6:  # to allow for a maximum of 6 contianers
        container = random.randint(1, 6)  # generates a random number from 1-6
        if container not in containers_used:  # make sure not to reuse same container ID
            containers_used.append(container)  # keep track of used containers
            return container


# Nour
def pick_up():
    arm.home()
    arm.move_arm(0.548, 0.048, 0.02)  # move arm to pick up location
    time.sleep(2)
    arm.control_gripper(35)  # hold container
    time.sleep(2)
    arm.move_arm(0.406, 0.0, 0.483)  # move arm to home


# Nour
def rotate_arm():
    tracker_initial = potentiometer.right()  # set initial tracker equal to initial position before any movement
    while potentiometer.right() <= 1.0:  # track arm location
        tracker_final = potentiometer.right()  # set final potentiometer equal to current arm location
        tracker_diff = tracker_final - tracker_initial  # find difference between final and initial arm location
        convert_to_deg = tracker_diff * 3.75 * 100  # convert potentiometer value to degree value
        if tracker_final > 0.5:  # if potentiometer > 0.5 move in positive direction
            arm.rotate_base(convert_to_deg)
        elif tracker_final < 0.5:  # if potentiometer < 0.5 move in negative direction
            arm.rotate_base(convert_to_deg)
        tracker_initial = tracker_final  # set initial position equal to old final position
        if rotation_checker(container) == "stop":  # checks if q-arm is above corresponding autoclave
            break


# Ismail
def rotation_checker(container):
    # check contianer number
    if (container == 1) or (container == 4):  # checks for red contianers
        while arm.check_autoclave("red") == True:
            return "stop"
    elif (container == 2) or (container == 5):
        while arm.check_autoclave("green") == True:  # checks for green containers
            return "stop"
    elif (container == 3) or (container == 6):
        while arm.check_autoclave("blue") == True:  # checks for blue containers
            return "stop"


# Ismail
def drop():  # function to drop off containers
    time.sleep(2)
    arm.control_gripper(-35)  # release container
    time.sleep(2)


# Nour
def drop_off(container):
    if (container == 1) or (container == 2) or (
            container == 3):  # tells user what to adjust potentiometer to according to contiainer id
        print("please adjust left potentiometer to greater than 50%")
    elif (container == 4) or (container == 5) or (container == 6):
        print("please adjust left potentiometer equal to 100%")
    while (potentiometer.left() <= 1.0):
        if (potentiometer.left() > 0.5) and (potentiometer.left() < 1.0):  # threshold 1 (small boxes)
            if container == 1:
                arm.move_arm(0.0, -0.594, 0.269)  # small red drop off location
                drop()
                break
            elif container == 2:
                arm.move_arm(-0.608, 0.233, 0.261)  # small green drop off location
                drop()
                break
            elif container == 3:
                arm.move_arm(0.0, 0.605, 0.302)  # small blue drop off location
                drop()
                break
        elif (potentiometer.left() == 1.0):  # threshold 2 (large boxes)
            if container == 4:
                arm.open_autoclave("red")
                time.sleep(1)
                arm.move_arm(-0.019, -0.363, 0.249)  # large red drop off location
                drop()
                arm.open_autoclave("red", False)
                break
            elif container == 5:
                arm.open_autoclave("green")
                time.sleep(1)
                arm.move_arm(-0.385, 0.103, 0.31)  # large green drop off location
                drop()
                arm.open_autoclave("green", False)
                break
            elif container == 6:
                arm.open_autoclave("blue")
                time.sleep(1)
                arm.move_arm(0.0, 0.351, 0.232)  # large blue drop off location
                drop()
                arm.open_autoclave("blue", False)
                break
    arm.home()


# Nour
def potentiometer_adjuster():
    message_checker = 0  # checks to make sure message is not repeated in loop
    while (potentiometer.left() <= 1.0) and (potentiometer.right() <= 1.0):  # track potentiometers
        message_checker += 1
        if (potentiometer.right() != 0.5) or (potentiometer.left() != 0.5):
            if message_checker == 1:
                print("please adjust both potentiometers to 50%")  # print message to adjust potentiometers
        elif (potentiometer.right() == 0.5) and (
                potentiometer.left() == 0.5):  # if both potentiometers are equal to 50% break loop and continue
            break


def main():  # main function that operates the entire program, takes a list of the containers
    counter = 0  # tracks number of boxes placed in autoclaves
    arm.activate_autoclaves()  # activate autoclaves
    while counter < 6:
        container_generator()  # generate container id
        potentiometer_adjuster()  # make sure both potentiometers are set to 50%
        arm.spawn_cage(container)  # spawn container generated from container_generator
        time.sleep(1)
        pick_up()  # pick up container
        rotate_arm()  # rotate to corresponding autoclave
        drop_off(container)  # drop off container using coordinates from container id
        counter = counter + 1
    arm.deactivate_autoclaves()  # once loop is complete deactivate autoclave and terminate program

