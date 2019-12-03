"""
    模拟客户端界面
"""
from bll import *
import tkinter as tk
import tkinter.messagebox
from time import sleep


class ClientUI:
    def __init__(self):
        # bll对象
        self.__client = ChatClient()
        # 登录界面初始设置
        self.__window = tk.Tk()
        self.__window.title("Chat Room Main")
        self.__window.geometry("400x300")
        self.__window.resizable(height=False, width=False)
        self.__x0 = 30  # 游戏map X方向起始位置
        self.__y0 = 20  # 游戏map Y方向起始位置

    def run(self):
        self.__create_connect()  # 连接网络
        self.__first_menu()

    def __create_connect(self):
        self.__client.connect_server()

    def __first_menu(self):
        # 背景图片
        can = tk.Canvas(self.__window, bg="purple", height=140, width=400)
        can.pack()
        image_file = tk.PhotoImage(file="view.gif")
        image = can.create_image(200, 0, anchor="n", image=image_file)
        # 文本显示
        tk.Label(self.__window, text="Welcome join us !", font=("Arial", 18, "bold"), fg="blue").pack()
        tk.Label(self.__window, text="User name", font=("Arial", 14), fg="black").place(x=10, y=180)
        tk.Label(self.__window, text="Password", font=("Arial", 14), fg="black").place(x=10, y=220)
        # 用户名和密码输入框
        self.__entry_name_value = tk.StringVar()
        self.__entry_pwd_value = tk.StringVar()
        self.__entry_user_name = tk.Entry(self.__window, width=25, textvariable=self.__entry_name_value)
        self.__entry_user_pwd = tk.Entry(self.__window, width=25, show="*", textvariable=self.__entry_pwd_value)
        self.__entry_user_name.place(x=150, y=180)
        self.__entry_user_pwd.place(x=150, y=220)
        # 登录和注册按钮
        bt_login = tk.Button(self.__window, text="Entry", font=("Arial", 12, "bold"), activebackground="yellow",
                             command=self.__login)
        bt_login.place(x=70, y=260)
        bt_register = tk.Button(self.__window, text="Register", font=("Arial", 12, "bold"), activebackground="yellow",
                                command=self.__register_view)
        bt_register.place(x=230, y=260)
        self.__window.mainloop()

    def __register_view(self):
        re_window = tk.Toplevel(self.__window, height=200, width=300)
        re_window.title("Register")

        tk.Label(re_window, text="User name", font=("Arial", 12), fg="black").place(x=10, y=30)
        tk.Label(re_window, text="Password", font=("Arial", 12), fg="black").place(x=10, y=90)

        self.__register_name_value = tk.StringVar()
        self.__register_pwd_value = tk.StringVar()
        self.__register_user_name = tk.Entry(re_window, width=18, textvariable=self.__register_name_value)
        self.__register_user_pwd = tk.Entry(re_window, width=18, show="*", textvariable=self.__register_pwd_value)
        self.__register_user_name.place(x=120, y=30)
        self.__register_user_pwd.place(x=120, y=90)

        bt_commit = tk.Button(re_window, text="Commit", font=("Arial", 10, "bold"), activebackground="yellow",
                              command=self.__commit)
        bt_commit.place(x=60, y=160)
        bt_cancel = tk.Button(re_window, text="Cancel", font=("Arial", 10, "bold"), activebackground="yellow")
        bt_cancel.place(x=160, y=160)

    def __commit(self):
        user = self.__register_user_name.get()
        passwd = self.__register_user_pwd.get()
        if not user or not passwd:
            tkinter.messagebox.showwarning(title="Warning", message="user or password can not be empty!")
            return
        re = self.__client.register(user, passwd)
        if re == "OK":
            tkinter.messagebox.showinfo(title="commit information", message="注册成功，登陆后即可进入")
        else:
            tkinter.messagebox.showerror(title="commit error", message="%s" % re)
        self.__register_name_value.set("")
        self.__register_pwd_value.set("")

    def __login(self):
        user = self.__entry_user_name.get()
        passwd = self.__entry_user_pwd.get()
        re = self.__client.login(user, passwd)
        if re == "OK":
            self.__client.chat_recv()  # bll对象启动收消息进程
            self.__chat_view()  # 弹出群聊界面
        else:
            tkinter.messagebox.showerror(title="entry error", message="%s" % re)
        self.__entry_name_value.set("")
        self.__entry_pwd_value.set("")

    """------------------------------------------聊天界面-----------------------------------------------"""

    def __chat_view(self):
        self.__chat_window = tk.Toplevel(self.__window, height=420, width=400)
        self.__chat_window.title("Chat view")
        self.__chat_window.resizable(width=False, height=False)
        self.__init_chat_view()
        self.__roll_display()
        self.__msg_input_entry()
        self.__file_configure()
        self.__game_configure()

    def __init_chat_view(self):
        self.__label_obj = []
        for i in range(8):
            label = tk.Label(self.__chat_window, text="", bg="greenyellow", anchor="w")
            self.__label_obj.append(label)
        for i in range(8):
            self.__label_obj[i].place(x=20, y=10 + i * 30)

    def __roll_display(self):
        for i in range(8):
            self.__label_obj[i]["text"] = self.__client.list_msgs[i]
        self.__label_obj[0].after(100, self.__roll_display)

    def __msg_input_entry(self):
        entry_msg_value = tk.StringVar()
        entry_msg = tk.Entry(self.__chat_window, width=35, textvariable=entry_msg_value)
        entry_msg.place(x=20, y=260)
        bt_send_msg = tk.Button(self.__chat_window, text="send", font=("Arial", 10, "bold"), activebackground="yellow",
                                width=4, command=lambda: self.__send_msg_button(entry_msg, entry_msg_value))
        bt_send_msg.place(x=320, y=258)

    def __send_msg_button(self, entry_obj, entry_info):
        self.__client.send_msg(entry_obj.get())
        entry_info.set("")

    """------------------------------------------聊天界面-----------------------------------------------"""

    """---------------------------------------文件传输控件设置-------------------------------------------"""

    def __file_configure(self):
        # 上传文件
        label_put = tk.Label(self.__chat_window, text="file path", font=("Arial", 12, "bold"), fg="purple")
        label_put.place(x=20, y=300)
        entry_file_path_value = tk.StringVar()
        entry_file_path = tk.Entry(self.__chat_window, width=25, textvariable=entry_file_path_value)
        entry_file_path.place(x=98, y=300)
        bt_file_put = tk.Button(self.__chat_window, text="put file", font=("Arial", 10, "bold"), width=4,
                                activebackground="yellow",
                                command=lambda: self.__put_file_button(entry_file_path, entry_file_path_value))
        bt_file_put.place(x=320, y=298)
        # 下载文件
        label_get = tk.Label(self.__chat_window, text="file name", font=("Arial", 12, "bold"), fg="purple")
        label_get.place(x=20, y=340)
        entry_file_name_value = tk.StringVar()
        entry_file_name = tk.Entry(self.__chat_window, width=25, textvariable=entry_file_name_value)
        entry_file_name.place(x=98, y=340)
        bt_file_get = tk.Button(self.__chat_window, text="get file", font=("Arial", 10, "bold"), width=4,
                                activebackground="yellow",
                                command=lambda: self.__get_file_button(entry_file_name, entry_file_name_value))
        bt_file_get.place(x=320, y=338)

    # 文件上传按钮关联函数
    def __put_file_button(self, entry_obj, entry_info):
        if entry_obj.get():
            try:
                f = open(entry_obj.get(), "rb")  # 拿到路径
            except FileNotFoundError:
                tkinter.messagebox.showerror(title="put file error", message="您的本地不存在该文件，上传指令无效！")
            else:
                f.close()
                self.__client.put_file(entry_obj.get())
            finally:
                entry_info.set("")

    # 文件下载按钮关联函数
    def __get_file_button(self, entry_obj, entry_info):
        if entry_obj.get():
            self.__client.get_file(entry_obj.get())
            entry_info.set("")

    """---------------------------------------文件传输控件设置-------------------------------------------"""

    """---------------------------------------游戏相关控件设置-------------------------------------------"""

    def __game_configure(self):
        # 游戏邀请发送
        bt_game_request = tk.Button(self.__chat_window, text="request", font=("Arial", 10, "bold"), width=6,
                                    activebackground="yellow", command=self.__game_request)
        bt_game_request.place(x=20, y=378)
        # 游戏邀请接受
        label_accept = tk.Label(self.__chat_window, text="proposer", font=("Arial", 11, "bold"), fg="purple")
        label_accept.place(x=150, y=380)
        entry_proposer_value = tk.StringVar()
        entry_proposer = tk.Entry(self.__chat_window, width=8, textvariable=entry_proposer_value)
        entry_proposer.place(x=225, y=380)
        bt_game_accept = tk.Button(self.__chat_window, text="accept", font=("Arial", 10, "bold"), width=6,
                                   activebackground="yellow",
                                   command=lambda: self.__game_accept(entry_proposer, entry_proposer_value))
        bt_game_accept.place(x=306, y=378)

    # 游戏邀请按钮关联函数
    def __game_request(self):
        if self.__client.was_in_game == True:  # 先判断自己是否已处于一个游戏
            tkinter.messagebox.showerror(title="Request Error", message="You are in a game now")
            return  # 已在游戏中则中止后续处理
        self.__client.game_request()  # 游戏请求发送
        self.__client.mark = 1  # 游戏标记变更(表明此时为发起者)
        self.__client.mark_adv = 2  # 对手游戏标记变更(表明对手为接受者)
        self.__game_window = tk.Toplevel(self.__chat_window, height=360, width=340)  # 棋盘外框架设置
        self.__game_window.title("game view")
        self.__game_window.resizable(width=False, height=False)
        self.__canvas_set()  # 生成棋盘视图

    # 游戏接受按钮关联函数
    def __game_accept(self, entry_obj, entry_info):
        if self.__client.was_in_game == True:  # 先判断自己是否已处于一个游戏
            tkinter.messagebox.showerror(title="Accept Error", message="You are in a game now")
            return  # 已在游戏中则中止后续处理
        if not entry_obj.get():  # 判断对手名称处输入是否为空
            tkinter.messagebox.showerror(title="Adversary Error", message="Adversary is empty")
            return
        self.__client.game_accept(entry_obj.get())  # 游戏接受请求发送
        entry_info.set("")
        sleep(1)
        if self.__client.allow_join == False:
            tkinter.messagebox.showerror(title="Accept Error", message="The game has already been joined")
            return
        self.__client.mark = 2  # 游戏标记变更(表明此时为接受者)
        self.__client.mark_adv = 1  # 对手游戏标记变更(表明对手为发起者)
        self.__game_window = tk.Toplevel(self.__chat_window, height=360, width=340)  # 棋盘外框架设置
        self.__game_window.title("game view")
        self.__game_window.resizable(width=False, height=False)
        self.__canvas_set()  # 生成棋盘视图

    def __canvas_set(self):  # 基础布局设置
        canvas = tk.Canvas(self.__game_window, bg="#bbb", width=340, height=360)  # 背景
        self.__line_set(canvas)  # 网格线
        self.__mark_set(canvas)  # 行列号
        self.__handle_widget(canvas)  # 操作控件
        self.__init_ovals(canvas)  # 棋子控件
        canvas.pack()

    # 网格线
    def __line_set(self, canvas):
        for r in range(15):  # 横线
            canvas.create_line(self.__x0, self.__y0 + r * 20, 310, self.__y0 + r * 20)
        for c in range(15):  # 竖线
            canvas.create_line(self.__x0 + c * 20, self.__y0, self.__x0 + c * 20, 300)
        canvas.create_oval(self.__x0 - 2 + 140, self.__y0 - 2 + 140, self.__x0 + 2 + 140, self.__y0 + 2 + 140,
                           fill="black")
        canvas.create_oval(self.__x0 - 2 + 60, self.__y0 - 2 + 60, self.__x0 + 2 + 60, self.__y0 + 2 + 60, fill="black")
        canvas.create_oval(self.__x0 - 2 + 220, self.__y0 - 2 + 60, self.__x0 + 2 + 220, self.__y0 + 2 + 60,
                           fill="black")
        canvas.create_oval(self.__x0 - 2 + 60, self.__y0 - 2 + 220, self.__x0 + 2 + 60, self.__y0 + 2 + 220,
                           fill="black")
        canvas.create_oval(self.__x0 - 2 + 220, self.__y0 - 2 + 220, self.__x0 + 2 + 220, self.__y0 + 2 + 220,
                           fill="black")

    # 行号&列号
    @staticmethod
    def __mark_set(canvas):
        for r in range(15):  # 横向
            text = str(r + 1)
            label_row = tk.Label(canvas, text=text, width=2, fg="blue", bg="#bbb", font=("Arial 10"))
            label_row.place(x=4, y=10 + r * 20)
        for c in range(15):  # 纵向
            text = str(c + 1)
            label_col = tk.Label(canvas, text=text, width=2, fg="blue", bg="#bbb", font=("Arial 10"))
            label_col.place(x=22 + c * 20, y=307)

    # 坐标输入与确认控件
    def __handle_widget(self, canvas):
        # 自己
        tk.Label(canvas, text="行", bg="#bbb").place(x=175, y=327)
        entry_self_row_value = tk.StringVar()
        entry_self_row_obj = tk.Entry(canvas, textvariable=entry_self_row_value, font=("Arial 10"), width=2)
        entry_self_row_obj.place(x=195, y=330)
        tk.Label(canvas, text="列", bg="#bbb").place(x=222, y=327)
        entry_self_col_value = tk.StringVar()
        entry_self_col_obj = tk.Entry(canvas, textvariable=entry_self_col_value, font=("Arial 10"), width=2)
        entry_self_col_obj.place(x=242, y=330)
        bt_self = tk.Button(canvas, text="OK", font=("Arial 7 bold"), width=1, height=1,
                            command=lambda: self.__oval_join_self(entry_self_row_obj, entry_self_col_obj,
                                                                  entry_self_row_value, entry_self_col_value))
        bt_self.place(x=270, y=329)

    # 棋子控件设置
    def __init_ovals(self, canvas):
        for c in range(15):
            for r in range(15):  # 横向设置
                if self.__client.map[c][r] == 1:
                    canvas.create_oval(self.__x0 - 7 + r * 20, self.__y0 - 7 + c * 20, self.__x0 + 7 + r * 20,
                                       self.__y0 + 7 + c * 20, fill="white")
                if self.__client.map[c][r] == 2:
                    canvas.create_oval(self.__x0 - 7 + r * 20, self.__y0 - 7 + c * 20, self.__x0 + 7 + r * 20,
                                       self.__y0 + 7 + c * 20, fill="black")
        canvas.after(100, lambda: self.__init_ovals(canvas))

    # 根据输入的坐标填充棋子（链接坐标提交按钮）
    def __oval_join_self(self, entry_obj_row, entry_obj_col, entry_info_row, entry_info_col):
        if self.__client.was_in_game == False:
            return
        try:
            r = int(entry_obj_row.get().strip()) - 1
            c = int(entry_obj_col.get().strip()) - 1
        except ValueError:
            return
        else:
            if self.__client.map[r][c] == 0:
                self.__client.map[r][c] = self.__client.mark
            entry_info_row.set("")
            entry_info_col.set("")
            self.__client.game_step_send(("%s&%s" % (str(r), str(c))))  # 将走棋步骤发送
            if self.__client.game_obj.win(r, c):
                self.__client.init_game()
                tkinter.messagebox.showinfo(title="Game Over", message="You Win")

    """---------------------------------------游戏相关控件设置-------------------------------------------"""


if __name__ == '__main__':
    def main():
        client = ClientUI()
        client.run()


    main()
