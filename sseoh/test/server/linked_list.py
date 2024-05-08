from send import*

class ClientLinkedList:
    def __init__(self):
        self.head = None
  

    def add(self, new_node):
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def remove(self, client_socket):
        current = self.head
        previous = None
        while current:
            if current.client_socket == client_socket:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return
            previous = current
            current = current.next
