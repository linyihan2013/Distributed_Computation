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

def roles(arg):
    def _deco(func):
        arg1 = arg
        def __deco(self, *args, **kwargs):
            mode = self.get_secure_cookie("mode")
            if mode.decode() in arg1:
                func(self, *args, **kwargs)
            else:
                self.redirect("/")
        return __deco
    return _deco

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

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
        mode = self.get_argument("mode", "user")
        users = None
        if mode == "user":
            users = db.users
        elif mode == "admin":
            users = db.admins
        elif mode == "vip":
            users = db.vips
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
                self.set_secure_cookie("username", username)
                self.set_secure_cookie("mode", mode)
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
        self.render('index.html', user=self.current_user)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        self.clear_cookie("mode")
        global success
        success = True
        self.redirect("/")

class UserHandler(BaseHandler):
    @tornado.web.authenticated
    @roles(['admin', 'user'])
    def get(self):
        self.render('user.html', user=self.current_user)

class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    @roles(['admin'])
    def get(self):
        self.render('admin.html', user=self.current_user)

class VIPHandler(BaseHandler):
    @tornado.web.authenticated
    @roles(['vip'])
    def get(self):
        self.render('vip.html', user=self.current_user)

if __name__ == "__main__":
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login"
    }

    application = tornado.web.Application([
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/user', UserHandler),
        (r'/admin', AdminHandler),
        (r'/vip', VIPHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()