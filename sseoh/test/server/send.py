import socket
import threading
import time

class ClientNode:
    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address
        
        self.last_name = None
        self.last_name_time = 0
        self.name_to_send = None
        self.next = None  # 'next' 속성 추가


    def handle_client(self, client_node, clients):
        client_socket = client_node.client_socket
        address = client_node.address

        def receive_messages():
            try:
                while True:
                    data = client_socket.recv(1024).decode()
                    if data:
                        name, rssi = data.split(',')
                        print(f"Message from {address[1]}: Beacon Name = {name}, RSSI = {rssi}")
                        current_time = time.time()
        
                        client_node.last_name = name
                        client_node.last_name_time = current_time
                        client_node.name_to_send = name
                        time.sleep(1.5)
                    else:
                        break
            finally:
                clients.remove(client_socket)
                client_socket.close()
                print(f"Connection closed for {address}")

        def send_messages():
            try:
                while True:
                    if client_node.name_to_send:
                        # 메시지 끝에 구분자 '\n' 추가
                        message = f"{client_node.name_to_send}\n"
                        client_socket.sendall(message.encode())
                        client_node.name_to_send = None
                    time.sleep(1.5)  # 1초마다 메시지 전송
            except Exception as e:
                print(f"메시지 전송 중 오류 발생: {e}")


        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

        send_thread = threading.Thread(target=send_messages)
        send_thread.start()

        receive_thread.join()


    def accept_connections(self, server_socket, clients):
        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address} has been established.")

            new_node = ClientNode(client_socket, address)
            clients.add(new_node)

            thread = threading.Thread(target=self.handle_client, args=(new_node, clients))
            thread.start()