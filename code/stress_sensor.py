import RPi.GPIO as GPIO
import time

class stress_sensor_driver:
    
    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.DOUT, GPIO.IN)
        GPIO.setup(self.SCK, GPIO.OUT)


    def __init__(self, dout, sck, gap_value):
        self.DOUT = dout
        self.SCK = sck
        self.GapValue = gap_value
        self.setup()

    def set_sck_high(self):
        GPIO.output(self.SCK, GPIO.HIGH)

    def set_sck_low(self):
        GPIO.output(self.SCK, GPIO.LOW)

    def read_dout(self):
        return GPIO.input(self.DOUT)

class stress_sensor_process:
    
    # default pin: DOUT = 11, SCK = 13, default gap_value = 400
    def __init__(self, dout = 11, sck = 13, gap_value = 400):
        self.zero = 0
        self.value = 0
        self.filtered_value = 0 # to do: fileter function
        self.sensor = stress_sensor_driver(dout, sck, gap_value)

    def read_value(self):
        cout = 0
        self.sensor.set_sck_low()
        time.sleep(1e-6)

        # data is ready after DOUT is pulled down
        while(self.sensor.read_dout() == 1):
            pass

        # read 24 bit for 24 clk high
        for _ in range(0,24):
            self.sensor.set_sck_high()
            cout = cout << 1
            self.sensor.set_sck_low()
            cout += self.sensor.read_dout() & 0x1
        
        self.sensor.set_sck_high()
        cout = cout ^ 0x8000000 # convert the value at 25th clk high
        self.sensor.set_sck_low()
        self.value = cout

        print("raw value: " + self.value)
        return self.value
    
    # alpha filter
    def filter_value(filtered_value, cur_value):
        ret = filtered_value * 0.1 + cur_value * 0.9 
        return ret
        
    def get_filtered_value(self):
        print("============================================================")
        self.filtered_value = self.read_value()
        print("filtered value: " + self.value)     

        for _ in range(1, 20):
            self.filtered_value = filter_value(self.filtered_value, self.read_value())
            print("filtered value: " + self.value) 
            time.sleep(0.01)    

        print("============================================================")
    
    # external API to set zero
    def set_zero(self):
        self.get_filtered_value()
        self.zero = self.filter_value
        print("Set zero done!")

    # external API to get the current weight
    def get_weight(self):
        self.get_filtered_value()
        weight = (self.filter_value - self.zero)/self.sensor.GapValue


# test function
if __name__ == "__main__":
    sensor_test = stress_sensor_process(11, 13, 400)
    sensor_test.set_zero()

    input("Put item and press Enter to continue!")    
    sensor_test.get_weight()

    GPIO.cleanup()




        






        

        

    