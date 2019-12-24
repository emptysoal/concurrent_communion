import tkinter as tk

top = tk.Tk()
top.geometry("300x300")

map_data1 = [
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]
]

map_data2 = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]

map_data = map_data1
mark = True

color = {
    0: "purple",
    1: "blue"
}


def change_button():
    bt = tk.Button(top, text="change mode", bg="green", activebackground="aqua", command=change_exe)
    bt.place(x=30, y=200)


def change_exe():
    global map_data
    global mark
    if mark:
        mark = False
        map_data = map_data2
    else:
        mark = True
        map_data = map_data1


def init_view():
    map_labels = []  # 游戏各方块的lable Widget
    for r in range(4):
        row = []
        for c in range(len(map_data[0])):
            value = map_data[r][c]
            text = ""
            bg = color[value]
            label = tk.Label(top, text=text, width=5, height=2, font=("黑体", 10, "bold"), bg=bg)
            label.grid(row=r, column=c, padx=1, pady=1)
            row.append(label)
        map_labels.append(row)
    map_labels[0][0].after(500, init_view)


def main():
    init_view()
    change_button()
    top.mainloop()


if __name__ == '__main__':
    main()
