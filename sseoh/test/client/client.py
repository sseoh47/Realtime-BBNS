import socket
import threading
import time
from tts_api import*
import playsound
from beacon import*
import os

class Client:
    def __init__(self,server_host, server_port,):
        print("클라이언트 연결됨")
         # 서버에 접속
        self.sock = socket.create_connection((server_host, server_port))
        print("서버에 연결되었습니다.")

        # 메시지 수신을 위한 스레드 시작
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
    # init과 send_beacon 다시보기. 기존 send_beacon 안에 create_connection이 있었는데
    # send_beacon은 while문 내부에 있었음.

    # 비콘 이름, rssi는 비콘함수 추가 후 바꾸기
    def send_beacon(self, server_host, server_port, beacon_name, rssi):
        print("send_beacon함수")
        try:
           
            while True:
                # 비콘 이름과 RSSI 값을 문자열로 결합하여 서버에 전송
                print("비콘정보전송")
                data = f"{beacon_name},{rssi}"
                self.sock.sendall(data.encode('utf-8'))
                time.sleep(1)

        except KeyboardInterrupt:
            print('프로그램이 사용자에 의해 중단되었습니다.')
        except Exception as e:
            print('Error:', e)
        # finally:
        #     # 소켓 닫기
        #     if self.sock:
        #         self.sock.close()
        #     print("클라이언트 종료")

    def receive_messages(self):
        try:
            previous_beacon_name = None
            buffer = ""
            while True:
                response = self.sock.recv(1024)
                if not response:
                    break
                buffer += response.decode('utf-8')
            
                # 버퍼에서 메시지를 줄바꿈 문자 기준으로 분리하여 처리
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    current_beacon_name = message.strip()

                    if current_beacon_name != previous_beacon_name:
                        text_to_speech(current_beacon_name)
                        # pip install playsound==1.2.2
                        playsound.playsound(AUDIO)
                        os.remove(AUDIO) #생성된 파일 제거 # 다중 접속할때 permisson denined.해결용
                        previous_beacon_name = current_beacon_name

        except Exception as e:
            print(f"메시지 수신 중 오류 발생: {e}")
        # 수신 중 오류 발생->소켓 닫음...->
        



    #xml파일 생성. 현재 위치에 대한 x,y좌표 값
    #client가 버튼 누르면 음성 녹음
    #->녹음된 음성 SST API(음성을 텍스트로 바꿈)후, POI API&대중교통 API()
    #->버스 text를 client로 전송
    #->받은 text를 TTS API 사용. 실행
    
