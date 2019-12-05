"""
    客户端入口
"""
import ui


class MainClient:
    def main(self):
        client = ui.ClientUI()
        client.run()


if __name__ == '__main__':
    client = MainClient()
    client.main()
