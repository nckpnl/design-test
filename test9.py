import RPi.GPIO as GPIO
import time
import subprocess
import cv2

# Setup always set warnings to false
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER = 20
GPIO_ECHO = 21
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Haar cascades for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Measure the distance
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

# Play sound for ranges, only change the directory if needed
def play_sound(range_value, face_detected):
    dist = range_value
    
    if dist <= 30:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/30cm.mp3"])
    elif dist <= 50:
        if face_detected:
            print("Face detected. No sound will be played.")
        else:
            print("No Face detected! Playing 50cm sound.")
            subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/50cm.mp3"])
    elif dist <= 100:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/dictation/object 100cm.mp3"])
        #subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/dictation/100cm.mp3"])
    elif dist <= 200:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/200cm.mp3"])
    elif dist <= 300:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/300cm.mp3"])
    elif dist <= 400:
        subprocess.run(["mpg321", "/home/rpi/Desktop/HColocation/range_mp4/measure/400cm.mp3"])

# Main loop
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #Determine if a face was detected
    if len(faces) > 0:
        face_detected = True
        print("Face detected!")
    else:
        face_detected = False
        print("No face detected.")

    pulse_duration = measure_distance()
    range_value = int(pulse_duration * 34300 / 2)
    volume = int((400 - range_value) / 4.5) - 10


    print("Range: {} cm, Volume: {}%".format(range_value, volume))
    play_sound(range_value, face_detected)

    time.sleep(0.1)

