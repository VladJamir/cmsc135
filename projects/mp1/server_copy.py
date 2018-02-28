import sys
import socket
import select
import utils
import re

class Channel(object):

    def __init__(self, name):
        self.name = name
        self.clients = []

class Server(object):
    
    def __init__(self, port):
        self.host = 'localhost'
        self.port = int(port)
        self.socket_list = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.socket_list.append(self.server)
        self.channel_name_list = []
        self.channel_list = []
        self.pattern = re.compile('\[(.+)\]\s(/join|/create|/list)?\s?(.*)')
    
    def chat(self):
        
        while True:
            readable, writable, exception = select.select(self.socket_list, [], [], 0)
            for socket in readable:
                if socket is self.server:
                    client, client_addr = self.server.accept()
                    self.socket_list.append(client)
                else:
                    try:
                        data = socket.recv(4096)
                        if data:
                            m = self.pattern.match(data.rstrip())
                            if m.group(2) == '/join':
                                if m.group(3) == '':
                                    self.send(socket, utils.SERVER_JOIN_REQUIRES_ARGUMENT)
                                elif m.group(3) not in self.channel_name_list:
                                    self.send(socket, utils.SERVER_NO_CHANNEL_EXISTS.format(m.group(3)))
                                else:
                                    #leave
                                    self.leave(socket, m.group(1))
                                    #join
                                    self.join(socket, m.group(3), m.group(1))
                            elif m.group(2) == '/create':
                                if m.group(3) == '':
                                    self.send(socket, utils.SERVER_CREATE_REQUIRES_ARGUMENT)
                                else:
                                    if m.group(3) in self.channel_name_list:
                                        self.send(socket, utils.SERVER_CHANNEL_EXISTS.format(m.group(3)))
                                    else:
                                        #create
                                        self.create(socket, m.group(3))
                            elif m.group(2) == '/list' and m.group(3) == '':
                                #show list
                                self.show_list_of_channels(socket)
                            elif m.group(2) == '' and m.group(3).startswith('/'):
                                #invalid
                                self.send(socket, utils.SERVER_INVALID_CONTROL_MESSAGE)
                            else:
                                print 'it goes here '
                                if not self.is_joined_in_channel(socket):
                                    print 'a'
                                    self.send(socket, utils.SERVER_CLIENT_NOT_IN_CHANNEL)
                                else:
                                    print 'b'
                                    self.broadcast_to_channel(socket, data)
                        else:
                            if socket in self.socket_list:
                                self.socket_list.remove(socket)
                    except Exception as e:
                        #self.send(self.server, socket, 'Client  offline')  
                        # send to channels that a socket left 
                        #print 'e on line {}'.format(sys.exc_info()[-1].tb_lineno)                        
                        print str(e)
                        continue
        self.server.close()

    def send(self, socket, message):
        try:
            print 'sending'
            socket.send(message)
        except:
            print 'otherwise'
            socket.close()
            if s in self.socket_list:
                self.socket_list.remove(s)

    def create(self, socket, new_channel_name):
        new_channel = Channel(new_channel_name)
        new_channel.clients.append(socket)
        self.channel_name_list.append(new_channel_name)
        self.channel_list.append(new_channel)

    def show_list_of_channels(self, socket):
        for channel_name in self.channel_name_list:
            self.send(socket, channel_name)
    
    def leave(self, socket, client_name):
        for channel in self.channel_list:
            if socket in channel.clients:
                for client in channel.clients:
                    if client != socket:
                        self.send(client, utils.SERVER_CLIENT_LEFT_CHANNEL.format(client_name))
                channel.clients.remove(socket)
                break

    def join(self, socket, channel_name, client_name):
        for channel in self.channel_list:
            if channel_name == channel.name:
                for client in channel.clients:
                    self.send(client, utils.SERVER_CLIENT_JOINED_CHANNEL.format(client_name))
                channel.clients.append(socket)
                break

    def is_joined_in_channel(self, socket):
        for channel in self.channel_list:
            if socket in channel.clients:
                return True
        else:
            return False
        
    def broadcast_to_channel(self, socket, message):
        for channel in self.channel_list:
            if socket in channel.clients:
                for client in channel.clients:
                    if client != socket:
                        self.send(client, message)
                break

args = sys.argv
if len(args) != 2:
    print 'Please supply port number'
    sys.exit()

server = Server(args[1])
server.chat()

                    