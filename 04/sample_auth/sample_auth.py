__author__ = 'yihan'
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import pymongo
import hashlib

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

success = True

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_cookie("username")

class LoginHandler(BaseHandler):
    def get(self):
        global success
        if success:
            self.render('login.html')
        else:
            self.render('login2.html')

    def post(self):
        global success
        conn = pymongo.MongoClient()
        db = conn.example
        users = db.users
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        if username and password:
            m = hashlib.md5()
            m.update(password.encode())
            cursor = users.find({"name": username, "password": m.hexdigest()})
            count = 0
            for doc in cursor:
                count += 1
            if count:
                success = True
                self.set_cookie("username", username)
                self.redirect("/")
            else:
                success = False
                self.redirect("/login")
        else:
            success = False
            self.redirect("/login")

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.current_user == "zixuan":
            self.render('vip.html', user=self.current_user)
        elif self.current_user == "yihan":
            self.render('admin.html', user=self.current_user)
        else:
            self.render('index.html', user=self.current_user)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        global success
        success = True
        self.redirect("/")

if __name__ == "__main__":
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        #"cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": False,
        "login_url": "/login"
    }

    application = tornado.web.Application([
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()