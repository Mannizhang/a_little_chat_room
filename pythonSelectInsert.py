#encoding=utf-8

import pymysql


db = pymysql.connect("localhost", "root", "Ko007mysql.", "test", charset='utf8')


class User(object):
    id = 0
    userName = ""
    password = ""


def select_user(name, password):
    cursor = db.cursor()

    sql = "SELECT id,userName FROM user WHERE userName='%s' AND password ='%s'" % (name, password)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()
        user = User()
        user.id = int(results[0])
        user.userName = results[1]
        db.close()
        return user
    except:
        print("Error: unable to fecth data")
        return None

def insert_user(name, password):

    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO user(userName,password) VALUES ('%s', '%s')" % (name, password)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print("error")

    db.close()

#insert_user("zhangsan","123456")
user = select_user("zmy","123456")
print(user.userName)