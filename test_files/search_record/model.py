"""
    调用数据库
"""
import pymysql

db = None
cur = None


def search_record(name):
    global db
    db = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                         password="123456", database="concurrent_communion", charset="utf8")

    global cur
    cur = db.cursor()

    sql = "select name,result,start_time from game_record where name = '%s' limit 10;" % name
    cur.execute(sql)
    re = list(cur.fetchall())
    list_record = []
    for item in re:
        list_record.append((item[0], item[1], "%s" % item[2]))
    return list_record


def close_():
    cur.close()
    db.close()


if __name__ == '__main__':
    print(search_record("Lily"))
    close_()
