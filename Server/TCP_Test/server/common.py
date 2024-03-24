import json
import socket
from constant import BUFFER_SIZE

"""
socket.socket의 accept()를 통해 반환된 데이터를 보관하기 위한 클래스
소켓을 통한 송신 수신 기능을 포함한다.
"""
class Socket:
    def __init__(self, socket, addr):
        self.__socket= socket
        self.__addr = addr
    
    #주소 데이터 반환
    def get_addr(self):
        return self.__addr

    # 데이터 받기
    # data = <데이터타입>:<본문>
    # head = 데이터 타입  ('FILE', "STRING")
    # body = 본문
    def receive_data(self, buffuer_size = BUFFER_SIZE):
        data:bytes = self.__socket.recv(buffuer_size)
        decoded_data = data.decode()
        head, body= self.__recognize_protocol(data = decoded_data)
        print(f"{head}Received Data : {body}")
        return head, body
    
    def receive_file(self, buffuer_size = BUFFER_SIZE):
        data:bytes = self.__socket.recv(buffuer_size)
        #decoded_data = data.decode()
        return data 


    # String 보내기
    def send_data(self, data:str):
        encoded_data = data.encode()
        self.__socket.sendall(encoded_data)
        return 
    
    def send_result(self, data):
        serialized_data = json.dumps(data).encode()
        self.__socket.sendall(serialized_data)
        return

    # 파일전송
    def send_file(self, data:bytes):
        self.__socket.sendall(data)
        return
    
    # 프로토콜 분석
    def __recognize_protocol(self, data:str):
        data_parts = data.split(":")
        return data_parts[0], data_parts[1:]
    
    
    def close_socket(self):
        self.__socket.close()
        return


"""
Client를 정의하기 위한 클래스  (위의 Socket 클래스를 상속)
_id : 클라이언트 번호
_data : 필수 데이터 (head, bid, target)
_flag : 데이터가 처리 되었다는 것을 알려주기 위한 세마포어
"""
class Client(Socket):
    def __init__(self, id, client_socket:socket.socket, addr):
        self._id:int = id
        self._data = {'head':'default', 'bid':'-1', 'target':'default', "result":"None"}
        self._flag = "Default"
        self._thread = None
        super().__init__(client_socket, addr)
        
    def set_thread(self, thread):
        self._thread = thread
        return

    def get_client_id(self):
        return self._id

    def get_data(self):
        return self._data
    
    def set_head(self, head):
        self._data['head'] = head
        return 
    
    #BindTarget으로 수정하기
    def set_BindTarget(self, bid:str, target:str):
        self._data['bid'] = bid
        self._data['target'] = target
        return
    
    def set_result(self, result):
        self._data['result'] = result
        return

    def get_flag(self):
        return self._flag

    def dataCompletelyCame(self):
        self._flag = "Set"
        return
    
    def dataReady2Send(self):
        self._flag = "Ready"
        return

    def dataReset(self):
        self._flag = "Default"
        return
