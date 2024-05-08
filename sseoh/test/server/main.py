import socket
from linked_list import*
from send import*
from constant import*
import sys
import json
import requests
import pygame
import os
from constant import HOST, PORT, BUFFER_SIZE


class TCP_Server():
    def __init__(self, host, port):
        self.clients = ClientLinkedList()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.client_node = ClientNode(host, port) 

    def start_server(self):
        print("Server is listening for incoming connections...")
        self.client_node.accept_connections(self.server_socket, self.clients)




    def close_socket(self):
        protocol = 'END:'
        self.client_sock.sendall(protocol.encode())
        self.client_sock.close()
    


if __name__ == "__main__":
    main = TCP_Server(HOST, PORT)
    main.start_server()
