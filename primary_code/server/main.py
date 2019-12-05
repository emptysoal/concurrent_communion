"""
    服务器程序入口
"""
import chat_server
import configure_server as config


class MainServer:
    def main(self):
        host = config.HOST
        port = config.PORT
        server = chat_server.ChatServer(host, port)
        server.serve_forever()


if __name__ == '__main__':
    main_obj = MainServer()
    main_obj.main()
