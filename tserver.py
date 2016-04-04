import tornado.ioloop
import os, urllib
from urlparse import urlparse, parse_qs
import tornado.autoreload
import tornado.web
from neo_connector import NeoConnector
from tornado_json.routes import get_routes
from tornado_json.application import Application
from tornado import gen
from tornado import ioloop as IOLoop
from tornado.httpserver import HTTPServer
import json
import config

debug=True

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 3600)
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        

class MainHandler(BaseHandler):
    def get(self):
        self.set_default_headers()
        self.set_header('Content-type', 'application/json')
        self.render("lana.js")

class ReadJSHandler(BaseHandler):
    def get(self):
        self.set_default_headers()
        self.set_header('Content-type', 'application/json')
        self.render("read.js")
        
class EventHandler(BaseHandler):
    def options(self):
        self.doRequest()
    
    def get(self):
        self.doRequest()
   
    """The meat"""   
    def dosomething(self, data, callback):
        z = NeoConnector().write_to_neo(data)
        print "performing NEO write"
        return callback(z)
            
    def doRequest(self):
        self.set_default_headers()
        url = self.request.uri
        print url
        try:
            query = urlparse(urllib.unquote(url),allow_fragments=False).query
            data = json.loads(query)
            
            z = NeoConnector().write_to_neo(data)
            #yield gen.Task(self.dosomething, data)
        except IOError as e:
            print e
            self.write("nOK!")
        else:
           
            self.write("OK!")

     
class DashboardHandler(tornado.web.RequestHandler): 
    def get(self):
        self.write("Hi!");       

def make_app():
    #tornado.autoreload.start()
    for dir, _, files in os.walk('.'):
        [tornado.autoreload.watch(dir + '/' + f) for f in files]
    return tornado.web.Application([
        (r"/lana.js", MainHandler),
        (r"/read.js", ReadJSHandler),
        (r"/lana/events", EventHandler),
        (r"/lana/visits", EventHandler),
        (r"/", DashboardHandler),
        
    ])

if __name__ == "__main__":
    app = make_app()
    server = HTTPServer(app)
    server.bind(8888)
    server.start(4)
    tornado.ioloop.IOLoop.instance().start()
    
