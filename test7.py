import RPi.GPIO as GPIO
import time
import subprocess

#setup always setwarnings to false
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER = 20
GPIO_ECHO = 21
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#Measurwe sa distance
def measure_distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    pulse_start = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start

    return pulse_duration

#play sound for ranges, only change the directory if needed
def play_sound(range_value):
    dist = range_value
    #subprocess.run(['mpg321', '-g', str(100), '/home/rpi/Desktop/HColocation/range_mp4/measure/50cm.mp3'])
    
    if dist <= 30:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/30cm.mp3"])
    elif dist <= 50:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/50cm.mp3"])
    elif dist <= 100:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/100cm.mp3"])
    elif dist <= 200:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/200cm.mp3"])
    elif dist <= 300:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/300cm.mp3"])
    elif dist <= 400:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/400cm.mp3"])

# Main loop
while True:
    pulse_duration = measure_distance()
    range_value = int(pulse_duration * 34300 / 2)

    volume = int((400 - range_value) / 4.5)-10 #formula pang convert sa distance ranges into certain volume range

    print("Range: {} cm, Volume: {}%".format(range_value, volume))#ang volume para rani tung last test pero di na magamit :D (or di jud ba kaha?)

    play_sound(range_value)

    time.sleep(0.1)
