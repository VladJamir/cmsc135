import sys
import socket
import utils

class  Client(object):
    
    def __init__(self, name, host, port):
        self.name = '[' + name + ']'
        self.host = host
        self.port = int(port)
        self.socket = socket.socket()
        self.connected = False
    
    def run(self):
        try:
            self.socket.connect((self.host, self.port))
        except:
            print utils.CLIENT_CANNOT_CONNECT.format(self.host, self.port)
            sys.exit()
        sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX, ); sys.stdout.flush()
        while True:
            socket_list = [sys.stdin, self.socket]
            readable, writable, exception = select.select(socket_list, [], [])
            for s in readable:
                if s is server:
                    data = s.recv(1024)
                    if not data:
                        print utils.CLIENT_SERVER_DISCONNECTED.format(self.host, self.port)
                        sys.exit()
                    else:
                        sys.stdout.write(data)
                        sys.stdout.write(utils.CLIENT_WIPE_ME, utils.CLIENT_MESSAGE_PREFIX, ); sys.stdout.flush()
                else:
                    msg = sys.stdin.readline()
                    msg = name + ' ' + msg
                    s.send(name msg)
                    sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX, ); sys.stdout.flush()
                
args = sys.argv
if len(args) != 4:
    print 'Please supply name, host, and port'
    sys.exit()

client = Client(args[1], args[2], args[3])
client.run()
