import tkinter as tk
import tkinter.messagebox

window = tk.Tk()
window.title("Chat Room Main")
window.geometry("400x300")
window.resizable(height=False, width=False)


def fun(content):
    tkinter.messagebox.showinfo(title="view", message=content)


def main():
    can = tk.Canvas(window, bg="purple", height=140, width=400)
    can.pack()
    image_file = tk.PhotoImage(file="view.gif")
    image = can.create_image(200, 0, anchor="n", image=image_file)

    tk.Label(window, text="Welcome join us !", font=("Arial", 18, "bold"), fg="blue").pack()

    tk.Label(window, text="User name", font=("Arial", 14), fg="black").place(x=10, y=180)
    tk.Label(window, text="Password", font=("Arial", 14), fg="black").place(x=10, y=220)

    entry_name_value = tk.StringVar()
    entry_user_name = tk.Entry(window, width=25, textvariable=entry_name_value)
    entry_user_pwd = tk.Entry(window, width=25, show="*")
    entry_user_name.place(x=150, y=180)
    entry_user_pwd.place(x=150, y=220)

    bt_login = tk.Button(window, text="Entry", font=("Arial", 12, "bold"), activebackground="yellow")
    bt_login.place(x=70, y=260)
    bt_register = tk.Button(window, text="Register", font=("Arial", 12, "bold"), activebackground="yellow",
                            command=lambda: fun(entry_name_value.get()))
    bt_register.place(x=230, y=260)

    window.mainloop()


if __name__ == '__main__':
    main()
