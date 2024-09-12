import time
import Jetson.GPIO as GPIO
from hx711 import HX711

# Pin Definitions
LOADCELL_DOUT_PIN = 16 
LOADCELL_SCK_PIN = 27   
SERVO_PIN_B = 32        

# Setup GPIO for Jetson Nano
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN_B, GPIO.OUT)

# Setup PWM for Gate B (50Hz for typical servo motors)
servoB = GPIO.PWM(SERVO_PIN_B, 50)
servoB.start(0)  # Start with the servo at 0 degrees (closed position)

# Setup HX711 for load cell
hx = HX711(dout_pin=LOADCELL_DOUT_PIN, pd_sck_pin=LOADCELL_SCK_PIN)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(2280)  # Adjust calibration factor here
hx.reset()
hx.tare()

previous_weight = 0.0  # Variable to store previous weight

# Helper function to move servo
def move_servo(servo, angle):
    duty_cycle = angle / 18 + 2 
    servo.ChangeDutyCycle(duty_cycle)  

try:
    print("Start weighing...")
    while True:
        # Read weight from the load cell (average of 10 readings)
        weight = hx.get_weight(10)
        weight = abs(weight)  # Ensure weight is positive
        print(f"Weight: {weight:.2f} g")

        # If the weight exceeds 150 grams, open Gate B
        if weight > 150:
            # Open Gate B (0 degrees to the right)
            move_servo(servoB, 0)
            time.sleep(1)  # Wait for 1 second

            # Close Gate B (90 degrees to the closed position)
            move_servo(servoB, 90)
            time.sleep(1)  # Wait for 1 second

        
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    # Clean up resources
    servoB.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete")
