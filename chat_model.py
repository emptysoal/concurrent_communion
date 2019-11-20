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
        if not self.__judge_user(user):  # 用户名不可用
            return False
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

    def __judge_user(self, user):
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


if __name__ == '__main__':
    data_manager = DataManager("localhost", 3306, "root", "123456", "concurrent_communion", "utf8")
    data_manager.create_cur()
