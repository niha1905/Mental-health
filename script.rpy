import RPi.GPIO as GPIO
import time

trigger_pin = 17  
echo_pin = 18  
lid_motor_pin = 22 
red_light_pin = 23  
wet_bin_pin = 24 
dry_bin_pin = 25  
buzzer_pin = 26 

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.setup(lid_motor_pin, GPIO.OUT)
    GPIO.setup(red_light_pin, GPIO.OUT)
    GPIO.setup(wet_bin_pin, GPIO.IN)
    GPIO.setup(dry_bin_pin, GPIO.IN)
    GPIO.setup(buzzer_pin, GPIO.OUT)

def measure_distance():
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start_time = time.time()

    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = pulse_duration * 34300 / 2  
    return distance

def is_bin_full():
    return measure_distance() < 20 

def open_lid():
    GPIO.output(lid_motor_pin, GPIO.HIGH)
    time.sleep(2)  
    GPIO.output(lid_motor_pin, GPIO.LOW)

def activate_red_light():
    GPIO.output(red_light_pin, GPIO.HIGH)

def deactivate_red_light():
    GPIO.output(red_light_pin, GPIO.LOW)

def check_and_sort_waste():
    if GPIO.input(wet_bin_pin) == GPIO.HIGH:
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(1) 
        GPIO.output(buzzer_pin, GPIO.LOW)
    elif GPIO.input(dry_bin_pin) == GPIO.HIGH:
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(1) 
        GPIO.output(buzzer_pin, GPIO.LOW)

def loop():
    try:
        while True:
            if is_bin_full():
                activate_red_light()
                open_lid()
            else:
                deactivate_red_light()

            check_and_sort_waste()
            time.sleep(1) 

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program terminated by user.")

def main():
    setup_gpio()
    loop()

if __name__ == "__main__":
    main()
