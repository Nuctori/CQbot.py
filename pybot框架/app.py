import CQbot

@CQbot.route('hello')
def hello(handle,QQInfo):
    CQbot.sendMsg(handle,QQInfo,'你好！')

if __name__ == "__main__":
    CQbot.Run()