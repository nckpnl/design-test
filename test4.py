import RPi.GPIO as GPIO
import time
import subprocess

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Function to measure distance using ultrasonic sensor
def measure_distance():
    # Send 10us pulse to trigger pin
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Record start time when pulse is sent
    pulse_start = time.time()

    # Record end time when pulse is received
    while GPIO.input(GPIO_ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        pulse_end = time.time()

    # Calculate time difference
    pulse_duration = pulse_end - pulse_start

    return pulse_duration

# Function to play sound with specified volume
def play_sound_C(volume):
    if volume > 70:
        subprocess.run(['mpg321', '-g', str(volume), '/home/admin/Desktop/HColocation/beep-C/3beep.mp3'])
    elif volume > 45:
        subprocess.run(['mpg321', '-g', str(volume), '/home/admin/Desktop/HColocation/beep-C/2beep.mp3'])
    else:
        subprocess.run(['mpg321', '-g', str(volume), '/home/admin/Desktop/HColocation/beep-C/1beep.mp3'])


# Main loop
while True:
    pulse_duration = measure_distance()
    range_value = int(pulse_duration * 34300 / 2)

    volume = int((400 - range_value) / 4.5)-10

    print("Range: {} cm, Volume: {}%".format(range_value, volume))

    play_sound_C(volume)

    # Wait 0.1 seconds before taking another measurement
    time.sleep(0.1)
