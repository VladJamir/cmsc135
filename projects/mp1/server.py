import sys
import socket
import re
import utils

class Channel(object):
    def __init__(self, name):
        self.name = name
        self.members = []
    
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
       pattern = re.compile('\[(.+)\]\s(/join|/create|/list)?\s?(.*)')
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
                            m = pattern.match(data)
                            if m.group(2) == '/join':
                                if m.group(3) == '':
                                    #send error message
                                else:
                                    #join
                            elif m.group(2) == '/create':
                                if m.group(3) == '':
                                    #send error message
                                else: 
                                    #create
                            elif m.group(2) == '/list' and m.group(2) == '':
                                #show list
                            elif m.group(3).startswith('/'):
                                #invalid pattern send SERVER_INVALID_CONTROL_MESSAGE = \
                            else:
                                #send message to channels
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
                        chan.members.remove(socket)
                self.socket_list.remove(socket)
    
    def leave(self, name, socket):
        for channel in self.channels:
            if socket in channel.members:
                for client in channel.members:
                    try:
                        client.send(utils.SERVER_CLIENT_LEFT_CHANNEL.format(name) + '\n')
                    except:
                        client.close
                        channel.members.remove(client)
                        self.socket_list.remove(client)

    def join(self, name, socket, channel):
        for client in channel.members:
            try:
                if client != socket:
                    client.send(utils.SERVER_CLIENT_JOINED_CHANNEL.format(name) + '\n')
            except:
                client.close()
                channel.members.remove(client)
                self.socket_list.remove(client)
        channel.members.add(socket)

    def create(self, name, socket):
        channel = Channel(name)
        self.channel_names.append(name)
        channel.members.append(socket)

    def send_error_message(self, socket, message):
        try:
            socket.send(message)
        except:
            socket.close()
            self.socket_list.remove(socket)
            for channel in self.channels:
                if socket in channel.members:
                    channel.members.remove(socket)

    def send_message(self, socket, message):
        for channel in self.channels:
            if socket in channel.members:
                for s in channel.members:
                    try:
                        if s != socket:
                            s.send(message)
                    except:
                        s.close()
                        self.socket_list.remove(s)
                        channel.members.remove(s)
                break
        else:
            self.send_error_message(socket, utils.SERVER_CLIENT_NOT_IN_CHANNEL)

args = sys.argv
if len(args) != 2:
    print 'Please supply port number'
    sys.exit()

server = Server(args[1])
