# -*- coding: utf-8 -*-
import os.path
from tornado import httpserver,ioloop,web
from tornado.options import define,options
import torndb
import tornado.options
from handlers import HANDLERS,TEMPLATE_PATH

# 定义数据库初始化配置
define("port", default=8000, type=int)
define("mysql_host",default="127.0.0.1:3306",help="blog database host")
define("mysql_database",default="project",help="blog database name")
define("mysql_user",default="root",help="blog database user")
# define("mysql_password",default="",help="blog database password")


class Application(web.Application):
    def __init__(self):
        handlers = HANDLERS
        settings = dict(
            # 模板路径
            template_path = TEMPLATE_PATH,
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # 防跨站攻击的设置
            xsrf_cookies = False,
            # 就是cookie的密钥，是根据py一个小算法"base64"获得的
            # cmd python：print base64.b64encode(uuid.uuid4().bytes+uuid.uuid4().bytes)
            cookie_secret="tmxvMsfgRHqV61E6iZ/pJcVRAiHQZEmehIFLhNJtvYM=",
        )
        # Application初始化
        web.Application.__init__(self,handlers,**settings)
        # db链接,App init时会紧接着做
        self.db = torndb.Connection(
            host= options.mysql_host,database=options.mysql_database,
            user= options.mysql_user,password=None)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()