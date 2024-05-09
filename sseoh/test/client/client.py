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
    def __init__(self,server_host, server_port):
        print("클라이언트 연결됨")
        # 서버에 접속
        self.sock = socket.create_connection((server_host, server_port))
        print("서버에 연결되었습니다.")
        
        # 메시지 수신을 위한 스레드 시작
        # 스레드 실행 상태를 확인하는 플래그
        self.receive_thread_running = False
        self.previous_beacon_name = None
        self.buffer = ""

        self.current_beacon_info = None  # 현재 비콘 정보를 저장할 변수 추가

    # init과 send_beacon 다시보기. 기존 send_beacon 안에 create_connection이 있었는데
    # send_beacon은 while문 내부에 있었음.

    # 비콘 이름, rssi는 비콘함수 추가 후 바꾸기
     # send_beacon 메소드 수정
    def update_beacon_info(self, beacon_name, rssi):
        self.current_beacon_info = (beacon_name, rssi)  # 비콘 정보 업데이트

    def send_beacon(self):
        print("send_beacon함수")
        if self.receive_thread_running:
            self.receive_thread_running = False
            self.receive_thread.join()

        self.receive_thread_running = True
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        print("receive_thread 스레드 시작됨")

        try:
            print("receive_beacon")
            while True:
                if self.current_beacon_info:
                    beacon_name, rssi = self.current_beacon_info  # 업데이트된 비콘 정보 사용
                    print("비콘정보전송")
                    data = f"{beacon_name},{rssi}"
                    self.sock.sendall(data.encode('utf-8'))
                time.sleep(3)

        except KeyboardInterrupt:
            print('프로그램이 사용자에 의해 중단되었습니다.')
        except Exception as e:
            print('Error:', e)


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

                        #os.remove(AUDIO) #생성된 파일 제거 # 다중 접속할때 permisson denined.해결용
                        self.previous_beacon_name = current_beacon_name

        except Exception as e:
            print(f"receive meessege 중 오류 발생: {e}")

        except KeyboardInterrupt:
            print("stop receive messages")
        # 수신 중 오류 발생->소켓 닫음...->
        



    #xml파일 생성. 현재 위치에 대한 x,y좌표 값 ->POI
    #client가 버튼 누르면 음성 녹음 -> button
    # 새로 추가한 soundout 실행 확인 후, receive 이후 tts 출력까지 후 계속 비콘 정보만 전송되는지 확인!

    #->녹음된 음성 SST API(음성을 텍스트로 바꿈)후, POI API&대중교통 API()
    #->버스 text를 client로 전송
    #->받은 text를 TTS API 사용. 실행
    
