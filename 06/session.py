__author__ = 'yihan'
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import hashlib
import pymongo
import redis
import uuid

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

success = True
session_secret = "3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc"
id = hashlib.sha256(session_secret + str(uuid.uuid4()))
id = id.hexdigest()
Redis = redis.StrictRedis()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        #return self.get_secure_cookie("username")
        myapp =  self.get_secure_cookie("myapp_session")
        return Redis.hget(myapp, "username")

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
                #self.set_secure_cookie("username", username)
                myapp =  self.get_secure_cookie("myapp_session")
                Redis.hset(myapp, "username", username)
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
        #self.clear_cookie("username")
        myapp = self.get_secure_cookie("myapp_session")
        Redis.hset(myapp, "username", None)
        global success
        success = True
        self.redirect("/")

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
        (r'/logout', LogoutHandler)
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()