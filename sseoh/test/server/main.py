import socket
from linked_list import*
from send import*
from constant import HOST, PORT
import sys

class Main():
    def __init__(self, host, port):
        self.clients = ClientLinkedList()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.client_node = ClientNode(host, port) 

    def start_server(self):
        print("Server is listening for incoming connections...")
        self.client_node.accept_connections(self.server_socket, self.clients)

if __name__ == "__main__":
    main = Main(HOST, PORT)
    main.start_server()
