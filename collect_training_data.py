from utils import FileTool
import socket
import sys
from thread import *
import json
import re

is_collection = False
raw_acc = []
# all_raw_acc = FileTool.readPickle("lock_all_raw")
all_raw_acc = []
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 5001  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

# Start listening on socket
s.listen(10)
print 'Socket now listening'


# Function for handling connections. This will be used to create threads
def clientthread(conn):
    global is_collection,raw_acc
    # Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n')  # send only takes string
    t = 0
    # infinite loop so that function do not terminate and thread do not end.
    while True:
        # Receiving from client
        data = conn.recv(1024)
        index = [m.start() for m in re.finditer('\}', data)]
        try:
            data = data[:index[1] + 1]
            data = json.loads(data)
        except Exception as e:
            print data
            break
        if (data[u'type'] == u'acc'):
            if (is_collection):
                print data
                raw_acc.append([data[u'values'][u'x'],data[u'values'][u'y'],data[u'values'][u'z']])
        if not data:
            break

    conn.close()

def save_data(a):
    global is_collection, raw_acc, all_raw_acc
    i = 0
    while (True):
        e = raw_input("press enter to start !!!")
        if e == "":
            is_collection = True
        e = raw_input("press enter to stop !!!")
        if e == "":
            is_collection = False
        e = raw_input("press s + enter to stop !!!")
        if e == "s":
            i+=1
            print i
            all_raw_acc.append(raw_acc)
            raw_acc = []
            FileTool.writePickle("tuan_hook_all_raw",all_raw_acc)
        else:
            raw_acc = []


# now keep talking with the client
while 1:

    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))
    start_new_thread(save_data, (0,))

s.close()
