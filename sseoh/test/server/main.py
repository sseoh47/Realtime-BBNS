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


    def send_string(self, bid = '-1', target = "Default"):
        protocol = f'STRING:{bid}:{target}'
        self.client_sock.sendall(protocol.encode())
        
        result = self.client_sock.recv(BUFFER_SIZE)
        decoded_data = result.decode()
        
        result = self.client_sock.recv(BUFFER_SIZE)
        decoded_data = json.loads(result.decode()) 
        
        return decoded_data
        
    def send_file(self, file_path):
        
        with open(file_path, 'rb') as file:
            file_size = os.path.getsize(file_path)
            protocol = f'FILE:{file_size}'
            self.client_sock.sendall(protocol.encode())
            receive = self.client_sock.recv(BUFFER_SIZE)
            
            data = file.read(BUFFER_SIZE)
            while data:
                self.client_sock.send(data)
                data = file.read(BUFFER_SIZE)
        
        result = self.client_sock.recv(BUFFER_SIZE)
        
        decoded_data = json.loads(result.decode())
        
        return decoded_data

    def close_socket(self):
        protocol = 'END:'
        self.client_sock.sendall(protocol.encode())
        self.client_sock.close()
    
# 버스 파인더
class Bus_Finder():
    def __init__(self):
        self.tcp_connect = TCP_Server()


    # 경로까지 버스 찾기
    def run_bus_finder(self, bid = "1"): 
        # 목표위치 검색
        target = self.__get_target()
        if target == "Default":
            try:
                self.tcp_connect.close_socket()
            except:
                print("may be connection close")
            finally:
                return
        
        # 경로 까지 버스 검색
        self.__search_path(bid=bid, target=target)
        try:
            self.tcp_connect.close_socket()
        except:
            print("may be connection close")
        finally:
            return
        

    # 도착지 찾기
    def __get_target(self):
        file_path = './sample.wav'

        response = self.tcp_connect.send_file(file_path)


        print(response)


        target:str = response['place']
        return target

    # 경로 찾기
    def __search_path(self, bid, target):
        response = self.tcp_connect.send_string(bid=bid, target=target)

        print(response)


        return

if __name__ == "__main__":
    main = TCP_Server(HOST, PORT)
    main.start_server()
