import sys
import socket
import select
import utils

class Client(object):

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = int(port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(2)

    def chat(self):
        try:
            self.client.connect((self.host, self.port))
        except:
            print utils.CLIENT_CANNOT_CONNECT.format(self.host, self.port)
            sys.exit()
        
        sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX); sys.stdout.flush()

        while True:
            socket_list = [sys.stdin, self.client]
            readable, writable, exception = select.select(socket_list, [], [])
            for socket in readable:
                if socket is self.client:
                    data = self.receive_message(socket)
                    if not data:
                        print utils.CLIENT_SERVER_DISCONNECTED.format(self.host, self.port)
                        sys.exit()
                    else:
                        sys.stdout.write(utils.CLIENT_WIPE_ME)
                        sys.stdout.write('\r' + data.rstrip())
                        sys.stdout.write('\n' + utils.CLIENT_MESSAGE_PREFIX); sys.stdout.flush()
                else:
                    msg = sys.stdin.readline()
                    msg = '[' + self.name + '] ' + msg
                    self.send(self.client, msg)
                    sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX); sys.stdout.flush()

    def receive_message(self, socket):
        chunks = []
        bytes_recd = 0
        while bytes_recd < utils.MESSAGE_LENGTH:
            chunk = socket.recv(min(utils.MESSAGE_LENGTH - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def send(self, socket, msg):
        totalsent = 0
        while totalsent < utils.MESSAGE_LENGTH:
            sent = socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
                         
args = sys.argv
if len(args) != 4:
    print 'Please supply name, host, and port number'
    sys.exit()

client = Client(args[1], args[2], args[3])
client.chat()