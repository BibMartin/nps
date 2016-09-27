import tornado.web
import tornado.wsgi
import wsgiref.simple_server
import os
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world\n")


class ByColor(tornado.web.RequestHandler):
    def get(self, color):
        color = color.lower()
        if color not in ['green', 'yellow', 'orange', 'red']:
            raise tornado.web.HTTPError(400, reason='Unknown color {}'.format(color))
        data = json.load(open('./data.json'))
        self.write("{} : {}\n".format(color, data.get(color, 0)))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/byColor/(.*?)", ByColor),
    ])

if __name__ == "__main__":
    wsgi_app = tornado.wsgi.WSGIAdapter(application)
    server = wsgiref.simple_server.make_server('', 8888, wsgi_app)
    server.serve_forever()
