import RPi.GPIO as GPIO #type: ignore
import time
from hx711 import HX711 #type: ignore
import LOADCELL #type: ignore



LOADCELL_DOUT_PIN = 16     
LOADCELL_SCK_PIN = 27   
SERVO_PIN_B = 32        


GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN_B, GPIO.OUT)

servoB = GPIO.PWM(SERVO_PIN_B, 50)  
servoB.start(0)  

# HX711 to loadcell
hx = HX711(dout_pin=LOADCELL_DOUT_PIN, pd_sck_pin=LOADCELL_SCK_PIN)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(2280)  
hx.reset()
hx.tare()  

def move_servo(servo, angle):
    """Function to move servo to a specified angle."""
    duty_cycle = angle / 18 + 2  
    servo.ChangeDutyCycle(duty_cycle)  
    time.sleep(0.5)  

try:
    print("Start weighing...")
    while True:
        
        weight = hx.get_weight(10)
        weight = abs(weight)  
        print(f"Weight: {weight:.2f} g")

       
        if weight > 150:
            move_servo(servoB, 90)  
            time.sleep(3)  
            move_servo(servoB, 0)   
        else:
            time.sleep(0.5) 

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    
    servoB.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete")