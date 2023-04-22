try:
    from yolobit import *
    import machine
    import neopixel
    from machine import *
    import time
    from utility import *
    import rover_pcf8574
    import rover_hcsr04
    from rover_ir import * 
    print('Import Rover done')

except KeyboardInterrupt as err:
    print('Import interrupted')
    for m in ['yolobit', 'machine', 'neopixel', 'rover_pcf8574', 'rover_hcsr04', 'rover_ir']:
        if m in sys.modules:
            del sys.modules[m]

# IR receiver
rover_ir_rx = IR_RX(Pin(pin4.pin, Pin.IN))


class Rover():

    def __init__(self):
        # motor pins
        self.ina1 = PWM(Pin(pin12.pin), freq=500, duty=0)
        self.ina2 = PWM(Pin(pin2.pin), freq=500, duty=0)

        self.inb1 = PWM(Pin(pin10.pin), freq=500, duty=0)
        self.inb2 = PWM(Pin(pin15.pin), freq=500, duty=0)

        self.servo1 = PWM(Pin(pin16.pin), freq=50, duty=0)
        self.servo2 = PWM(Pin(pin3.pin), freq=50, duty=0)

        self.m1_speed = 0
        self.m2_speed = 0

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
        self._rgb_leds = neopixel.NeoPixel(
            machine.Pin(pin6.pin), self._num_leds)

        self.show_led(0, 0)

        self.stop()

        say('Rover setup done!')

    def forward(self, speed, t=None):
        self.set_wheel_speed(speed, speed)
        if t != None:
            time.sleep(t)
            self.stop()

    def backward(self, speed, t=None):
        self.set_wheel_speed(-speed, -speed)
        if t != None:
            time.sleep(t)
            self.stop()

    def turn_right(self, speed, t=None):
        self.set_wheel_speed(speed, -speed)
        if t != None:
            time.sleep(t)
            self.stop()

    def turn_left(self, speed, t=None):
        self.set_wheel_speed(-speed, speed)
        if t != None:
            time.sleep(t)
            self.stop()

    def stop(self):
        self.set_wheel_speed(0, 0)
        time.sleep_ms(20)

    def set_wheel_speed(self, m1_speed, m2_speed):
        # logic to smoothen motion, avoid voltage spike
        # if wheel speed change > 30, need to change to 30 first
        if (m1_speed != 0 and abs(m1_speed - self.m1_speed) > 30) and (m2_speed != 0 and abs(m2_speed - self.m2_speed) > 30):
            if m1_speed > 0:
                # Forward
                self.ina1.duty(int(translate(30, 0, 100, 0, 1023)))
                self.ina2.duty(0)
            elif m1_speed < 0:
                # Backward
                self.ina1.duty(0)
                self.ina2.duty(int(translate(30, 0, 100, 0, 1023)))

            if m2_speed > 0:
                # Forward
                self.inb1.duty(int(translate(30, 0, 100, 0, 1023)))
                self.inb2.duty(0)
            elif m2_speed < 0:
                # Backward
                self.inb1.duty(0)
                self.inb2.duty(int(translate(30, 0, 100, 0, 1023)))

            time.sleep_ms(200)

        if m1_speed > 0:
            # Forward
            self.ina1.duty(int(translate(abs(m1_speed), 0, 100, 0, 1023)))
            self.ina2.duty(0)
        elif m1_speed < 0:
            # Backward
            self.ina1.duty(0)
            self.ina2.duty(int(translate(abs(m1_speed), 0, 100, 0, 1023)))
        else:
            # Release
            self.ina1.duty(0)
            self.ina2.duty(0)

        if m2_speed > 0:
            # Forward
            self.inb1.duty(int(translate(abs(m2_speed), 0, 100, 0, 1023)))
            self.inb2.duty(0)
        elif m2_speed < 0:
            # Backward
            self.inb2.duty(int(translate(abs(m2_speed), 0, 100, 0, 1023)))
            self.inb1.duty(0)
        else:
            # Release
            self.inb1.duty(0)
            self.inb2.duty(0)

        self.m1_speed = m1_speed
        self.m2_speed = m2_speed

    def read_line_sensors(self, index=0):
        '''
        self.pcf.pin(0) = 0 white line
        self.pcf.pin(0) = 1 black line
        '''
        if index < 0 or index > 4:
            return 1

        if index == 0:
            if self.pcf:
                return (self.pcf.pin(0), self.pcf.pin(1), self.pcf.pin(2), self.pcf.pin(3))
            else:
                return (1, 1, 1, 1)  # cannot detect black line
        else:
            if self.pcf:
                return self.pcf.pin(index-1)
            else:
                return 1

    def show_led(self, index, state):
        if self.pcf:
            if index == 0:  # both led
                self.pcf.pin(4, state)
                self.pcf.pin(5, state)
            elif index == 1:  # left led
                self.pcf.pin(4, state)
            elif index == 2:  # right led
                self.pcf.pin(5, state)
        else:
            pass

    def show_rgb_led(self, index, color, delay=None):
        if index == 0:
            for i in range(self._num_leds):
                self._rgb_leds[i] = color

            self._rgb_leds.write()

        elif (index > 0) and (index <= self._num_leds):
            self._rgb_leds[index - 1] = color
            self._rgb_leds.write()

        if delay != None:
            time.sleep(delay)
            if index == 0:
                for i in range(self._num_leds):
                    self._rgb_leds[i] = (0, 0, 0)

                self._rgb_leds.write()

            elif (index > 0) and (index <= self._num_leds):
                self._rgb_leds[index - 1] = (0, 0, 0)
                self._rgb_leds.write()

    def servo_write(self, index, value, max=180):
        if index not in [1, 2]:
            print("Servo index out of range")
            return None
        if value < 0 or value > max:
            print("Servo position out of range. Must be from 0 to " +
                  str(max) + " degree")
            return

        # duty for servo is between 25 - 115
        duty = 25 + int((value/max)*100)

        if index == 1:
            self.servo1.duty(duty)
        else:
            self.servo2.duty(duty)

    def servo360_write(self, index, value):
        if value < -100 or value > 100:
            print("Servo 360 speed out of range. Must be from -100 to 100")
            return

        if value == 0:
            self.servo_write(index, 0)
            return
        else:
            degree = 90 - (value/100)*90
            self.servo_write(index, degree)

    def move(self, dir, speed=None):

        # calculate direction based on angle
        #         90(3)
        #   135(4) |  45(2)
        # 180(5)---+----Angle=0(dir=1)
        #   225(6) |  315(8)
        #         270(7)

        if speed == None:
            speed = self._speed

        if dir == 1:
            self.turn_right(speed/2)

        elif dir == 2:
            self.set_wheel_speed(speed, speed/2)

        elif dir == 3:
            self.forward(speed)

        elif dir == 4:
            self.set_wheel_speed(speed/2, speed)

        elif dir == 5:
            self.turn_left(speed/2)

        elif dir == 6:
            self.set_wheel_speed(-speed/2, -speed)

        elif dir == 7:
            self.backward(speed)

        elif dir == 8:
            self.set_wheel_speed(-speed, -speed/2)

        else:
            self.stop()


rover = Rover()


def stop_all():  # override stop function called by app
    rover.stop()

