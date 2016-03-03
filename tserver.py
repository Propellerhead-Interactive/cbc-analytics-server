import tornado.ioloop
import os, urllib
from urlparse import urlparse, parse_qs
import tornado.autoreload
import tornado.web
from tornado_json.routes import get_routes
from tornado_json.application import Application
import json
import config
from neo_connector import NeoConnector

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 3600)
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        self.set_header('Content-type', 'application/json')

class MainHandler(BaseHandler):
    def get(self):
        self.set_default_headers()
        self.render("anal.js")

class ReadJSHandler(BaseHandler):
    def get(self):
        self.set_default_headers()
        self.render("read.js")
        
class EventHandler(BaseHandler):
    def options(self):
        self.doRequest()
    def get(self):
        self.doRequest()
        
    #def allowRequest(uri):
     #   if self.request.
        
        
    def doRequest(self):
        self.set_default_headers()
        #print self.request.uri
        url = self.request.uri
        orig =  self.request.headers["origin"]
        allowed = False
        for host in config.allowed_origins:
            if host in orig:
                allowed = True
        if allowed:
            print "allowed"
            query = urlparse(urllib.unquote(url),allow_fragments=False ).query
            data = json.loads(query)
            print data
            nc = NeoConnector()
            nc.write_to_neo(data)
        
        self.write("OK!")
    
     
class DashboardHandler(tornado.web.RequestHandler): 
    def get(self):
        self.write("coming soon");       

        
class NothingHandler(tornado.web.RequestHandler):        
    def get(self):
        jsonData = request.get_json()
        if "url" in jsonData[0]:
            userid = jsonData[0]["id"]
            name = jsonData[0]["name"]
            time = jsonData[0]["time"]
            props = jsonData[0]["properties"]
            url= props["url"]
            title= props["title"]
            return name +""+ str(time) +""+ userid
        else:
            return jsonData
        
        

def make_app():
    
    
    tornado.autoreload.start()
    for dir, _, files in os.walk('.'):
        [tornado.autoreload.watch(dir + '/' + f) for f in files]
    
    return tornado.web.Application([
        (r"/anal.js", MainHandler),
        (r"/read.js", ReadJSHandler),
        (r"/anal/events", EventHandler),
        (r"/anal/visits", EventHandler),
        (r"/dashboard/", DashboardHandler),
        
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()