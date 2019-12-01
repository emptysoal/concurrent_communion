"""
    简单模拟服务器，测试客户端用
"""
from socket import *
from select import select

sockfd = socket(AF_INET, SOCK_STREAM)
sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockfd.bind(("127.0.0.1", 32802))
sockfd.listen(5)
print("Listen the port:", 32802)

# 创建监控对象
rlist = [sockfd]
wlist = []
xlist = []

dict_base_info = {"Tom":"123"}


def handle(connfd):
    request = connfd.recv(1024).decode()
    # print(request)
    if not request:
        rlist.remove(connfd)
        connfd.close()
        return
    if request.split(" ")[0] == "R":
        name = request.split(" ")[1]
        password = request.split(" ")[2]
        register(connfd, name, password)
    elif request.split(" ")[0] == "E":
        name = request.split(" ")[1]
        password = request.split(" ")[2]
        entry(connfd, name, password)
    elif request.split(" ")[0] == "C":
        name = request.split(" ")[1]
        content = request.split(" ", 2)[2]
        print(("%s: %s" % (name, content)))
        connfd.send(b"the msg you send was received")


def entry(connfd, name, password):
    try:
        if dict_base_info[name] == password:
            response = "OK"
        else:
            response = "name or password Error, please check or sign up again"
    except:
        response = "name or password Error, please check or sign up again"
    connfd.send(response.encode())


def register(connfd, name, password):
    for user in dict_base_info:
        if user == name:
            response = "The name has already been used"
            break
    else:
        response = "OK"
        dict_base_info[name] = password  # 注册请求处理
    connfd.send(response.encode())


# 循环阻塞等待IO发生
while True:
    try:
        rs, ws, xs = select(rlist, wlist, xlist)
        for r in rs:
            if r is sockfd:
                connfd, addr = r.accept()
                print("Connect from :", addr)
                rlist.append(connfd)
            else:
                handle(r)
                # data = r.recv(1024).decode()
                # if not data:
                #     rlist.remove(r)
                #     r.close()
                #     continue
                # print("Receive:", data)
                # r.send(b"OK")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        continue
