import tornado.ioloop
import os, urllib
from urlparse import urlparse, parse_qs
import tornado.autoreload
import tornado.web
from neo_connector import NeoConnector
from tornado_json.routes import get_routes
from tornado_json.application import Application
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
    """The ol options routine for those times when Cross domain is not your friend"""
    def options(self):
        self.doRequest()
    """The ol get routine"""
    def get(self):
        self.doRequest()
   
    """make sure your origin header is allwoed to be sending data"""
    def check_allowed(domain):
        allowed = False
        for host in config.allowed_origins:
            if host in orig:
                allowed = True   
        return allowed
    
    """The meat"""   
    def doRequest(self):
        self.set_default_headers()
        url = self.request.uri
        if True:#check_allowed(orig):
            try:
                query = urlparse(urllib.unquote(url),allow_fragments=False ).query
                data = json.loads(query)
                nc = NeoConnector()
                nc.write_to_neo(data)
            except IOError as e:
                if debug:
                    print e
                self.write("nOK!")
            else:
                self.write("OK!")
    
     
class DashboardHandler(tornado.web.RequestHandler): 
    def get(self):
        self.write("coming soon");       

def make_app():
    tornado.autoreload.start()
    for dir, _, files in os.walk('.'):
        [tornado.autoreload.watch(dir + '/' + f) for f in files]
    return tornado.web.Application([
        (r"/lana.js", MainHandler),
        (r"/read.js", ReadJSHandler),
        (r"/lana/events", EventHandler),
        (r"/lana/visits", EventHandler),
        (r"/dashboard/", DashboardHandler),
        
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(config.service_port)
    tornado.ioloop.IOLoop.instance().start()
