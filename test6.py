import RPi.GPIO as GPIO
import time
import subprocess

# Set up GPIO pins


GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER_C = 5
GPIO_ECHO_C = 6
GPIO.setup(GPIO_TRIGGER_C, GPIO.OUT)
GPIO.setup(GPIO_ECHO_C, GPIO.IN)

GPIO_TRIGGER_R = 9
GPIO_ECHO_R = 11
GPIO.setup(GPIO_TRIGGER_R, GPIO.OUT)
GPIO.setup(GPIO_ECHO_R, GPIO.IN)

# Function to measure distance using ultrasonic sensor
def measure_distance_C():
    # Send 10us pulse to trigger pin
    GPIO.output(GPIO_TRIGGER_C, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_C, False)

    # Record start time when pulse is sent
    pulse_start = time.time()

    # Record end time when pulse is received
    while GPIO.input(GPIO_ECHO_C) == 0:
        pulse_start = time.time()

    while GPIO.input(GPIO_ECHO_C) == 1:
        pulse_end = time.time()

    # Calculate time difference
    pulse_duration_C = pulse_end - pulse_start

    return pulse_duration_C
    
def measure_distance_R():
    # Send 10us pulse to trigger pin
    GPIO.output(GPIO_TRIGGER_R, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_R, False)

    # Record start time when pulse is sent
    pulse_start = time.time()

    # Record end time when pulse is received
    while GPIO.input(GPIO_ECHO_R) == 0:
        pulse_start = time.time()

    while GPIO.input(GPIO_ECHO_R) == 1:
        pulse_end = time.time()

    # Calculate time difference
    pulse_duration_R = pulse_end - pulse_start

    return pulse_duration_R

# Function to play sound with specified volume
def play_sound_C(volume):
    if volume > 70:
        subprocess.run(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-C/3beep.mp3'])
    elif volume > 45:
        subprocess.run(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-C/2beep.mp3'])
    else:
        subprocess.run(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-C/1beep.mp3'])

def play_sound_L(volume):
    if volume > 70:
        subprocess.run(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-L/3beep-L.mp3'])
    elif volume > 45:
        subprocess.run(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-L/2beep-L.mp3'])
    else:
        subprocess.run(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-L/1beep-L.mp3'])
        
def play_sound_R(volume):
    if volume > 70:
        subprocess.run(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-R/3beep-R.mp3'])
    elif volume > 45:
        subprocess.run(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-R/2beep-R.mp3'])
    else:
        subprocess.run(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-R/1beep-R.mp3'])

def loop_C():
     pulse_duration_C = measure_distance_C()
     range_value_C = int(pulse_duration_C * 34300 / 2)

     volume_C = int((400 - range_value_C) / 4.5)-10

     print("Range: {} cm, Volume: {}%".format(range_value_C, volume_C))

     play_sound_C(volume_C)

     # Wait 0.1 seconds before taking another measurement
     time.sleep(0.1)

def loop_R():
     pulse_duration_R = measure_distance_R()
     range_value_R = int(pulse_duration_R * 34300 / 2)

     volume_R = int((400 - range_value_R) / 4.5)-10

     print("Range: {} cm, Volume: {}%".format(range_value_R, volume_R))

     play_sound_R(volume_R)

     # Wait 0.1 seconds before taking another measurement
     time.sleep(0.1)
     
# Main loop
while True:
    loop_C();
