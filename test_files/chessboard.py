import tkinter as tk

top = tk.Tk()
top.title("五子棋")
top.geometry("340x360")
top.resizable(width=False, height=False)

x0 = 30
y0 = 20

map = []

"""----------------------------------------逻辑--------------------------------------------"""


def init_map():  # 初始化map
    for c in range(15):
        map_r = []
        for r in range(15):
            map_r.append(0)
        map.append(map_r)


def win(row, line):
    if crossrange(row, line) or endwise(row, line) or slant(row, line):
        return True
    else:
        return False


def crossrange(row, line):
    """
        判断落点纵向棋子是否相同
    :param row: 横坐标
    :param line: 纵坐标
    :return:
    """
    color = map[row][line]

    positive = line + 1
    # 纵向负方向 棋盘坐标向下
    negative = line - 1
    # 纵向正方向 棋盘坐标向上
    count = 1
    while positive < 14:
        if map[row][positive] == color:
            count += 1
            positive += 1
        else:
            break
    while negative >= 0:
        if map[row][negative] == color:
            count += 1
            negative -= 1
        else:
            break
    return judge_row(count, positive, negative, row)


def endwise(row, line):
    """
        判断落点横向棋子是否相同
    :param row:
    :param line:
    :return:
    """
    color = map[row][line]

    positive = row + 1
    # 横向正方向 棋盘坐标向右
    negative = row - 1
    # 横向负方向 棋盘坐标向左
    count = 1
    while positive < 15:
        if map[positive][line] == color:
            count += 1
            positive += 1
        else:
            break
    while negative >= 0:
        if map[negative][line] == color:
            count += 1
            negative -= 1
        else:
            break
    return judge_line(count, positive, negative, line)


def slant(row, line):
    color = map[row][line]
    r_positive = row + 1
    # 横向正方向 棋盘坐标向右
    r_negative = row - 1
    # 横向负方向 棋盘坐标向左
    l_positive = line + 1
    # 纵向正方向 棋盘坐标向下
    l_negative = line - 1
    # 纵向负方向 棋盘坐标向上
    right_count = 1
    left_count = 1
    if right_slant(r_negative, r_positive, l_positive, l_negative, color, right_count) or left_slant(
            r_negative, r_positive, l_positive, l_negative, color, left_count):
        return True


def judge_row(count, positive, negative, row):
    if count == 5:
        return True
    elif count == 4:
        if positive < 14 and negative > 0:
            if map[row][positive + 1] == 0 and \
                    map[row][negative - 1] == 0:
                return True
    else:
        return


def judge_line(count, positive, negative, line):
    if count == 5:
        return True
    elif count == 4:
        if positive < 14 and negative > 0:
            if map[positive + 1][line] == 0 and \
                    map[negative - 1][line] == 0:
                return True
    else:
        return


def right_slant(r_negative, r_positive, l_positive, l_negative, color, right_count):
    """
         判断方向 ： 右斜线-->左上至右下
    :param r_negative:
    :param r_positive:
    :param l_positive:
    :param l_negative:
    :param color:
    :param right_count:
    :return:
    """

    while r_negative > 0 and l_negative >= 0:
        # 判断落点左上方向
        if map[r_negative][l_negative] == color:
            right_count += 1
            r_negative -= 1
            l_negative -= 1
        else:
            break

    while r_positive <= 14 and l_positive <= 14:
        # 判断落点右下方向
        if map[r_positive][l_positive] == color:
            right_count += 1
            r_positive += 1
            l_positive += 1
        else:
            break
    return judge_right_slant(r_negative, r_positive, l_positive, l_negative, right_count)


def left_slant(r_negative, r_positive, l_positive, l_negative, color, left_count):
    """
        判断方向 ： 左斜线-->右上至左下
    :param r_negative:
    :param r_positive:
    :param l_positive:
    :param l_negative:
    :param color:
    :param left_count:
    :return:
    """
    while r_positive < 14 and l_negative >= 0:
        # 判断落点右上方向
        if map[r_positive][l_negative] == color:
            left_count += 1
            r_positive += 1
            l_negative -= 1
        else:
            break
    while r_negative >= 0 and l_positive <= 14:
        # 判断落点左下方向
        if map[r_negative][l_positive] == color:
            left_count += 1
            r_negative -= 1
            l_positive += 1
        else:
            break
    return judge_left_slant(r_negative, r_positive, l_positive, l_negative, left_count)


def judge_right_slant(r_negative, r_positive, l_positive, l_negative, count):
    if count == 5:
        return True
    elif count == 4:
        if (r_negative > 0 and r_positive < 14) or \
                (l_negative > 0 and l_positive < 14):
            if map[r_positive + 1][l_positive + 1] == 0 and \
                    map[r_negative - 1][l_negative - 1] == 0:
                return True
    else:
        return


def judge_left_slant(r_negative, r_positive, l_positive, l_negative, count):
    if count == 5:
        return True
    elif count == 4:
        if (r_negative > 0 and r_positive < 14) or \
                (l_negative > 0 and l_positive < 14):
            if map[r_positive + 1][l_negative - 1] == 0 and \
                    map[r_negative - 1][l_positive + 1] == 0:
                return True
    else:
        return


"""----------------------------------------界面--------------------------------------------"""


def canvas_set():  # 基础布局设置
    canvas = tk.Canvas(top, bg="#bbb", width=340, height=360)
    line_set(canvas)  # 网格线
    mark_set(canvas)  # 行列号
    handle_widget(canvas)  # 操作控件
    init_ovals(canvas)  # 棋子控件
    canvas.pack()


def line_set(canvas):
    for r in range(15):  # 横线
        canvas.create_line(x0, y0 + r * 20, 310, y0 + r * 20)
    for c in range(15):  # 竖线
        canvas.create_line(x0 + c * 20, y0, x0 + c * 20, 300)
    canvas.create_oval(x0 - 2 + 140, y0 - 2 + 140, x0 + 2 + 140, y0 + 2 + 140, fill="black")
    canvas.create_oval(x0 - 2 + 60, y0 - 2 + 60, x0 + 2 + 60, y0 + 2 + 60, fill="black")
    canvas.create_oval(x0 - 2 + 220, y0 - 2 + 60, x0 + 2 + 220, y0 + 2 + 60, fill="black")
    canvas.create_oval(x0 - 2 + 60, y0 - 2 + 220, x0 + 2 + 60, y0 + 2 + 220, fill="black")
    canvas.create_oval(x0 - 2 + 220, y0 - 2 + 220, x0 + 2 + 220, y0 + 2 + 220, fill="black")


def mark_set(canvas):
    for r in range(15):  # 横向
        text = str(r + 1)
        label_row = tk.Label(canvas, text=text, width=2, fg="blue", bg="#bbb", font=("Arial 10"))
        label_row.place(x=4, y=10 + r * 20)
    for c in range(15):  # 纵向
        text = str(c + 1)
        label_col = tk.Label(canvas, text=text, width=2, fg="blue", bg="#bbb", font=("Arial 10"))
        label_col.place(x=22 + c * 20, y=307)


def handle_widget(canvas):
    # 对手
    tk.Label(canvas, text="行", bg="#bbb").place(x=25, y=327)
    entry_adver_row_value = tk.StringVar()
    entry_adver_row_obj = tk.Entry(canvas, textvariable=entry_adver_row_value, font=("Arial 10"), width=2)
    entry_adver_row_obj.place(x=45, y=330)
    tk.Label(canvas, text="列", bg="#bbb").place(x=72, y=327)
    entry_adver_col_value = tk.StringVar()
    entry_adver_col_obj = tk.Entry(canvas, textvariable=entry_adver_col_value, font=("Arial 10"), width=2)
    entry_adver_col_obj.place(x=92, y=330)
    bt_adver = tk.Button(canvas, text="OK", font=("Arial 7 bold"), width=1, height=1,
                         command=lambda: oval_join_adver(entry_adver_row_obj, entry_adver_col_obj,
                                                         entry_adver_row_value, entry_adver_col_value))
    bt_adver.place(x=120, y=329)
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
                        command=lambda: oval_join_self(entry_self_row_obj, entry_self_col_obj,
                                                       entry_self_row_value, entry_self_col_value))
    bt_self.place(x=270, y=329)


def init_ovals(canvas):  # 初始化棋子界面
    for c in range(15):
        for r in range(15):  # 横向设置
            if map[c][r] == 1:
                canvas.create_oval(x0 - 7 + r * 20, y0 - 7 + c * 20, x0 + 7 + r * 20, y0 + 7 + c * 20, fill="black")
            if map[c][r] == 2:
                canvas.create_oval(x0 - 7 + r * 20, y0 - 7 + c * 20, x0 + 7 + r * 20, y0 + 7 + c * 20, fill="white")
    canvas.after(100, lambda: init_ovals(canvas))


def oval_join_adver(entry_obj_row, entry_obj_col, entry_info_row, entry_info_col):
    try:
        r = int(entry_obj_row.get()) - 1
        c = int(entry_obj_col.get()) - 1
    except ValueError:
        return
    else:
        if map[r][c] == 0:
            map[r][c] = 1
            if win(r, c):
                print("You Win!")
        entry_info_row.set("")
        entry_info_col.set("")


def oval_join_self(entry_obj_row, entry_obj_col, entry_info_row, entry_info_col):
    try:
        r = int(entry_obj_row.get()) - 1
        c = int(entry_obj_col.get()) - 1
    except ValueError:
        return
    else:
        if map[r][c] == 0:
            map[r][c] = 2
            if win(r, c):
                print("You Win!")
        entry_info_row.set("")
        entry_info_col.set("")


"""----------------------------------------启动--------------------------------------------"""


def main():
    init_map()  # 初始化map
    canvas_set()  # 基础布局设置
    top.mainloop()


if __name__ == '__main__':
    main()
