"""
    聊天室服务器
        主要通过IO多路复用实现
"""
from socket import *
from select import *
import chat_model
import sys


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__addr = (host, port)
        self.__sockfd = self.__create_socket()
        self.__rlist = [self.__sockfd]  # 监控读事件IO，此时里面放入了监听套接字
        self.__wlist = []  # 监控写事件IO
        self.__xlist = []  # 监控错误事件IO
        self.__data_manager = chat_model.DataManager("localhost", 3306, "root", "123456", "concurrent_communion",
                                                     "utf8")

    def __create_socket(self):
        """
            创建服务器套接字
        :return: 套接字对象
        """
        sockfd = socket(AF_INET, SOCK_STREAM)
        sockfd.bind(self.__addr)
        sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return sockfd

    def __handle(self, connfd):
        self.__data_manager.create_cur()
        request = connfd.recv(1024)
        if not request:
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
            content = request.decode().split(" ")[2]
            self.__chat_handle(connfd, name, content)  # 聊天请求处理
        elif request.decode().split(" ")[0] == "F":
            pass  # 上传文件请求处理
        elif request.decode().split(" ")[0] == "L":
            pass  # 下载文件请求处理
        elif request.decode().split(" ")[0] == "G":
            pass  # 游戏邀请请求处理
        elif request.decode().split(" ")[0] == "D":
            pass  # 接受游戏邀请请求处理
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
        :return:
        """
        if self.__data_manager.regster_deal(user, passwd):
            response = "OK"
        else:
            response = "The name has already been used"
        connfd.send(response.encode())

    def __chat_handle(self, connfd, name, content):
        """
            群发消息
        :param connfd: 对应处理发消息人的相关信息的套接字
        :param name: 发消息者用户名
        :param content: 消息内容
        """
        for client in self.__rlist:
            if client is not self.__sockfd and client is not connfd:
                client.send(("%s:%s" % (name, content)).encode())

    def __select_concurrent(self):
        """
            IO多路复用方式，循环监控各IO事件
        """
        while True:
            try:
                rs, ws, xs = select(self.__rlist, self.__wlist, self.__xlist)
                for item in rs:
                    if item is self.__sockfd:
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

    def serve_forever(self):
        """
            服务端对象启动方法
        """
        self.__sockfd.listen(5)  # 设置为监听套接字
        print("Listening the port %d" % self.port)
        self.__select_concurrent()


# 用于启动服务器
def main():
    # 定义常量
    HOST = "127.0.0.1"
    PORT = 32802
    chat_server = ChatServer(HOST, PORT)
    chat_server.serve_forever()


if __name__ == '__main__':
    main()
