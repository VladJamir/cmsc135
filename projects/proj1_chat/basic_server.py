import socket
import sys

class BasicServer(object):

    def __init__(self, port):
        self.port = int(port)
        self.socket = socket.socket()
        self.socket.bind(('localhost', self.port))
        self.socket.listen(5)

    def receive(self):
        while True:
            client, client_addr = self.socket.accept()
            message = self.socket.recv(1024)
            print message
            client.close()

args = sys.argv
if len(args) != 2:
    print 'Please supply port number'
    sys.exit()

server = BasicServer(args[1])
server.receive()