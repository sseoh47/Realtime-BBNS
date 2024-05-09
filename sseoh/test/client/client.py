import socket
import threading
import time
from tts_api import*
from beacon import*
from pydub import AudioSegment
from pydub.playback import play

from constant import AUDIO
from playsound import playsound


class Client:
    def __init__(self, server_host, server_port):
        print("클라이언트 연결됨")
        self.sock = socket.create_connection((server_host, server_port))
        print("서버에 연결되었습니다.")
        self.receive_thread_running = False
        self.previous_beacon_name = None
        self.buffer = ""
        # receive_messages 스레드 시작
        self.start_receive_thread()

    def start_receive_thread(self):
        if not self.receive_thread_running:
            self.receive_thread_running = True
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
            print("receive_thread 스레드 시작됨")

    def send_beacon(self, beacon_name, rssi):
        print("send_beacon함수")
        # 비콘 이름과 RSSI 값을 문자열로 결합하여 서버에 전송
        data = f"{beacon_name},{rssi}"
        self.sock.sendall(data.encode('utf-8'))
        time.sleep(1.0)


    def receive_messages(self):
        try:
            print("receive_messages 함수 시작")
            
            while True:
                response = self.sock.recv(1024)
                if not response:
                    break
                self.buffer += response.decode('utf-8')
            
                # 버퍼에서 메시지를 줄바꿈 문자 기준으로 분리하여 처리
                while "\n" in self.buffer:
                    message, self.buffer = self.buffer.split("\n", 1)
                    current_beacon_name = message.strip()

                    if current_beacon_name != self.previous_beacon_name:
                        #print("tts 시작")
                        print("current_beacon_name:",current_beacon_name)
                        text_to_speech(current_beacon_name)
                        # pip install playsound==1.2.2
                        playsound(AUDIO)
                        #os.remove(AUDIO) #생성된 파일 제거 # 다중 접속할때 permisson denined.해결용
                        self.previous_beacon_name = current_beacon_name

        except Exception as e:
            print(f"receive meessege 중 오류 발생: {e}")

        except KeyboardInterrupt:
            print("stop receive messages")
   
