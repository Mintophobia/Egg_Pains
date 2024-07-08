import RPi.GPIO as GPIO
import time

class stepper_motor_driver():

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PULSE_P, GPIO.OUT)
        GPIO.setup(self.DIR_P, GPIO.OUT)

    # default pin: PULSE_P = ?, DIR_P = ?, default peed = ?
    def __init__(self, pulse_p, dir_p, m_step):
        self.PULSE_P = pulse_p
        self.DIR_P = dir_p
        self.cur_dir = 1 #default diretion
        self.m_step = m_step
        self.setup()

    def set_pulse_p_high(self):
        GPIO.output(self.PULSE_P, GPIO.HIGH)

    def set_pulse_p_low(self):
        GPIO.output(self.PULSE_P, GPIO.LOW)

    def set_dir_anticlock(self):
        GPIO.output(self.DIR_P, GPIO.HIGH)
        self.cur_dir = 1

    def set_dir_clockwise(self):
        GPIO.output(self.DIR_P, GPIO.LOW)
        self.cur_dir = 0

    def rev_dir(self):
        if self.cur_dir == 1:
            self.set_dir_clockwise()
        else:
            self.set_dir_anticlock()

    def set_m_step(self, m_step):
        self.m_step = m_step

    # return m step for client to cal speed
    def get_m_step(self):
        return self.m_step


class stepper_motor_process():

    def __init__(self, pulse_p = 11, dir_p = 13, m_step = 200, speed = 1):
      self.speed = speed
      self.motor = stepper_motor_driver(pulse_p, dir_p, m_step)

    def set_speed(self, speed):
      self.speed = speed # speed: round per second

    def set_dir(self, dir):
        if dir == 1:
            self.motor.set_dir_anticlock()
        else: 
            self.motor.set_dir_clockwise()

    def drive_motor_by_step(self, step):
        m_step = self.motor.get_m_step()
        delay = self.speed / (2 * m_step);
        for _ in range(step * m_step):
            self.motor.set_pulse_p_high()
            time.sleep(delay)
            self.motor.set_pulse_p_low()
            time.sleep(delay)

    def drive_motor_by_dir_step(self, dir, step):
        self.set_dir(dir)
        self.drive_motor_by_step(step)

    def drive_motor_by_speed_dir_step(self, speed, dir, step):
        self.speed(speed)
        self.drive_motor_by_dir_step(dir, step)


# test function
if __name__ == "__main__":
    motor_test = stepper_motor_process(11, 13, 200)

    # to do: input speed, dir, and step
    input("Press Enter to continue, will drive motor by 10 steps!")    
    motor_test.drive_motor_by_speed_dir_step(1, 1, 10)

    GPIO.cleanup()