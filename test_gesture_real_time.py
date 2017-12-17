from utils import FileTool
import socket
import sys
from thread import *
import json
import re
from process import Process
from knn import KNN
from pyautogui import press, typewrite, hotkey
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import Queue
import threading
import time

trung_lock = FileTool.readPickle("data_processed/processed_trung_lock")
trung_punch = FileTool.readPickle("data_processed/processed_trung_punch")
trung_unlock = FileTool.readPickle("data_processed/processed_trung_unlock")
trung_hook = FileTool.readPickle("data_processed/processed_trung_hook")
trung_next = FileTool.readPickle("data_processed/processed_trung_next")
trung_prev = FileTool.readPickle("data_processed/processed_trung_prev")
tuan_lock = FileTool.readPickle("data_processed/processed_tuan_lock")
tuan_punch = FileTool.readPickle("data_processed/processed_tuan_punch")
tuan_unlock = FileTool.readPickle("data_processed/processed_tuan_unlock")
tuan_hook = FileTool.readPickle("data_processed/processed_tuan_hook")
tuan_next = FileTool.readPickle("data_processed/processed_tuan_next")
tuan_prev = FileTool.readPickle("data_processed/processed_tuan_prev")

list = []
list.extend(trung_lock)
list.extend(tuan_lock)
list.extend(trung_punch)
list.extend(tuan_punch)
list.extend(trung_unlock)
list.extend(tuan_unlock)
list.extend(trung_hook)
list.extend(tuan_hook)
list.extend(trung_next)
list.extend(tuan_next)
list.extend(trung_prev)
list.extend(tuan_prev)

knn = KNN()
knn.load_file(list)
process = Process(knn)

###########################################
is_collection = True
raw_acc = []
# all_raw_acc = FileTool.readPickle("lock_all_raw")
all_raw_acc = []
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 5000  # Arbitrary non-privileged port

###########################################
MODE_ALL = 'mode_all'
MODE_PRESENT = 'mode_present'
MODE_CONTINUOUS = 'mode_continuous'

current_mode = MODE_ALL
action_lock_count = 0
action_unlock_count = 0

# img_next=plt.imread('next.png')
# img_prev=plt.imread('prev.png')

# img = None

# callback_queue = Queue.Queue()

# def from_dummy_thread(func_to_call_from_main_thread):
#     callback_queue.put(func_to_call_from_main_thread)

# def from_main_thread_blocking():
#     callback = callback_queue.get() #blocks until an item is available
#     callback()

# def from_main_thread_nonblocking():
#     while True:
#         try:
#             callback = callback_queue.get(False) #doesn't block
#         except Queue.Empty: #raised when queue is empty
#             break
#         callback()


# def print_num(dummyid, n):
#     print "From %s: %d" % (dummyid, n)
# def dummy_run(dummyid):
#     from_dummy_thread(lambda: show_img(dummyid))
    

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

def sendAction(conn, action):
    if action == 'lock':
        FileTool.writePickle("index_img",0)
        conn.send('action_lock')

    elif action == 'unlock':
        FileTool.writePickle("index_img",2)
        conn.send('action_unlock')

    elif action == 'punch':
        FileTool.writePickle("index_img",1)
        conn.send('action_punch')

    elif action == 'hook':
        FileTool.writePickle("index_img",3)
        conn.send('action_hook')

    elif action == 'next':
        FileTool.writePickle("index_img",4)

    elif action == 'prev':
        FileTool.writePickle("index_img",5)
        conn.send('action_prev')

def handleMode(conn, action): 
    global current_mode, action_lock_count, action_unlock_count

    if action == 'lock':
        if current_mode == MODE_PRESENT:
            action_lock_count += 1
            if (action_lock_count >= 2):
                current_mode = MODE_CONTINUOUS;
                conn.send(MODE_CONTINUOUS)

    elif action == 'unlock':
        if current_mode == MODE_ALL:
            action_unlock_count += 1
            print 'Unlock count %d'%action_unlock_count
            if (action_unlock_count >= 2):
                current_mode = MODE_PRESENT;
                conn.send(MODE_PRESENT)

    elif action == 'punch' or action == 'hook' or action == 'next' or action == 'prev':
        action_lock_count = 0
        action_unlock_count = 0
        
def handleBaseOnMode(action):
    global current_mode

    if current_mode == MODE_PRESENT:
        if action == 'next':
            press('right')
        elif action == 'prev':
            press('left')


def show_img(f):
    global img
    if img is None:
        img = plt.imshow(f)
    else:
        img.set_data(f)
    plt.show()

# Function for handling connections. This will be used to create threads
def clientthread(conn,func):
    global is_collection,raw_acc, img, img1, img2
    # Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n')  # send only takes string
    conn.send(current_mode)

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
            continue    
        if (data[u'type'] == u'acc'):
            if (is_collection):
                process.process_data([data[u'values'][u'x'],data[u'values'][u'y'],data[u'values'][u'z']])
                action = process.detect_segment()
                sendAction(conn, action)
                handleMode(conn, action)
                handleBaseOnMode(action)

        if not data:
            print "break"
            continue

    conn.close()


while True:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread, (conn,show_img))
# now keep talking with the client


    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    

s.close()
