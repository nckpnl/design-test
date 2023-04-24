import RPi.GPIO as GPIO
import time
import subprocess

# Set up GPIO pins for Center, Left and Right sensors
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER_C = 23
GPIO_ECHO_C = 24
GPIO_TRIGGER_L = 17
GPIO_ECHO_L = 27
GPIO_TRIGGER_R = 5
GPIO_ECHO_R = 6
GPIO.setup(GPIO_TRIGGER_C, GPIO.OUT)
GPIO.setup(GPIO_ECHO_C, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_L, GPIO.OUT)
GPIO.setup(GPIO_ECHO_L, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_R, GPIO.OUT)
GPIO.setup(GPIO_ECHO_R, GPIO.IN)

# Function to measure distance using ultrasonic sensor
def measure_distance(trigger_pin, echo_pin):
    # Send 10us pulse to trigger pin
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)

    # Record start time when pulse is sent
    pulse_start = time.time()

    # Record end time when pulse is received
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
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

def play_sound_L(volume):
    if volume > 70:
        subprocess.run(['mpg321', '-g', str(volume), '/home/admin/Desktop/HColocation/beep-L/3beep-L.mp3'])
    elif volume > 45:
        subprocess.run(['mpg321', '-g', str(volume), '/home/admin/Desktop/HColocation/beep-L/2beep-L.mp3'])
    else:
        subprocess.run(['mpg321', '-g', str(volume), '/home/admin/Desktop/HColocation/beep-L/1beep-L.mp3'])

def play_sound_R(volume):
    if volume > 70:
        subprocess.run(['mpg321', '-g', str(volume), '/home/admin/Desktop/HColocation/beep-R/3beep-R.mp3'])
    elif volume > 45:
        subprocess.run(['mpg321', '-g', str(volume), '/home/admin/Desktop/HColocation/beep-R/2beep-R.mp3'])
    else:
        subprocess.run(['mpg321', '-g', str(volume), '/home/admin/Desktop/HColocation/beep-R/1beep-R.mp3'])
        
# Main loop
while True:
    pulse_duration_center = measure_distance(GPIO_TRIGGER_C, GPIO_ECHO_C)
    pulse_duration_left = measure_distance(GPIO_TRIGGER_L, GPIO_ECHO_L)
    pulse_duration_right = measure_distance(GPIO_TRIGGER_R, GPIO_ECHO_R)

    range_value_center = int(pulse_duration_center * 34300 / 2)
    range_value_left = int(pulse_duration_left * 34300 / 2)
    range_value_right = int(pulse_duration_right * 34300 / 2)

    volume_center = int((400 - range_value_center) / 4.5) - 10
    volume_left = int((400 - range_value_left) / 4.5) - 10
    volume_right = int((400 - range_value_right) / 4.5) - 10

    print("Center Range: {} cm, Volume: {}%".format(range_value_center, volume_center))
    print("Left Range: {} cm, Volume: {}%".format(range_value_left, volume_left))
    print("Right Range: {} cm, Volume: {}%".format(range_value_right, volume_right))

    # Play sounds
    sound_threads = []
    sound_threads.append(Thread(target=play_sound_C, args=(volume_center,)))
    sound_threads.append(Thread(target=play_sound_L, args=(volume_left,)))
    sound_threads.append(Thread(target=play_sound_R, args=(volume_right,)))
    for thread in sound_threads:
        thread.start()
    for thread in sound_threads:
        thread.join()

    # Wait 0.1 seconds before taking another measurement
    time.sleep(0.1)
