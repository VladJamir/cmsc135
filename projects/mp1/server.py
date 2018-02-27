import sys
import socket

class Channel(object):
    def __init__(self, name):
        self.name = name
        self.members = []
    def add(self, socket):
        self.members.append(socket)
    def delete(self, socket)
        self.members.remove(socket)
    

class Server(object):
    def __init__(self, port):
        self.port = int(port)
        self.host = 'localhost'
        self.server = socket.socket()
        self.server.bind((self.address, self.port))
        self.server.listen(5)
        self.socket_list = [self.server]
        self.channels = []
        self.channel_names = []

    def run(self):
        while True:
            readable, writable, exception = select.select(self.socket_list, [], [], 0)
            for s in readable:
                # for a new connection
                if s is server:
                    sfd, addr = server.accept()
                    self.socket_list.append(sockfd)
                # a message from client, not a new client
                else:
                    try:
                        data = s.recv(1024)
                        if data:
                            if data[:5] == '/join':
                            elif data[:7] == '/create':
                                if (data[7:] in self.channel_names):
                                    #broadcast to requesting socket that channel already exists
                                else:
                                    channel = Channel(data[7:])
                                    channel.add(s)
                            elif data[:5] == '/list':
                                #broadcast self.channel_names to requesting socket
                            elif data[:1] == '/':
                                #brodcast error message SERVER_INVALID_CONTROL_MESSAGE
                            else:
                                #broadcast message to channel
                            
                        else: 
                            #broadcast to channels if disconnected
                            if sock in self.socket_list:
                                self.socket_list.remove(s)
                    except:
                        #broadcast client is disconnected
                        continue
        server.close()

    def send_list(self, socket):
        for channel in self.channel_names:
            try:
                socket.send(channel + '\n')
            except:
                socket.close()
                for chan in channels:
                    if socket in chan.members
                        chan.delete(socket)
                self.socket_list.remove(socket)

args = sys.argv
if len(args) != 2:
    print 'Please supply port number'
    sys.exit()

server = Server(args[1])
