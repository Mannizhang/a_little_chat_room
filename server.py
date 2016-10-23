from tornado import websocket, web, ioloop,escape
import pymysql
import json

db = pymysql.connect("localhost", "root", "Ko007mysql.", "test", charset='utf8')


class MainHandler(web.RequestHandler):
    def get(self):
        self.render("client.html")


users = []


class SocketHandler(websocket.WebSocketHandler):
    def open(self):
        users.append(self)
        print("连接成功")

    def on_connection_close(self):
        print("关闭了")

    def on_message(self, message):
        print(message)
        for ws in users:
            ws.write_message(message)

    def on_finish(self):
        print("finish")

    def on_close(self):
        print("连接关闭")
        users.remove(self)


class registerHandler(web.RequestHandler):
    def post(self):
        data = escape.json_decode(self.request.body)
        # userName = self.request.body_arguments["userName"][0].decode("utf-8")
        # password = self.request.body_arguments["password"][0].decode("utf-8")
        insert_user(data["userName"], data["password"])
        result = {"code":0,"msg":"注册成功"}
        jsonString = json.dumps(result, ensure_ascii=False)
        self.write(jsonString)

class User(object):
    id = 0
    userName = ""
    password = ""

class login(web.RequestHandler):
    def post(self):
        userName = self.request.body_arguments["userName"][0].decode("utf-8")
        password = self.request.body_arguments["password"][0].decode("utf-8")
        user = select_user(userName, password)
        self.write(user.userName+":"+str(user.id))

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

    cursor.close()


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
        cursor.close()
        return user
    except:
        print("Error: unable to fecth data")
        return None

application = web.Application([
    (r"/", MainHandler),
    (r"/ws", SocketHandler),
    (r"/register", registerHandler),
    (r"/login",login),

])

if __name__ == "__main__":
    application.listen(9999)
    ioloop.IOLoop.instance().start()
