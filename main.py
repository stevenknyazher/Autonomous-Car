import machine
import utime

# Pico LED
ONBOARD_LED = machine.Pin(25, machine.Pin.OUT)

# Motor pins
IN1 = machine.Pin(6, machine.Pin.OUT)
IN2 = machine.Pin(7, machine.Pin.OUT)
EN_A = machine.Pin(8, machine.Pin.OUT)
IN3 = machine.Pin(4, machine.Pin.OUT)
IN4 = machine.Pin(3, machine.Pin.OUT)
EN_B = machine.Pin(2, machine.Pin.OUT)

# Infrared sensor pins
IR_RIGHT = machine.Pin(27, machine.Pin.IN)
IR_LEFT = machine.Pin(26, machine.Pin.IN)

# Ultrasonic sensor pins
ECHO = machine.Pin(19, machine.Pin.IN)
TRIG = machine.Pin(18, machine.Pin.OUT)

def left():
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)

def right():
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)

def forward():
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)

def back():
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)

def stop():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)

def get_distance():
    echo_timeout = 3000
    TRIG.value(0)
    utime.sleep_ms(50)
    TRIG.value(1)
    utime.sleep_ms(50)
    TRIG.value(0)

    start = utime.ticks_us()
    end = start

    while ECHO.value() == 0:
        if utime.ticks_us() - start > echo_timeout:
            return -1
        start = utime.ticks_us()

    while ECHO.value() == 1:
        end = utime.ticks_us()
        if utime.ticks_us() - start > echo_timeout:
            return -1

    cms = (end - start) / 2 / 29.1
    if cms > 0:
        return cms
    return -1

def main():
    ONBOARD_LED.init(machine.Pin.OUT)
    IN1.init(machine.Pin.OUT)
    IN2.init(machine.Pin.OUT)
    EN_A.init(machine.Pin.OUT)
    IN3.init(machine.Pin.OUT)
    IN4.init(machine.Pin.OUT)
    EN_B.init(machine.Pin.OUT)
    IR_RIGHT.init(machine.Pin.IN)
    IR_LEFT.init(machine.Pin.IN)
    ECHO.init(machine.Pin.IN)
    TRIG.init(machine.Pin.OUT)

    pwm_a = machine.PWM(EN_A)
    pwm_a.freq(50)
    pwm_a.duty_u16(16383)
    
    pwm_b = machine.PWM(EN_B)
    pwm_b.freq(50)
    pwm_b.duty_u16(16383)
    
    while True:
        ONBOARD_LED.value(1)

        ir_right_state = IR_RIGHT.value()
        ir_left_state = IR_LEFT.value()

        distance = get_distance()

        if distance <= 15 and distance != -1:
            stop()
            utime.sleep_ms(100)
        else:
            if ir_right_state == 0 and ir_left_state == 1:
                right()
            if ir_right_state == 1 and ir_left_state == 0:
                left()
            if ir_right_state == 1 and ir_left_state == 1:
                stop()
            if ir_right_state == 0 and ir_left_state == 0:
                forward()

        utime.sleep_ms(1)

if __name__ == '__main__':
    main()
