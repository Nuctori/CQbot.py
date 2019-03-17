import socketserver
import threading
from config import HOST,PORT

Routes = {}
msgqueue = []

class Server(socketserver.BaseRequestHandler):

    def handle(self):
        print('已与客户端进行连接:',self.client_address)
        try:
            while True:
                buf = self.request.recv(4096).strip()
                if not buf:
                    break
    
                print(buf.decode('GBK'))
                QQInfo = packeTotuple(buf)
                Instruction(self,QQInfo)

        except ConnectionResetError:
            print('连接已关闭')

def packeTotuple(packet)->tuple:
    '''
    将接受到的封包转化为元组
    '''
    def replace(msg):
        msg = msg.replace('：',':')
        msg = msg.replace('none','None')
        msg = msg.strip()
        return(msg)

    
    try:
        packet = packet.decode('GBK')
    except UnicodeDecodeError:
        #若转码失败，返回空元组,抛弃
        return (None,None,None,None)

    if packet[0] != "(" or packet[-1] != ")":
        raise TypeError("封包格式错误")

    #封包数据整理
    msg = packet[1:len(packet)-1]
    msg = msg.lower()
    msg = replace(msg)
    tuple_ = tuple(msg.split("|data|"))
    return tuple_


def route(key:str):
    '''
    路由装饰器，通过装饰器定义指令
    '''
    def decorate(func):
        if key:
            Routes[key] = func
        return func
    return decorate


def Instruction(handle,QQInfo):
    '''
    指令判断及执行程序
    '''
    try:
        _,_,Msg,_ = QQInfo
    except ValueError:
        return None

    routes = Routes.keys()
    for route in routes:
        if route in Msg:
            func = Routes[route]
            return func(handle,QQInfo)
    return None

def sendMsg(handle,QQInfo,msg):
    '''
    消息发送函数
    '''
    QQNum,QQGrand, _ ,msgType = QQInfo

    if not QQGrand:
        QQGrand = 'None'

    
    msgqueue.append(
    (handle,'/start/{msg}|data|{QQNum}|data|{QQGrand}|data|{msgType}/end/*1078*'
    .format(msg=msg,QQGrand=QQGrand,QQNum=QQNum,msgType=msgType).encode('GBK')))

def MsgLoop():
    '''
    轮询消息队列
    '''
    import time
    while True:
        time.sleep(0.01)
        if not msgqueue:
            continue
        msg_ = msgqueue.pop()
        handel,msg = msg_

        try:
            handel.request.sendall(msg)
        except OSError:
            #处理断开连接发送失败的请求
            pass

def Run():
    from threading import Thread
    msgloop = Thread(target=MsgLoop)
    msgloop.start()
    server = socketserver.ThreadingTCPServer((HOST,PORT),Server)
    server.serve_forever()
    

if __name__ == '__main__':
    Run()
