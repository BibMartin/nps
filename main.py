import tornado.web
import tornado.wsgi
import wsgiref.simple_server
import os
import json

_DATA_FILE = 'data.json'

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world\n")

class Data(object):
    def __init__(self, filename):
        self._filename = filename

    def _read_data(self):
        try:
            fid = open(self._filename)
        except FileNotFoundError as e:
            open(self._filename, 'w').write('{}')
            fid = open(self._filename)
        return json.load(fid)

    def get(self, key, default=0):
        data = self._read_data()
        return data.get(key, default)

    def set(self, key, value):
        data = self._read_data()
        data[key] = value
        json.dump(data, open(self._filename, 'w'))

    def incr(self, key, default=0):
        data = self._read_data()
        data[key] = data.get(key, default) + 1
        json.dump(data, open(self._filename, 'w'))
        return data[key]


class ByColor(tornado.web.RequestHandler):
    def get(self, color):
        color = color.lower()
        if color not in ['green', 'yellow', 'orange', 'red']:
            raise tornado.web.HTTPError(400, reason='Unknown color {}'.format(color))
        value = Data(_DATA_FILE).get(color)
        self.write("{} : {}\n".format(color, value))
    def post(self, color):
        color = color.lower()
        if color not in ['green', 'yellow', 'orange', 'red']:
            raise tornado.web.HTTPError(400, reason='Unknown color {}'.format(color))
        value = Data(_DATA_FILE).incr(color)
        self.write("{} : {}\n".format(color, value))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/byColor/(.*?)", ByColor),
    ])

if __name__ == "__main__":
    wsgi_app = tornado.wsgi.WSGIAdapter(application)
    server = wsgiref.simple_server.make_server('', 8888, wsgi_app)
    server.serve_forever()
