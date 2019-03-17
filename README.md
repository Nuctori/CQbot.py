# CQbot.py
A tiny framework use python to make a qq bot dependency upon CoolQ
you can use it to build a qqbot in a easy way

一个依赖于酷Q机器人的微型QQ机器人框架
能让你轻松的编写简单的QQ机器人。



    import CQbot

    @CQbot.route('hello')
    def hello(handle,QQInfo):
        CQbot.sendMsg(handle,QQInfo,'你好,祖国!')

    if __name__ == "__main__":
        CQbot.Run()
    
-------------------------------------

只需这样，就可以让QQ机器人收到“hello“信息的时，回复“你好,祖国!”

使用本框架前，需要下载酷Q的QQ机器人
https://cqp.cc/
使用酷Q机器人登陆QQ，并在酷Q里导入 CQbot.py/pybot框架/易语言端酷Q插件/moe.zri.pybot.cpk 插件。
然后即可使用本框架。

框架原理为使用TCP连接酷Q和python服务器。酷Q将接收到的QQ信息以TCP的形式发送给python服务器
python服务器将信息处理后返回信息给酷Q,酷Q从服务器中收到的信息将会发送到QQ上
