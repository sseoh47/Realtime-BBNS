import pyaudio
import wave
import tkinter as tk
import threading

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = r'C:\Users\y2h75\Desktop\record_output.wav'

frames = []
recording = False

def start_recording():
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

root = tk.Tk()
root.withdraw()  # tkinter 창 숨기기

def on_keypress(event):
    global recording
    if event.char == 'a':  # 'a' 키를 누르면 녹음 시작
        if not recording: # 녹음 중이 아닐 때만 녹음 시작
            recording = True
            thread = threading.Thread(target=start_recording)
            thread.start()

def on_keyrelease(event):
    global recording
    if event.char == 'a':  # 'a' 키를 떼면 녹음 종료
        recording = False

# root.bind('<KeyPress>', on_keypress)
# root.bind('<KeyRelease>', on_keyrelease)

button = tk.Button(root)
button.bind("<Button-1>", on_keypress)
button.bind("<ButtonRelease-1>", on_keyrelease)
button.pack()

root.mainloop()