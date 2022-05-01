# This file is executed on every boot (including wake-boot from deepsleep)
import gc, time
from yolobit import *
import music
from rover import *
from rover_ir import *

stop_all()
rover.show_rgb_led(0, hex_to_rgb('#ff0000'))
display.set_all('#ff0000')
music.play(music.POWER_UP, wait=False)

print('Rover started and ready')

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
current_speed = 80
key = KEY_NONE
ble_connected = False

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

def ir_callback(cmd, addr, ext):
    global mode, mode_changed, current_speed, key
    if cmd == IR_REMOTE_A:
        mode = ROBOT_MODE_DO_NOTHING
        mode_changed = True
    elif cmd == IR_REMOTE_B:
        mode = ROBOT_MODE_AVOID_OBS
        mode_changed = True
    elif cmd == IR_REMOTE_C:
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
  global mode, mode_changed
  if chu_E1_BB_97i == ('!B516'):
    rover.forward(50)
  elif chu_E1_BB_97i == ('!B615'):
    rover.backward(50)
  elif chu_E1_BB_97i == ('!B714'):
    rover.turn_right(50)
  elif chu_E1_BB_97i == ('!B814'):
    rover.turn_left(50)
  elif chu_E1_BB_97i == ('!B11:'): #A
    mode = ROBOT_MODE_DO_NOTHING
    mode_changed = True
  elif chu_E1_BB_97i == ('!B219'): #B
    mode = ROBOT_MODE_AVOID_OBS
    mode_changed = True
  elif chu_E1_BB_97i == ('!B318'): #C
    mode = ROBOT_MODE_LINE_FINDER
    mode_changed = True
  #elif chu_E1_BB_97i == ('!B417'): #D
  #  rover.servo2.servo_write(90)
  else:
    rover.stop()
  
  if mode_changed:
    print('mode changed by app')

ble.on_receive_msg("string", on_ble_message_string_receive_callback)

try:
    while True :
        if mode_changed:
            if mode == ROBOT_MODE_DO_NOTHING:
                rover.show_rgb_led(0, hex_to_rgb('#ff0000'))
                key = KEY_NONE
            elif mode == ROBOT_MODE_AVOID_OBS:
                rover.show_rgb_led(0, hex_to_rgb('#00ff00'))
            elif mode == ROBOT_MODE_LINE_FINDER:
                rover.show_rgb_led(0, hex_to_rgb('#0000ff'))
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
                        rover.turn_left(current_speed/1.5)
                    elif key == KEY_RIGHT:
                        rover.turn_right(current_speed/1.5)
                    elif key == KEY_S1_CLOSE:
                        rover.servo1.servo_write(0)
                    elif key == KEY_S1_OPEN:
                        rover.servo1.servo_write(120)

                    key = KEY_NONE
                else:
                    rover.stop()
                rover_ir_rx.clear_code()
                time.sleep_ms(100)

        elif mode == ROBOT_MODE_AVOID_OBS:
            if rover.ultrasonic.distance_cm() < 15:
              rover.backward(50, 0.5)
              rover.turn_right(50, 0.25)
            else:
              rover.forward(50)

        elif mode == ROBOT_MODE_LINE_FINDER:
            if rover.read_line_sensors() == (1, 0, 0, 0):
              rover.turn_right(50)
            elif rover.read_line_sensors() == (1, 1, 0, 0):
              rover.turn_right(20)
            elif rover.read_line_sensors() == (0, 0, 0, 1):
              rover.turn_left(50)
            elif rover.read_line_sensors() == (0, 0, 1, 1):
              rover.turn_left(20)
            elif rover.read_line_sensors() == (0, 0, 0, 0):
              while not ((rover.read_line_sensors(0)) or (rover.read_line_sensors(1)) or (rover.read_line_sensors(2)) or (rover.read_line_sensors(3))):
                rover.backward(20)
            else:
              rover.forward(25)
            
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
    del mode, mode_changed, current_speed, ble_connected, key, on_ble_message_string_receive_callback, on_ble_connected_callback, on_ble_disconnected_callback, on_button_a_pressed
    gc.collect()
