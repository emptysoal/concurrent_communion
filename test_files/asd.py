import tkinter as tk
import random


def rand_num(a, b):
    t.delete(1.0, 2.0)
    t.insert("end", random.randint(a, b))
    t.after(100, rand_num, a, b)


top = tk.Tk()
t = tk.Text(top, width=20, height=5)
t.place(x=20, y=20)
rand_num(1000, 1100)
top.mainloop()
