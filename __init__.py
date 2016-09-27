import tornado.web
import tornado.wsgi
import wsgiref.simple_server
import os
import json

_DATA_FILE = 'data.json'
path = os.path.abspath(os.path.dirname(__file__))
static_path = os.path.join(path, 'static')


class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.redirect('static/index.html', self.request.uri)
        raise tornado.web.Finish()

class Data(object):
    def __init__(self, filename):
        self._filename = filename

    def get_all(self):
        try:
            fid = open(self._filename)
        except FileNotFoundError as e:
            open(self._filename, 'w').write('{}')
            fid = open(self._filename)
        return json.load(fid)

    def get(self, key, default=0):
        data = self.get_all()
        return data.get(key, default)

    def set(self, key, value):
        data = self.get_all()
        data[key] = value
        json.dump(data, open(self._filename, 'w'))

    def incr(self, key, default=0):
        data = self.get_all()
        data[key] = data.get(key, default) + 1
        json.dump(data, open(self._filename, 'w'))
        return data[key]


class ByColor(tornado.web.RequestHandler):
    def get(self, color):
        color = color.lower()
        if color not in ['green', 'yellow', 'orange', 'red']:
            raise tornado.web.HTTPError(400, reason='Unknown color {}'.format(color))
        value = Data(_DATA_FILE).incr(color)
        self.write(('<center>'
                    '<h2>You have voted:</h2>'
                    '<img src="../static/img/{}.png"/><br>'
                    '<h2>Thanks for your feedback.</h2>'
                    '</center>'
                    ).format(color))


class All(tornado.web.RequestHandler):
    def get(self):
        value = Data(_DATA_FILE).get_all()
        self.write("{}\n".format(value))

application = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/all", All),
    (r"/byColor/(.*?)", ByColor),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
    ])

if __name__ == "__main__":
    wsgi_app = tornado.wsgi.WSGIAdapter(application)
    server = wsgiref.simple_server.make_server('', 8888, wsgi_app)
    server.serve_forever()
