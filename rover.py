from yolobit import *
import machine, neopixel
import time
from utility import *
import rover_pcf8574
import rover_hcsr04
from rover_ir import *

# IR receiver
rover_ir_rx = IR_RX(Pin(pin4.pin, Pin.IN))

class Rover():

    def __init__(self):
        # motor pins
        self.ina1 = pin12
        self.ina2 = pin2

        self.inb1 = pin10
        self.inb2 = pin15

        self.servo1 = pin16
        self.servo2 = pin6
        
        self.servo1.servo_release()
        self.servo2.servo_release()
        
        # line IR sensors
        try:
            self.pcf = rover_pcf8574.PCF8574(
                machine.SoftI2C(
                    scl=machine.Pin(22), 
                    sda=machine.Pin(21)), 0x23)
        except:
            say('Line IR sensors not detected')
            self.pcf = None

        # ultrasonic
        self.ultrasonic = rover_hcsr04.HCSR04(pin13.pin, pin14.pin)

        # RGB leds
        self._num_leds = 6
        self._rgb_leds = neopixel.NeoPixel(machine.Pin(pin11.pin), self._num_leds)

        self.show_led(0, 0)

        say('Rover setup done!')

    def forward(self, speed, t=None):
        self.set_wheel_speed(speed, speed)
        if t != None :
            time.sleep(t)
            self.stop()

    def backward(self, speed, t=None):
        self.set_wheel_speed(-speed, -speed)
        if t != None :
            time.sleep(t)
            self.stop()

    def turn_right(self, speed, t=None):
        self.set_wheel_speed(speed, -speed)
        if t != None :
            time.sleep(t)
            self.stop()

    def turn_left(self, speed, t=None):
        self.set_wheel_speed(-speed, speed)
        if t != None :
            time.sleep(t)
            self.stop()

    def stop(self):
        self.set_wheel_speed(0, 0)
        time.sleep_ms(20)

    def set_wheel_speed(self, m1_speed, m2_speed):
        if m1_speed > 0:
            # Forward
            self.ina1.write_analog(int(translate(abs(m1_speed), 0, 100, 0, 1023)))
            self.ina2.write_analog(0)
        elif m1_speed < 0:
            # Backward
            self.ina1.write_analog(0)
            self.ina2.write_analog(int(translate(abs(m1_speed), 0, 100, 0, 1023)))
        else:
            # Release
            self.ina1.write_analog(0)
            self.ina2.write_analog(0)

        if m2_speed > 0:
            # Forward
            self.inb1.write_analog(int(translate(abs(m2_speed), 0, 100, 0, 1023)))
            self.inb2.write_analog(0)
        elif m2_speed < 0:
            # Backward
            self.inb2.write_analog(int(translate(abs(m2_speed), 0, 100, 0, 1023)))
            self.inb1.write_analog(0)
        else:
            # Release
            self.inb1.write_analog(0)
            self.inb2.write_analog(0)

    def read_line_sensors(self, index=None):
        '''
        self.pcf.pin(0) = 0 white line
        self.pcf.pin(0) = 1 black line
        '''
        if index == None:
            if self.pcf:
                return (self.pcf.pin(0), self.pcf.pin(1), self.pcf.pin(2), self.pcf.pin(3))
            else:
                return (1, 1, 1, 1) # cannot detect black line
        else:
            if self.pcf:
                return self.pcf.pin(index)
            else:
                return 1

    def show_led(self, index, state):
        if self.pcf:
            if index == 0: # both led
                self.pcf.pin(4, state)
                self.pcf.pin(5, state)
            elif index == 1: # left led
                self.pcf.pin(4, state)
            elif index == 2: # right led
                self.pcf.pin(5, state)
        else:
            pass

    def show_rgb_led(self, index, color, delay=None):
        if index == 0:
            for i in range(self._num_leds):
                self._rgb_leds[i] = color

            self._rgb_leds.write()

        elif (index > 0) and (index <= self._num_leds) :
            self._rgb_leds[index - 1] = color
            self._rgb_leds.write()

        if delay != None:
            time.sleep(delay)
            if index == 0:
                for i in range(self._num_leds):
                    self._rgb_leds[i] = (0, 0, 0)

                self._rgb_leds.write()

            elif (index > 0) and (index <= self._num_leds) :
                self._rgb_leds[index - 1] = (0, 0, 0)
                self._rgb_leds.write()

rover = Rover()

def stop_all(): # override stop function called by app
  rover.stop()
  rover.servo1.servo_release()
  rover.servo2.servo_release()
  rover.show_rgb_led(0, hex_to_rgb('#00000'))
  rover.show_led(0, 0)

