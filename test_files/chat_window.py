"""
    聊天界面
"""
import tkinter as tk

window = tk.Tk()
window.title("Chat Room Main")
window.geometry("400x300")
window.resizable(height=False, width=False)


def register():
    re_window = tk.Toplevel(window, height=200, width=300)
    re_window.title("Register")

    tk.Label(re_window, text="User name", font=("Arial", 12), fg="black").place(x=10, y=30)
    tk.Label(re_window, text="Password", font=("Arial", 12), fg="black").place(x=10, y=70)
    tk.Label(re_window, text="Confirm Pwd", font=("Arial", 12), fg="black").place(x=10, y=110)

    entry_user_name = tk.Entry(re_window, width=18)
    entry_user_pwd = tk.Entry(re_window, width=18, show="*")
    entry_user_commit = tk.Entry(re_window, width=18, show="*")
    entry_user_name.place(x=120, y=30)
    entry_user_pwd.place(x=120, y=70)
    entry_user_commit.place(x=120, y=110)

    bt_login = tk.Button(re_window, text="Commit", font=("Arial", 10, "bold"), activebackground="yellow")
    bt_login.place(x=60, y=160)
    bt_register = tk.Button(re_window, text="Cancel", font=("Arial", 10, "bold"), activebackground="yellow")
    bt_register.place(x=160, y=160)


def main():
    # 背景图片
    can = tk.Canvas(window, bg="purple", height=140, width=400)
    can.pack()
    image_file = tk.PhotoImage(file="view.gif")
    image = can.create_image(200, 0, anchor="n", image=image_file)

    tk.Label(window, text="Welcome join us !", font=("Arial", 18, "bold"), fg="blue").pack()

    tk.Label(window, text="User name", font=("Arial", 14), fg="black").place(x=10, y=180)
    tk.Label(window, text="Password", font=("Arial", 14), fg="black").place(x=10, y=220)

    entry_user_name = tk.Entry(window, width=25)
    entry_user_pwd = tk.Entry(window, width=25, show="*")
    entry_user_name.place(x=150, y=180)
    entry_user_pwd.place(x=150, y=220)

    bt_login = tk.Button(window, text="Entry", font=("Arial", 12, "bold"), activebackground="yellow")
    bt_login.place(x=70, y=260)
    bt_register = tk.Button(window, text="Register", font=("Arial", 12, "bold"), activebackground="yellow",
                            command=register)
    bt_register.place(x=230, y=260)

    window.mainloop()


if __name__ == '__main__':
    main()
