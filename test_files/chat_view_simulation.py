import tkinter as tk

top = tk.Tk()
top.geometry("300x300")

list_msg = ["qwer", "asdf", "zxcv", "vbnm"]

a = 0

label1 = tk.Label(top, text="empty", bg="greenyellow", width=20)
label2 = tk.Label(top, text="empty", bg="greenyellow", width=20)
label3 = tk.Label(top, text="empty", bg="greenyellow", width=20)
label4 = tk.Label(top, text="empty", bg="greenyellow", width=20)
label1.place(x=20, y=10)
label2.place(x=20, y=40)
label3.place(x=20, y=70)
label4.place(x=20, y=100)


def display():
    # global a
    # a += 1
    # list_msg.pop(0)
    # list_msg.append(str(a))
    label1["text"] = list_msg[0]
    label2["text"] = list_msg[1]
    label3["text"] = list_msg[2]
    label4["text"] = list_msg[3]
    label1.after(500, display)


display()

var = tk.StringVar()
en = tk.Entry(top, textvariable=var)
en.place(x=50, y=140)


def change_item():
    if en.get():
        list_msg.append(en.get())
        list_msg.pop(0)
        var.set("")


bt = tk.Button(top, text="click", command=change_item)
bt.place(x=100, y=180)

# update()

top.mainloop()
