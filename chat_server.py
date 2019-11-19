"""
    聊天室服务器
        主要通过IO多路复用实现
"""
from socket import *
from select import *


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__addr = (host, port)
        self.__sockfd = self.__create_socket()
        self.__rlist = [self.__sockfd]  # 监控读事件IO，此时里面放入了监听套接字
        self.__wlist = []  # 监控写事件IO
        self.__xlist = []  # 监控错误事件IO

    def __create_socket(self):
        """
            创建服务器套接字
        :return: 套接字对象
        """
        sockfd = socket(AF_INET, SOCK_STREAM)
        sockfd.bind(self.__addr)
        return sockfd

    def __select_concurent(self):
        while True:
            rs, ws, xs = select(self.__rlist, self.__wlist, self.__xlist)
            for item in rs:
                if item is self.__sockfd:
                    connfd, addr = self.__sockfd.accept()
                    self.__rlist.append(connfd)

    def serve_forever(self):
        self.__sockfd.listen(5)  # 设置为监听套接字
        print("Listening the port %d" % self.port)
        self.__select_concurent()


# 用于启动服务器
def main():
    # 定义常量
    HOST = "127.0.0.1"
    PORT = 32802
    chat_server = ChatServer(HOST, PORT)
    chat_server.serve_forever()


if __name__ == '__main__':
    main()
