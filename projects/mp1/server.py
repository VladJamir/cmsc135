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
                        data = self.receive_msg(socket)
                        m = self.pattern.match(data.rstrip())
                        
                        if data:
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
                                        self.create(socket, m.group(3), m.group(1))
                            elif m.group(2) == '/list' and m.group(3) == '':
                                #show list
                                self.show_list_of_channels(socket)
                            elif m.group(2) == None and m.group(3).startswith('/'):
                                #invalid
                                self.send(socket, utils.SERVER_INVALID_CONTROL_MESSAGE.format(m.group(3)))
                            else:
                                print 'it goes here'
                                if not self.is_joined_in_channel(socket):
                                    print m.group(2), m.group(3)
                                    self.send(socket, utils.SERVER_CLIENT_NOT_IN_CHANNEL)
                                else:
                                    print 'broadcating to channels [', data, ']'
                                    self.broadcast_to_channel(socket, data)
                        else:
                            if socket in self.socket_list:
                                self.socket_list.remove(socket)
                    except Exception as e:                        
                        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), e
                        #self.leave(socket, m.group(2))
                        if socket in self.socket_list:
                            self.socket_list.remove(socket)
                            for channel in self.channel_list:
                                if socket in channel.clients:
                                    channel.clients.remove(socket)
                        continue
        self.server.close()

    def send(self, socket, message):
        try:
            print 'sending' + message + 'end'
            message = self.pad(message)
            socket.send(message)
        except:
            print 'message not sent, socket closed'
            socket.close()
            if s in self.socket_list:
                self.socket_list.remove(s)
    
    def pad(self, msg):
        while len(msg) < utils.MESSAGE_LENGTH:
            msg += ' '
        return msg
    
    def create(self, socket, new_channel_name, client_name):
        self.leave(socket, client_name)
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

    def receive_msg(self, socket):
        chunks = []
        bytes_recd = 0
        while bytes_recd < utils.MESSAGE_LENGTH:
            chunk = socket.recv(min(utils.MESSAGE_LENGTH - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

args = sys.argv
if len(args) != 2:
    print 'Please supply port number'
    sys.exit()

server = Server(args[1])
server.chat()

                    