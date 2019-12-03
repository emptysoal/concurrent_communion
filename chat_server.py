"""
    聊天室服务器
        主要通过IO多路复用实现
"""
from socket import *
from select import *
from multiprocessing import Process, Queue
import sys
import signal
from time import sleep
import chat_model


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__addr = (host, port)
        self.__sockfd = self.__create_socket()
        self.__rlist = [self.__sockfd]  # 监控读事件IO，此时里面放入了监听套接字
        self.__wlist = []               # 监控写事件IO
        self.__xlist = []               # 监控错误事件IO
        self.__data_manager = chat_model.DataManager("localhost", 3306, "root", "123456",
                                                     "concurrent_communion", "utf8")
        self.__buffer = Queue(10)       # 信息存储缓存队列
        self.__dict_game_info = {}      # 用于存放游戏对局双方connfd，键为游戏一方用户名，
                                        # 值为列表，列表中分别为对应用户名的connfd和对手的connfd

    def __create_socket(self):
        """
            创建服务器套接字
        :return: 套接字对象
        """
        sockfd = socket(AF_INET, SOCK_STREAM)
        sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sockfd.bind(self.__addr)
        return sockfd

    def __handle(self, connfd):
        self.__data_manager.create_cur()  # 创建游标对象,用于读取数据库信息
        request = connfd.recv(1024)
        if not request:
            connfd.send(b"##")
            return "Q"
        if request.decode().split(" ")[0] == "E":
            name = request.decode().split(" ")[1]
            password = request.decode().split(" ")[2]
            self.__verify_user(connfd, name, password)  # 登录请求处理
        elif request.decode().split(" ")[0] == "R":
            name = request.decode().split(" ")[1]
            password = request.decode().split(" ")[2]
            self.__register(connfd, name, password)  # 注册请求处理
        elif request.decode().split(" ")[0] == "C":
            name = request.decode().split(" ")[1]
            content = request.decode().split(" ", 2)[2]
            self.__chat_handle(connfd, name, content)  # 聊天内容群发处理
        elif request.decode().split(" ")[0] == "F":
            name = request.decode().split(" ")[1]
            file_name = (request.decode().split(" ")[2]).split("/")[-1]
            self.__file_put_handle(connfd, name, file_name)  # 上传文件请求处理
        elif request.decode().split(" ")[0] == "L":
            file_name = request.decode().split(" ")[1]
            self.__file_get_handle(connfd, file_name)  # 下载文件请求处理
        elif request.decode().split(" ")[0] == "G":
            name = request.decode().split(" ")[1]
            self.__game_request(connfd, name)  # 游戏邀请请求处理
        elif request.decode().split(" ")[0] == "D":
            name = request.decode().split(" ")[1]
            adversary_name = request.decode().split(" ")[2]  # 对手的用户名（即接受谁发起的游戏邀请）
            self.__game_accept(connfd, name, adversary_name)  # 接受游戏邀请请求处理
        elif request.decode().split(" ")[0] == "S":
            name = request.decode().split(" ")[1]
            step = request.decode().split(" ")[2]  # step结构为X&Y
            self.__game_step(name, step)  # 游戏走法处理
        elif request.decode().split(" ")[0] == "V":
            name = request.decode().split(" ")[1]
            self.__game_victory(name)  # 游戏胜利处理
        elif request.decode().split(" ")[0] == "B":
            name = request.decode().split(" ")[1]
            self.__game_defeat(name)  # 游戏失败处理
        else:
            pass  # 退出请求处理

    def __verify_user(self, connfd, user, passwd):
        """
            登录时，验证用户名和密码
        :param connfd: 对应某一用户的套接字
        :param user: 登录所需用户名
        :param passwd: 登录所需密码
        """
        if self.__data_manager.login_deal(user, passwd):
            response = "OK"
        else:
            response = "name or password Error, please check or sign up again"
        connfd.send(response.encode())

    def __register(self, connfd, user, passwd):
        """
            注册时，验证用户名
        :param connfd: 对应某一用户的套接字
        :param user: 注册所需用户名
        :param passwd: 注册所需密码
        """
        if self.__data_manager.judge_user(user):  # 判断该用户名是否可用
            response = "OK"
            self.__buffer.put(("BASE", user, passwd))  # 将用户基本信息传给缓存队列，“BASE”为基本信息标识
        else:
            response = "The name has already been used"
        connfd.send(response.encode())

    def __chat_handle(self, connfd, name, content):
        """
            群发消息,发送完毕后将消息信息记录到数据库
        :param connfd: 对应处理发消息人的相关信息的套接字
        :param name: 发消息者用户名
        :param content: 消息内容
        """
        for client in self.__rlist:  # 群发消息
            if client is not self.__sockfd and client is not connfd:
                client.send(("'%s':  %s" % (name, content)).encode())
        self.__buffer.put(("CHAT", name, content))  # 将聊天相关信息上传到缓存队列

    def __file_put_handle(self, connfd, name, file_name):
        """
            对客户欲上传的文件进行处理（判断文件是否已经存在）
        :param connfd: 对应处理发文件上传请求者的相关信息的套接字
        :param name: 文件上传请求者的用户名
        :param file_name: 要上传的文件的文件名
        """
        if self.__data_manager.is_file_exist(file_name):  # 如果文件已经存在
            response = "$$The file is already exist , please change one$$"
        else:  # 如果文件不存在
            response = "ALLOW"  # 开始文件上传标志
            self.__file_put_alert(connfd, name, file_name)
        connfd.send(response.encode())

    def __file_put_alert(self, connfd, name, file_name):
        """
            文件上传提示（群发他人XX上传了XXX）
        :param connfd: 对应处理发文件人的相关信息的套接字
        :param name: 发文件者用户名
        :param file_name: 发送的文件的文件名
        """
        for client in self.__rlist:  # 群发文件上传提示
            if client is not self.__sockfd and client is not connfd:
                client.send(("'%s'刚刚上传了'%s'" % (name, file_name)).encode())
        self.__buffer.put(("FILE", name, file_name))  # 将文件上传相关信息上传到缓存队列

    def __file_get_handle(self, connfd, file_name):
        """
            对客户要下载的文件进行处理(判断要下载的文件是否存在)
        :param connfd: 对应处理下载文件请求者的相关信息的套接字
        :param file_name: 要下载的文件的文件名
        """
        if self.__data_manager.is_file_exist(file_name):  # 如果文件存在
            response = "AGREE"
        else:
            response = "$$There is no file what you want...$$"
        connfd.send(response.encode())

    def __game_request(self, connfd, name):
        """
            游戏邀请请求处理
        :param connfd: 对应处理游戏邀请者的相关信息的套接字
        :param name: 游戏邀请者用户名
        """
        connfd.send(b"You are allowed")
        self.__dict_game_info[name] = [connfd]  # 对局字典中添加发起者信息，值为列表，列表长度为一时，为等待状态
        for client in self.__rlist:
            if client is not self.__sockfd and client is not connfd:
                client.send(("'%s'发起了游戏邀请" % name).encode())  # 群发游戏邀请通知

    def __game_accept(self, connfd, name, adversary_name):
        """
            游戏接受请求处理
        :param connfd: 对应处理接受游戏者的相关信息的套接字
        :param name: 游戏接受者用户名
        :param adversary_name: 对手用户名，即发邀请者用户名
        """
        if len(self.__dict_game_info[adversary_name]) == 1:  # 发起者为等待状态
            self.__dict_game_info[name] = [connfd, (self.__dict_game_info[adversary_name])[0]]  # 字典添加接受者信息
            (self.__dict_game_info[adversary_name]).append(connfd)  # 发起者为键的字典元素中，添加接受者的connfd
            response = "you can join the game"
            for client in self.__rlist:  # 群发其他人已接受游戏邀请
                if client is not self.__sockfd and client is not connfd:
                    client.send(("'%s'接受了'%s'的游戏邀请" % (name, adversary_name)).encode())  # 群发游戏邀请通知
        else:
            response = "The game has already been joined"
        connfd.send(response.encode())  # 回复游戏接受者

    def __game_step(self, name, step):
        """
            处理游戏步骤信息（将步骤信息发送给对手）
        :param connfd: 对应处理游戏进行者的相关信息的套接字
        :param name: 游戏步骤发送者用户名
        :param step: 游戏步骤信息
        """
        (self.__dict_game_info[name])[1].send(("STEP %s" % step).encode())

    def __game_victory(self, name):
        """
            将用户名和胜利结果上传到缓存队列
        :param name: 胜利者用户名
        """
        self.__buffer.put(("GAME", name, "victory"))

    def __game_defeat(self, name):
        """
            将用户名和失败结果上传到缓存队列
        :param name: 失败者用户名
        """
        self.__buffer.put(("GAME", name, "defeat"))

    @staticmethod
    def __recv_file(c):
        """
            接收上传的文件
        """
        file_name = c.recv(512).decode()  # 接收文件名称
        f = open("%s/%s" % ("./files", file_name), "wb")  # 新建文件，存储上传内容
        while True:
            data = c.recv(2048)  # 接收文件内容
            if data == b"###":  # 上传结束标志
                f.close()
                c.close()
                break
            f.write(data)

    def __wait_put_file(self):
        """
            等待客户端上传文件的连接,并分配子进程处理文件
        """
        s = socket(AF_INET, SOCK_STREAM)  # 创建新的套接字,专门用于接收文件上传
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 32803))  # 绑定文件传输网络的地址
        s.listen(5)
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # 处理僵尸进程
        while True:
            c, addr = s.accept()  # 当有传输文件的客户端连接时，分配子进程接收文件
            file_recv_process = Process(target=self.__recv_file, args=(c,))
            file_recv_process.daemon = True
            file_recv_process.start()

    @staticmethod
    def __send_file(c):
        """
            向客户端发送文件
        """
        file_name = c.recv(512).decode()  # 接收文件名称
        f = open("%s/%s" % ("./files", file_name), "rb")  # 打开客户端需求的文件
        while True:
            data = f.read(2048)  # 读取文件内容
            if not data:
                sleep(2)
                c.send(b"$$$")  # 下载结束标志
                f.close()
                c.close()
                break
            c.send(data)  # 发送文件内容

    def __wait_get_file(self):
        """
            等待客户端下载文件的连接,并分配子进程处理文件
        """
        s = socket(AF_INET, SOCK_STREAM)  # 创建新的套接字,专门用于向客户端发送文件
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 32804))  # 绑定文件传输网络的地址
        s.listen(5)
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # 处理僵尸进程
        while True:
            c, addr = s.accept()  # 当有传输文件的客户端连接时，分配子进程接收文件
            file_send_process = Process(target=self.__send_file, args=(c,))
            file_send_process.daemon = True
            file_send_process.start()

    def __select_concurrent(self):
        """
            IO多路复用方式，循环监控各IO事件，针对不同IO分别处理
        """
        while True:
            try:
                rs, ws, xs = select(self.__rlist, self.__wlist, self.__xlist)  # 监控IO发生
                for item in rs:
                    if item is self.__sockfd:  # 发生IO的为监听套接字时
                        connfd, addr = self.__sockfd.accept()
                        self.__rlist.append(connfd)
                    else:
                        if self.__handle(item) == "Q":
                            self.__rlist.remove(item)
                            item.close()
                            continue
            except KeyboardInterrupt:
                self.__sockfd.close()
                sys.exit("服务器退出！")
            except Exception as e:
                print(e)
                continue

    def __start_buffer(self):
        # 创建游标对象,用于向数据库写入信息
        self.__data_manager.create_cur()
        while True:
            buffer_info = self.__buffer.get()  # 循环从缓存队列中获取信息(mark,name,content) e.g.("BASE","Lily","456")
            if buffer_info[0] == "BASE":  # 录入基本信息标识为"BASE"
                self.__data_manager.regster_deal(buffer_info[1], buffer_info[2])
            elif buffer_info[0] == "CHAT":  # 录入聊天记录标识为"CHAT"
                self.__data_manager.update_chat(buffer_info[1], buffer_info[2])
            elif buffer_info[0] == "FILE":  # 录入文件上传记录标识为"FILE"
                self.__data_manager.update_file_put(buffer_info[1], buffer_info[2])
            elif buffer_info[0] == "GAME":  # 录入游戏结果记录标识为"GAME"
                self.__data_manager.update_game_info(buffer_info[1], buffer_info[2])
            else:
                print(buffer_info)

    def serve_forever(self):
        """
            服务端对象启动方法
        """
        self.__sockfd.listen(5)  # 设置为监听套接字
        print("Listening the port %d" % self.port)

        buffer_process = Process(target=self.__start_buffer)  # 启动缓存队列进程，用于记录信息到数据库
        buffer_process.start()

        wait_file_put_process = Process(target=self.__wait_put_file)  # 启动文件上传网络，用于服务端接收文件
        wait_file_put_process.start()

        wait_file_get_process = Process(target=self.__wait_get_file)  # 启动文件下载网络，用于客户端下载文件
        wait_file_get_process.start()

        self.__select_concurrent()  # 启动IO多路复用进程，用于频繁进行数据转发


# 用于启动服务器
def main():
    # 定义常量
    HOST = "127.0.0.1"
    PORT = 32802
    chat_server = ChatServer(HOST, PORT)
    chat_server.serve_forever()


if __name__ == '__main__':
    main()
