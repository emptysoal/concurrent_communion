"""
    项目数据处理，主要负责数据写入和读取
"""
import pymysql


class DataManager:
    def __init__(self, host="localhost", port=3306, user=None, password=None, database=None, charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        # 连接数据库
        self.__db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                    database=self.database, charset=self.charset)
        self.__cur = None

    def create_cur(self):
        # 创建游标对象
        self.__cur = self.__db.cursor()

    def close(self):
        if self.__cur:
            self.__cur.close()
        self.__db.close()

    def regster_deal(self, user, passwd):
        """
            注册处理
        :param user: 注册的用户名
        :param passwd: 注册的密码
        :return: False则未注册成功；True则注册成功，并将信息写入数据库
        """
        # if not self.__judge_user(user):  # 用户名不可用
        #     return False
        sql = "insert into base_info(name,password) values(%s,%s);"
        try:
            self.__cur.execute(sql, [user, passwd])
            self.__db.commit()
        except Exception as e:
            print(e)
            self.__db.rollback()
            return False
        else:
            return True

    def judge_user(self, user):
        """
            判断用户名是否重复，是返回False(注册的用户名不可用)，否返回True(注册的用户名可用)
        :param user: 注册的用户名
        :return: True(用户名可用) or False（用户名不可用）
        """
        sql = "select name from base_info where name='%s';" % user
        self.__cur.execute(sql)
        return not self.__cur.fetchone()

    def login_deal(self, user, passwd):
        """
            判断登录用户名和密码是否正确
        :param user: 登录的用户名
        :param passwd: 登录的密码
        :return: False则登录失败；True则登录验证成功
        """
        sql = "select name,password from base_info where name=%s and password=%s;"
        self.__cur.execute(sql, [user, passwd])
        return self.__cur.fetchone()

    def update_chat(self, name, content):
        """
            将用户名和相应聊天内容更新到数据表chat_history中
        :param name: 发消息者的用户名
        :param content: 所发送的消息内容
        """
        sql = "insert into chat_history(name,content) values(%s,%s);"
        try:
            self.__cur.execute(sql, [name, content])
            self.__db.commit()
        except Exception as e:
            self.__db.rollback()
            return False
        else:
            return True

    def is_file_exist(self, file_name):
        """
            判断传入的文件名是否已经存在
        :param file_name: 外界传入的文件名称
        :return: True表示已经存在,False表示不存在
        """
        sql = "select file_name from file_put_record where file_name='%s';" % file_name
        self.__cur.execute(sql)
        return self.__cur.fetchone() is not None

    def update_file_put(self, name, file_name):
        """
            将用户名和文件名称更新到数据表file_put_record
        :param name: 上传文件者的用户名
        :param file_name: 上传文件的文件名称
        """
        sql = "insert into file_put_record(name,file_name) values(%s,%s);"
        try:
            self.__cur.execute(sql, [name, file_name])
            self.__db.commit()
        except Exception as e:
            self.__db.rollback()
            return False
        else:
            return True

    def update_game_info(self, name, result):
        """
            将用户名和游戏结果更新到数据表game_record
        :param name: 游戏者的用户名
        :param result: 游戏结果
        """
        pass


if __name__ == '__main__':
    data_manager = DataManager("localhost", 3306, "root", "123456", "concurrent_communion", "utf8")
    data_manager.create_cur()
    print(data_manager.is_file_exist("test.txt"))
