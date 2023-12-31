import pyaudio
import wave
import threading
import RPi.GPIO as GPIO
import pygame
from client import Bus_Finder

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = r'sample.wav'
BUTTON_PIN = 2

frames = []
recording = False

def Start_Recording():
    global frames
    frames = []

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print('음성녹음 시작')

    while recording:  # recording이 True인 동안 계속 녹음
        data = stream.read(CHUNK)
        frames.append(data)

    print('음성녹음 완료')

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)
        if button_state == False and not recording:  # 버튼이 눌렸고 녹음 중이 아니면 녹음 시작
            recording = True
            thread = threading.Thread(target=Start_Recording)
            thread.start()
        elif button_state == True and recording:  # 버튼이 떼어지고 녹음 중이면 녹음 종료
            recording = False
            thread.join()  # 녹음 스레드가 종료될 때까지 기다립니다.
            break

except KeyboardInterrupt:
    GPIO.cleanup()  # 프로그램 종료 시 GPIO 설정 초기화

bus_finder = Bus_Finder()
bus_finder.run_bus_finder()

# pygame.mixer.init()
# pygame.mixer.music.load(WAVE_OUTPUT_FILENAME)
# pygame.mixer.music.play()

# while pygame.mixer.music.get_busy() == True:
#     continue


# import pyaudio
# import wave
# # import tkinter as tk
# import threading
# import RPi.GPIO as GPIO
# import pygame

# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# # WAVE_OUTPUT_FILENAME = r'C:\Users\y2h75\Desktop\record_output.wav'
# WAVE_OUTPUT_FILENAME = r'record_output.wav'
# BUTTON_PIN = 2

# frames = []
# recording = False

# def Start_Recording():
#     global frames
#     frames = []

#     p = pyaudio.PyAudio()

#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)

#     print('음성녹음 시작')

#     while recording:  # recording이 True인 동안 계속 녹음
#         data = stream.read(CHUNK)
#         frames.append(data)

#     print('음성녹음 완료')

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# try:
#     while True:
#         button_state = GPIO.input(BUTTON_PIN)
#         if button_state == False and not recording:  # 버튼이 눌렸고 녹음 중이 아니면 녹음 시작
#             recording = True
#             thread = threading.Thread(target=Start_Recording)
#             thread.start()
#         elif button_state == True and recording:  # 버튼이 떼어지고 녹음 중이면 녹음 종료
#             recording = False
#             break
    
    
# except KeyboardInterrupt:
#     GPIO.cleanup()  # 프로그램 종료 시 GPIO 설정 초기화
    
# pygame.mixer.init()
# pygame.mixer.music.load("./record_output.wav")
# pygame.mixer.music.play()

# while pygame.mixer.music.get_busy() == True:
#     continue