import socket

s = socket.socket()
s.connect(('localhost',13435))

s.send('(Sender|data|QunNum|data|hello|data|群消息)'.encode('utf-8'))
import time
print(s.recv(1024))

time.sleep(1)
s.close()