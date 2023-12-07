from controller import Master_Controller
from linkedList import Linked_List, Node
from unit import TCP_Server
from common import Client
from constant import HOST, PORT
from threading import Thread


class APP_Server():
    def __init__(self, controller):
        self.app = TCP_Server(host = HOST, port = PORT)
        self.controller:Master_Controller = controller
        self.client_list = Linked_List()
        
    def run_system(self):
        thread = Thread(target=self.route)
        thread.start()
        self.app.waiting_client(self.client_list)
        
    def route(self):
        threads = []
        now_count = 0
        while True:
            #print("size", self.client_list.getSize())
            #print("count",now_count)
            
            if self.client_list.getSize() > now_count:
                now_count = now_count + 1
                thread = Thread(target = self.data_process, args=(self.client_list.getRear(), ))
                threads.append(thread)
                thread.start()
                
            elif self.client_list.getSize() < now_count:
                now_count = now_count - 1
            
            else:
                continue
        
    def data_process(self, client_node:Node):
        while True:
            client = None
            try:
                while True:
                    client:Client = client_node.getData()
                    if client.get_flag() == "Set":
                        break
                
                if client.get_data()['head'] == "END":
                    break
                
                data = client.get_data()
                print("data", data)
                if data['head'] == "FILE":
                    result = self.controller.makeWAV2Text(client.get_client_id())
                    
                    
                elif data['head'] == "STRING":
                    bid = data['bid']
                    target = data['target']
                    result = self.controller.getShortestPath(bid=bid, target=target)
                    
                if client.get_data()['head'] == "END":
                    break
                
                client.set_result(result=result)
                client.dataReady2Send()
            except:
                print("Client Deleted")
                break
        return
            
            
        
        
        

