from tornado import websocket, web, ioloop


class MainHandler(web.RequestHandler):
    def get(self):
        self.render("client.html")


class SocketHandler(websocket.WebSocketHandler):

    def open(self):
        print("连接成功")

    def on_connection_close(self):
        print("关闭了")

    def on_message(self, message):
        print(message)
        self.write_message(message)

    def on_finish(self):
        print("finish")

    def on_close(self):
        print("连接关闭")


application = web.Application([
    (r"/", MainHandler),
    (r"/ws", SocketHandler),
])

if __name__ == "__main__":
    application.listen(9999)
    ioloop.IOLoop.instance().start()
