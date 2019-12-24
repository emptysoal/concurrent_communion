import tkinter as tk
import model

# list_record = [
#     ['Lily', 'victory', '2019-12-05 21:08:06'],
#     ['Lily', 'defeat', '2019-12-07 13:25:32']
# ]
list_record = []


def update_record(name):
    global list_record
    list_record = model.search_record(name)
    model.close_()


def generate_record(top, name):
    update_record(name)
    record_view = tk.Toplevel(top, width=400, height=300)
    record_view.title("Game Record")
    i = 1
    list_all_label = []
    for item in list_record:
        list_row_label = [tk.Label(record_view, text=str(i))]
        for element in item:
            label = tk.Label(record_view, text=element)
            list_row_label.append(label)
        list_all_label.append(list_row_label)
        i += 1
    create_head(record_view)
    show_record(list_all_label)


def create_head(record_view):
    tk.Label(record_view, text="No.").place(x=25, y=10)
    tk.Label(record_view, text="user").place(x=98, y=10)
    tk.Label(record_view, text="result").place(x=164, y=10)
    tk.Label(record_view, text="end time").place(x=260, y=10)


def show_record(list_all_label):
    for c in range(len(list_all_label)):
        for r in range(len(list_all_label[c])):
            list_all_label[c][r].place(x=30 + r * 65, y=40 + c * 30)


def main(name):
    top = tk.Tk()
    top.geometry("100x60")
    top.resizable(width=False, height=False)

    tk.Button(top, text="Click", command=lambda: generate_record(top, name)).pack()

    top.mainloop()


if __name__ == '__main__':
    main("Tom")
