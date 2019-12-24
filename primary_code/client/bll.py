"""
    模拟客户端逻辑处理
"""
from configure_client import *
from socket import *
from threading import Thread, Lock
from time import sleep
import tkinter.messagebox
import game_logic


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
        self.game_obj = game_logic.GameLogic()  # 创建游戏对象
        self.map = self.game_obj.list  # 游戏map
        self.r = 0
        self.c = 0
        self.mark = 0  # 游戏发起者或接受者标记，发起者为1，接受者为2
        self.mark_adv = 0  # 对手标记（发起者或接受者），发起者为2，接受者为1
        self.was_in_game = False  # 是否已在游戏中的标志，False不在，True在
        self.allow_join = False  # 是否允许加入游戏标志，False不允许，True允许
        self.list_game_record = []  # 存放游戏战绩

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

    # 发普通消息函数
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
            if data == b"ALLOW":  # 允许上传文件
                tkinter.messagebox.showinfo(title="File Put Info", message="File Put Succeed!")
                file_put_thread = Thread(target=self.__file_put, args=(self.__file_path,))
                file_put_thread.setDaemon(True)
                file_put_thread.start()
            elif data == b"$$The file is already exist , please change one$$":  # 要上传的文件已存在
                tkinter.messagebox.showerror(title="File Put Error", message=data.decode().strip("$$"))
            elif data == b"AGREE":  # 允许下载文件
                tkinter.messagebox.showinfo(title="File Get Info", message="File Get Succeed!")
                file_get_thread = Thread(target=self.__file_get, args=(self.__file_name,))
                file_get_thread.setDaemon(True)
                file_get_thread.start()
            elif data == b"$$There is no file what you want...$$":  # 要下载的文件不存在
                tkinter.messagebox.showerror(title="File Put Error", message=data.decode().strip("$$"))
            elif data == b"You are allowed":  # 允许发起游戏
                self.was_in_game = True
            elif data == b"you can join the game":  # 允许接受游戏邀请
                self.was_in_game = True
                self.allow_join = True
            elif data == b"The game has already been joined":  # 要接受的游戏已经开局
                self.allow_join = False
            elif data.decode().split(" ")[0] == "STEP":  # 接收到对手的游戏步骤
                step_info = data.decode().split(" ")[1]
                self.r = int(step_info.split("&")[0])
                self.c = int(step_info.split("&")[1])
                self.map[self.r][self.c] = self.mark_adv
                # if self.game_obj.win(r, c):
                #     self.init_game()
                #     tkinter.messagebox.showinfo(title="Game Over", message="You Lose")
            elif data.decode().split(" ")[0] == "GAMERECORD":
                str_game_record = data.decode().split(" ", 1)[1]
                list_game_record = []
                for ele in str_game_record.split("&&&"):
                    list_game_record.append(ele.split("&&"))
                self.list_game_record = list_game_record
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

    def game_request(self):
        """
            游戏邀请请求发送
        """
        self.__sockfd.send(("G %s" % self.__name).encode())

    def game_accept(self, proposer):
        """
            游戏接受请求发送
        :param proposer: 所接受游戏的发起者用户名
        """
        self.__sockfd.send(("D %s %s" % (self.__name, proposer)).encode())

    def game_step_send(self, step):
        """
            游戏步骤信息发送
        :param step: 游戏步骤信息
        """
        self.__sockfd.send(("S %s %s" % (self.__name, step)).encode())

    def game_result_win(self):
        """
            游戏胜利结果发送
        """
        self.__sockfd.send(("V %s" % self.__name).encode())

    def game_result_lose(self):
        """
            游戏失败结果发送
        """
        self.__sockfd.send(("B %s" % self.__name).encode())

    def init_game(self):
        """
            游戏相关数据初始化
        """
        self.map = self.game_obj.init_map_list()
        self.r = 0
        self.c = 0
        self.mark = 0
        self.mark_adv = 0
        self.was_in_game = False
        self.allow_join = False

    def game_record_refer(self):
        """
            游戏战绩查询请求发送
        """
        self.__sockfd.send(("H %s" % self.__name).encode())
