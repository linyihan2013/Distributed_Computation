__author__ = 'yihan'
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)

dic = {}

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", WordHandler)]
        fp = open('dict.txt', 'r+')
        try:
            text = fp.read()
            list1 = text.split("\n\n")
            for pair in list1:
                line = pair.split("\n")
                dic[line[0]] = line[1]
        finally:
            fp.close( )
        tornado.web.Application.__init__(self, handlers, debug=True)

class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        if word in dic.keys():
            pair = {}
            pair['word'] = word
            pair['definition'] = dic[word]
            self.write(pair)
        else:
            pair = {}
            pair['error'] = "word not found"
            self.write(pair)
            self.set_status(404)
    def post(self, word):
        definition = self.get_argument("definition")
        dic[word] = definition
        pair = {}
        pair['word'] = word
        pair['definition'] = definition
        self.write(pair)
        fp = open('dict.txt', 'a')
        try:
            text = "\n\n" + word + "\n" + definition
            fp.write(text)
        finally:
            fp.close( )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()