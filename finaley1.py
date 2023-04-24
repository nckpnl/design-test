import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trig = 9
echo = 11
trig2 = 20
echo2 = 21
trig3 = 12
echo3 = 16
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig2, GPIO.OUT)
GPIO.setup(echo2, GPIO.IN)
GPIO.setup(trig3, GPIO.OUT)
GPIO.setup(echo3, GPIO.IN)

GPIO.output(trig, False)
GPIO.output(trig2, False)
GPIO.output(trig3, False)

def measure_distance():
    print("measuring")
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    pulse_start = time.time()
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    return pulse_duration

def measure_distance2():
    print("measuring")
    GPIO.output(trig2, True)
    time.sleep(0.00001)
    GPIO.output(trig2, False)
    pulse_start = time.time()
    while GPIO.input(echo2) == 0:
        pulse_start = time.time()
    while GPIO.input(echo2) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    return pulse_duration
    
def measure_distance3():
    print("measuring")
    GPIO.output(trig3, True)
    time.sleep(0.00001)
    GPIO.output(trig3, False)
    pulse_start = time.time()
    while GPIO.input(echo3) == 0:
        pulse_start = time.time()
    while GPIO.input(echo3) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    return pulse_duration

def play_sound_C(volume):
    if volume > 70:
        subprocess.Popen(['mpg321', '-g', str(volume+250), '/home/rpi/Desktop/HColocation/beep-R/3beep-R.mp3'])
    elif volume > 45:
        subprocess.Popen(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-R/2beep-R.mp3'])
    else:
        subprocess.Popen(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-R/1beep-R.mp3'])
        
def play_sound_R(volume):
    if volume > 70:
        subprocess.Popen(['mpg321', '-g', str(volume+250), '/home/rpi/Desktop/HColocation/beep-C/3beep.mp3'])
    elif volume > 45:
        subprocess.Popen(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-C/2beep.mp3'])
    else:
        subprocess.Popen(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-C/1beep.mp3'])

def play_sound_L(volume):
    if volume > 70:
        subprocess.Popen(['mpg321', '-g', str(volume+250), '/home/rpi/Desktop/HColocation/beep-L/3beep-L.mp3'])
    elif volume > 45:
        subprocess.Popen(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-L/2beep-L.mp3'])
    else:
        subprocess.Popen(['mpg321', '-g', str(volume), '/home/rpi/Desktop/HColocation/beep-L/1beep-L.mp3'])


def dodaloop():
    pulse_duration = measure_distance()
    range_value = int(pulse_duration * 34300 / 2)
    volume = int(((400 - range_value) / 4.5)-10)
    print("Range: {} cm, Volume: {}%".format(range_value, volume))
    play_sound_C(volume)
    time.sleep(0.001)
    
    pulse_duration = measure_distance2()
    range_value = int(pulse_duration * 34300 / 2)
    volume = int(((400 - range_value) / 4.5)-10)
    print("Range: {} cm, Volume: {}%".format(range_value, volume))
    play_sound_R(volume)
    time.sleep(0.001)
    
    pulse_duration = measure_distance3()
    range_value = int(pulse_duration * 34300 / 2)
    volume = int(((400 - range_value) / 4.5)-10)
    print("Range: {} cm, Volume: {}%".format(range_value, volume))
    play_sound_L(volume)
    time.sleep(0.001)
    

while True:
    dodaloop();
    time.sleep(1)
