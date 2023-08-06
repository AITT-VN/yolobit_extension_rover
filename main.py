# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import time
from yolobit import *
import music
from rover import *
from rover_ir import *

rover.stop()
stop_all()
rover.show_rgb_led(0, hex_to_rgb('#ff0000'))
display.set_all('#ff0000')
music.play(music.POWER_UP, wait=False)

ROBOT_MODE_DO_NOTHING = const(31)
ROBOT_MODE_AVOID_OBS = const(32)
ROBOT_MODE_FOLLOW = const(33)
ROBOT_MODE_LINE_FINDER = const(34)

KEY_NONE = const(0)
KEY_UP = const(1)
KEY_DOWN = const(2)
KEY_LEFT = const(3)
KEY_RIGHT = const(4)

KEY_S1_CLOSE = const(20)
KEY_S1_OPEN = const(21)

mode = ROBOT_MODE_DO_NOTHING
mode_changed = False
current_speed = 100
key = KEY_NONE
ble_connected = False

robot_types_name = ['Basic - Gripper', 'Basic - Ball Launcher',
                    'Tank - Gripper', 'Tank - Ball Launcher']
robot_types = [[0, 0], [0, 1], [1, 0], [1, 1]]

if device_config.get('robot_type', False):
    print('Finish loading robot type')
    robot_type = device_config['robot_type']
else:
    robot_type = [0, 0]

__robot_type = robot_types.index(robot_type)

print('Rover', robot_types_name[__robot_type], 'started and ready')


def on_button_a_pressed():
    global mode, mode_changed
    music.play(['G3:1'], wait=True)
    if mode == ROBOT_MODE_DO_NOTHING:
        mode = ROBOT_MODE_AVOID_OBS
    elif mode == ROBOT_MODE_AVOID_OBS:
        mode = ROBOT_MODE_FOLLOW
    elif mode == ROBOT_MODE_FOLLOW:
        mode = ROBOT_MODE_LINE_FINDER
    elif mode == ROBOT_MODE_LINE_FINDER:
        mode = ROBOT_MODE_DO_NOTHING

    mode_changed = True
    time.sleep_ms(100)
    print('mode changed by button')


button_a.on_pressed = on_button_a_pressed


def on_button_b_pressed():
    global mode, mode_changed, __robot_type, robot_type, robot_types
    if mode == ROBOT_MODE_DO_NOTHING:
        music.play(['G3:1'], wait=True)
        press_begin = time.ticks_ms()
        press_duration = 0

        while button_b.is_pressed():
            press_end = time.ticks_ms()
            press_duration = time.ticks_diff(press_end, press_begin)

            if press_duration > 2000:
                print('robot type processing...')
                __robot_type = (__robot_type if isinstance(
                    __robot_type, (int, float)) else 0) + 1
                if __robot_type > (len(robot_types) - 1):
                    __robot_type = 0
                display.scroll(__robot_type + 1)
                time.sleep_ms(1000)

        time.sleep_ms(2000)

        if __robot_type != robot_type:

            device_config['robot_type'] = robot_types[__robot_type]
            save_config()

            for count in range(3):
                display.set_all('#ffa500')
                time.sleep_ms(200)
                display.set_all('#000000')
                time.sleep_ms(200)

            reset()
        else:
            display.set_all('#000000')
            print('robot type exit without change.')


button_b.on_pressed = on_button_b_pressed


def ir_callback(cmd, addr, ext):
    global mode, mode_changed, current_speed, key
    if cmd == IR_REMOTE_A:
        mode = ROBOT_MODE_DO_NOTHING
        mode_changed = True
    elif cmd == IR_REMOTE_B:
        mode = ROBOT_MODE_AVOID_OBS
        mode_changed = True
    elif cmd == IR_REMOTE_C:
        mode = ROBOT_MODE_FOLLOW
        mode_changed = True
    elif cmd == IR_REMOTE_D:
        mode = ROBOT_MODE_LINE_FINDER
        mode_changed = True
    elif cmd == IR_REMOTE_E:
        key = KEY_S1_CLOSE
    elif cmd == IR_REMOTE_F:
        key = KEY_S1_OPEN
    elif cmd == IR_REMOTE_UP:
        key = KEY_UP
    elif cmd == IR_REMOTE_DOWN:
        key = KEY_DOWN
    elif cmd == IR_REMOTE_LEFT:
        key = KEY_LEFT
    elif cmd == IR_REMOTE_RIGHT:
        key = KEY_RIGHT
    elif cmd == IR_REMOTE_1:
        current_speed = 20
    elif cmd == IR_REMOTE_2:
        current_speed = 25
    elif cmd == IR_REMOTE_3:
        current_speed = 30
    elif cmd == IR_REMOTE_4:
        current_speed = 40
    elif cmd == IR_REMOTE_5:
        current_speed = 50
    elif cmd == IR_REMOTE_6:
        current_speed = 60
    elif cmd == IR_REMOTE_7:
        current_speed = 70
    elif cmd == IR_REMOTE_8:
        current_speed = 80
    elif cmd == IR_REMOTE_9:
        current_speed = 100

    if mode_changed:
        print('mode changed by IR remote')


rover_ir_rx.on_received(ir_callback)
rover_ir_rx.start()


def on_ble_connected_callback():
    global ble_connected
    display.set_all('#00ff00')
    ble_connected = True


ble.on_connected(on_ble_connected_callback)


def on_ble_disconnected_callback():
    global ble_connected
    display.set_all('#ff0000')
    ble_connected = False


ble.on_disconnected(on_ble_disconnected_callback)


def on_ble_message_string_receive_callback(chu_E1_BB_97i):
    global mode, mode_changed, current_speed, robot_types, robot_type
    if chu_E1_BB_97i == ('!B516'):
        if robot_type[0] == 0:
            rover.forward(50)
        else:
            rover.forward(100)
    elif chu_E1_BB_97i == ('!B615'):
        if robot_type[0] == 0:
            rover.backward(50)
        else:
            rover.backward(100)
    elif chu_E1_BB_97i == ('!B714'):
        if robot_type[0] == 0:
            rover.turn_left(50)
        else:
            rover.turn_left(90)
    elif chu_E1_BB_97i == ('!B814'):
        if robot_type[0] == 0:
            rover.turn_right(50)
        else:
            rover.turn_right(90)
    elif chu_E1_BB_97i == ('!B11:'):  # A
        if robot_type[1] == 0:
            rover.servo_write(1, 0)
        else:
            launch_ball()
    elif chu_E1_BB_97i == ('!B219'):  # B
        if robot_type[1] == 0:
            rover.servo_write(2, 90)
        else:
            shoot_ball()
    elif chu_E1_BB_97i == ('!B318'):  # C
        if robot_type[1] == 0:
            rover.servo_write(2, 0)
        else:
            decr_speed()
    elif chu_E1_BB_97i == ('!B417'):  # D
        if robot_type[1] == 0:
            rover.servo_write(1, 90)
        else:
            incr_speed()
    else:
        rover.stop()

    if mode_changed:
        print('mode changed by app')


ble.on_receive_msg("string", on_ble_message_string_receive_callback)


def on_ble_message_name_value_receive_callback(name, value):
    global current_speed, key, ble_key_received

    if name == 'F':
        rover.forward(value)
    elif name == 'B':
        rover.backward(value)
    elif name == 'L':
        rover.turn_left(value/1.5)
    elif name == 'R':
        rover.turn_right(value/1.5)
    elif name == 'S':
        current_speed = 80
        rover.stop()
    elif name == 'S1':
        rover.servo_write(1, value)
    elif name == 'S2':
        rover.servo_write(2, value)


ble.on_receive_msg("name_value", on_ble_message_name_value_receive_callback)


def incr_speed():
    global current_speed
    current_speed = (current_speed if isinstance(
        current_speed, (int, float)) else 0) + 5
    if current_speed >= 100:
        current_speed = 100


def decr_speed():
    global current_speed
    current_speed = (current_speed if isinstance(
        current_speed, (int, float)) else 0) + -5
    if current_speed < 20:
        current_speed = 20


def launch_ball():
    global current_speed
    rover.servo_write(1, 180)
    time.sleep_ms(1000)
    rover.servo_write(2, 180)
    time.sleep_ms(1000)
    rover.servo_write(1, 90)
    time.sleep_ms(1000)
    rover.servo_write(2, 20)
    time.sleep_ms(1000)


def shoot_ball():
    global current_speed
    rover.servo_write(1, 180)
    time.sleep_ms(1000)


try:
    while True:

        if mode_changed:
            if mode == ROBOT_MODE_DO_NOTHING:
                rover.show_rgb_led(0, hex_to_rgb('#ff0000'))
                key = KEY_NONE
            elif mode == ROBOT_MODE_AVOID_OBS:
                rover.show_rgb_led(0, hex_to_rgb('#0000ff'))
            elif mode == ROBOT_MODE_FOLLOW:
                rover.show_rgb_led(0, hex_to_rgb('#ff00ff'))
            elif mode == ROBOT_MODE_LINE_FINDER:
                rover.show_rgb_led(0, hex_to_rgb('#ffffff'))
            mode_changed = False

        if mode == ROBOT_MODE_DO_NOTHING:
            if ble_connected:
                # do nothing and wait for commands from bluetooth
                time.sleep_ms(500)
            else:
                if key != KEY_NONE:
                    if key == KEY_UP:
                        rover.forward(current_speed)
                    elif key == KEY_DOWN:
                        rover.backward(current_speed)
                    elif key == KEY_LEFT:
                        turn_speed = int(current_speed/3)
                        if turn_speed < 20:
                            turn_speed = 20
                        rover.turn_left(turn_speed)
                    elif key == KEY_RIGHT:
                        turn_speed = int(current_speed/3)
                        if turn_speed < 20:
                            turn_speed = 20
                        rover.turn_right(turn_speed)
                    elif key == KEY_S1_CLOSE:
                        rover.servo_write(1, 20)
                    elif key == KEY_S1_OPEN:
                        rover.servo_write(1, 90)

                    key = KEY_NONE
                else:
                    rover.stop()
                rover_ir_rx.clear_code()
                time.sleep_ms(100)

        elif mode == ROBOT_MODE_AVOID_OBS:
            if robot_type[0] == 0:
                if rover.ultrasonic.distance_cm() < 15:
                    rover.backward(50, 0.5)
                    rover.turn_right(50, 0.25)
                else:
                    rover.forward(50)
            else:
                if rover.ultrasonic.distance_cm() < 15:
                    rover.backward(90, 1)
                    rover.turn_right(90, 1)
                else:
                    rover.forward(90)

        elif mode == ROBOT_MODE_FOLLOW:
            obs_distance = rover.ultrasonic.distance_cm()

            if robot_type[0] == 0:
                if obs_distance < 15:
                    rover.backward(50)
                elif obs_distance < 30:
                    rover.stop()
                elif obs_distance < 50:
                    rover.forward(50)
                else:
                    rover.stop()
            else:
                if obs_distance < 15:
                    rover.backward(90)
                elif obs_distance < 30:
                    rover.stop()
                elif obs_distance < 50:
                    rover.forward(90)
                else:
                    rover.stop()
            time.sleep_ms(20)

        elif mode == ROBOT_MODE_LINE_FINDER:
            if robot_type[0] == 0:
                if rover.read_line_sensors() == (1, 0, 0, 0):
                    rover.turn_left(50)
                elif rover.read_line_sensors() == (1, 1, 0, 0):
                    rover.turn_left(30)
                elif rover.read_line_sensors() == (0, 0, 0, 1):
                    rover.turn_right(50)
                elif rover.read_line_sensors() == (0, 0, 1, 1):
                    rover.turn_right(30)
                elif rover.read_line_sensors() == (0, 0, 0, 0):
                    # while not ((rover.read_line_sensors(0)) or (rover.read_line_sensors(1)) or (rover.read_line_sensors(2)) or (rover.read_line_sensors(3))):
                    rover.backward(20)
                else:
                    rover.forward(25)

            else:
                if rover.read_line_sensors() == (1, 0, 0, 0):
                    rover.turn_left(100)
                elif rover.read_line_sensors() == (1, 1, 0, 0):
                    rover.turn_left(90)
                elif rover.read_line_sensors() == (0, 0, 0, 1):
                    rover.turn_right(100)
                elif rover.read_line_sensors() == (0, 0, 1, 1):
                    rover.turn_right(90)
                elif rover.read_line_sensors() == (0, 0, 0, 0):
                    # while not ((rover.read_line_sensors(0)) or (rover.read_line_sensors(1)) or (rover.read_line_sensors(2)) or (rover.read_line_sensors(3))):
                    rover.backward(80)
                else:
                    rover.forward(80)


except KeyboardInterrupt:
    print('Rover program stopped')
finally:
    rover.stop()
    button_a.on_pressed = None
    rover_ir_rx.on_received(None)
    rover_ir_rx.stop()
    ble.on_receive_msg("string", None)
    ble.on_connected(None)
    ble.on_disconnected(None)
    del mode, mode_changed, current_speed, ble_connected, key, on_ble_message_string_receive_callback, on_ble_connected_callback, on_ble_disconnected_callback, on_button_a_pressed, on_button_b_pressed, robot_type, robot_types
    gc.collect()
