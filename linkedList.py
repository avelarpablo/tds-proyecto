"""
    Universidad de El Salvador

    Authors: 
    - Avelar Melgar, José Pablo		    –	AM16015
    - Campos Martínez, Abraham Isaac 	– 	CM17045
    - Lizama Escobar, Oscar Omar	    –	LE17004
    - Paredes Pastrán, Carlos Enrique	–	PP17012
    - Quinteros Lemus, Diego Enrique	–	QL17001

    Activity: Application project
    Subject: Técnicas de Simulación (TDS115)
    Professor: Lic. Guillermo Mejía
    Date: 06/11/2021
"""

class Node:
    def __init__(self, type = None, clock = None, next = None):
        self.type = type
        self.clock = clock
        self.next = next

    def __str__(self):
        return f"""Clock: {self.clock}
            typeCode": {self.type["typeCode"]},
            serverType": {self.type["serverType"]},
            index": {self.type["index"]}
        """

class LinkedList:
    def __init__(self):
        self.head = None

    def insertNode(self, type, clock):
        # Case 1: head is NULL
        if self.head == None:
            self.head = Node(type, clock, None)
        # Case 2: head.clock > newNode.clock
        elif self.head.clock > clock:
            self.head = Node(type, clock, self.head)
        # Case 3: insertion between head and last node of the list
        else:
            curr = self.head
            prev = None
            while curr and curr.clock <= clock:
                prev = curr
                curr = curr.next
            prev.next = Node(type, clock, curr)
    
    def removeFirstNode(self):
        head = self.head

        if self.head is not None:
            self.head = head.next

        head.next = None

        return head

    def deleteNode(self, type):
        curr = self.head
        prev = None
        while curr and curr.type != type:
            prev = curr
            curr = curr.next
        if prev is None:
            self.head = curr.next
        elif curr:
            prev.next = curr.next
            curr.next = None