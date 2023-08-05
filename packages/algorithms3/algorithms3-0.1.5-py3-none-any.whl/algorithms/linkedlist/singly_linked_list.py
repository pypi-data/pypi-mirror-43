class Node:
    def __init__(self, x):
        self.val = x
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        result = ''
        if self.head == None:
            return ''
        current = self.head
        while current.next:
            result += str(current.val) + '->'
            current = current.next
        result += str(current.val)
        return result

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def push_front(self, x):
        newNode = Node(x)
        if self.head != None:
            newNode.next = self.head
    
        self.head = newNode

    def push_end(self, x):
        if self.head == None:
            self.head = Node(x)
            return 
        current = self.head
        while current.next:
            current = current.next
        current.next = Node(x)

