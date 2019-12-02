"""
    模拟客户端逻辑处理
"""
from model import *
from socket import *
from threading import Thread, Lock
from time import sleep
import tkinter.messagebox


class ChatClient:
    def __init__(self):
        self.__host = HOST
        self.__port = PORT
        self.__addr = (self.__host, self.__port)
        self.__sockfd = None
        self.__file_path = None  # 用于上传文件
        self.__file_name = None  # 用于下载文件
        self.__name = None  # 用户名
        self.list_msgs = ["", "", "", "", "", "", "", ""]  # 信息存储列表
        self.__lock = Lock()  # 创建锁对象
        self.map = self.__init_map()  # 游戏map初始化
        self.was_in_game = False  # 是否在游戏中的标志，False不在，True在
        self.allow_join = False   # 是否允许加入游戏标志，False不允许，True允许

    def connect_server(self):
        """
            连接服务器主网络
        """
        self.__sockfd = socket(AF_INET, SOCK_STREAM)
        self.__sockfd.connect(self.__addr)

    def login(self, user, passwd):
        """
            用户登录请求处理
        :param user: 用户名
        :param passwd: 密码
        :return: “OK”或 登录不成功的原因
        """
        self.__sockfd.send(("E %s %s" % (user, passwd)).encode())
        response = self.__sockfd.recv(1024)
        if response.decode() == "OK":
            self.__name = user
        return response.decode()

    def register(self, user, passwd):
        """
            用户注册请求处理
        :param user: 用户名
        :param passwd: 密码
        :return: “OK”或 注册不成功的原因
        """
        self.__sockfd.send(("R %s %s" % (user, passwd)).encode())
        response = self.__sockfd.recv(1024)
        return response.decode()

    def chat_recv(self):
        """
            聊天功能正式开启（创建新线程接收信息）
        """
        thread_recv = Thread(target=self.__recv_msg)
        thread_recv.setDaemon(True)
        thread_recv.start()

    # 发消息函数
    def send_msg(self, msg_info):
        if msg_info:
            self.__sockfd.send(("C %s %s" % (self.__name, msg_info)).encode())
            with self.__lock:
                self.list_msgs.append(msg_info)
                self.list_msgs.pop(0)

    # 收消息函数
    def __recv_msg(self):
        while True:
            data = self.__sockfd.recv(1024)
            if data == b"###ALLOW###":
                tkinter.messagebox.showinfo(title="File Put Info", message="File Put Succeed!")
                file_put_thread = Thread(target=self.__file_put, args=(self.__file_path,))
                file_put_thread.setDaemon(True)
                file_put_thread.start()
            elif data == b"$$The file is already exist , please change one$$":
                tkinter.messagebox.showerror(title="File Put Error", message=data.decode().strip("$$"))
            elif data == b"###AGREE###":
                tkinter.messagebox.showinfo(title="File Get Info", message="File Get Succeed!")
                file_get_thread = Thread(target=self.__file_get, args=(self.__file_name,))
                file_get_thread.setDaemon(True)
                file_get_thread.start()
            elif data == b"$$There is no file what you want...$$":
                tkinter.messagebox.showerror(title="File Put Error", message=data.decode().strip("$$"))
            elif data == b"You are allowed":
                self.was_in_game = True
            elif data == b"you can join the game":
                self.was_in_game = True
                self.allow_join = True
            elif data == b"The game has already been joined":
                self.allow_join = False
            elif data == b"##EXIT##":
                return
            else:
                with self.__lock:
                    self.list_msgs.append(data.decode())
                    self.list_msgs.pop(0)

    # 上传文件请求发送
    def put_file(self, file_path):
        self.__file_path = file_path
        self.__sockfd.send(("F %s %s" % (self.__name, self.__file_path)).encode())

    # 下载文件请求发送
    def get_file(self, file_name):
        self.__file_name = file_name
        self.__sockfd.send(("L %s" % self.__file_name).encode())

    # 上传文件函数
    @staticmethod
    def __file_put(path):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(("127.0.0.1", 32803))
        file_name = path.split("/")[-1]
        sock.send(file_name.encode())
        sleep(2)
        f = open(path, "rb")
        while True:
            data = f.read(2048)
            if not data:
                sleep(2)
                sock.send(b"###")  # 结束上传标识
                f.close()
                sock.close()
                break
            sock.send(data)

    # 下载文件函数
    @staticmethod
    def __file_get(file_name):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(("127.0.0.1", 32804))
        target_dir = "./download"
        sock.send(file_name.encode())
        f = open(("%s/%s" % (target_dir, file_name)), "wb")
        while True:
            data = sock.recv(2048)
            if data == b"$$$":  # 结束下载标识
                f.close()
                sock.close()
                break
            f.write(data)

    @staticmethod
    def __init_map():
        """
            初始化游戏map
        """
        map = []
        for c in range(15):
            map_r = []
            for r in range(15):
                map_r.append(0)
            map.append(map_r)
        return map

    def game_request(self):
        self.__sockfd.send(("G %s" % self.__name).encode())

    def game_accept(self, proposer):
        self.__sockfd.send(("D %s %s" % (self.__name, proposer)).encode())
