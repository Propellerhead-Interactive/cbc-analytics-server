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
import datetime
from decimal import *


getcontext().prec = 2
debug=True
static_path= os.path.join(os.path.dirname(__file__), "web")

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
        start_time = datetime.datetime.now()

        self.set_default_headers()
        url = self.request.uri
        try:
            query = urlparse(urllib.unquote(url),allow_fragments=False).query
            data = json.loads(query)

            z = NeoConnector().write_to_neo(data)
            #yield gen.Task(self.dosomething, data)

            end_time = datetime.datetime.now()
            time_diff = end_time - start_time
            print time_diff
        except IOError as e:
            print e
            self.write("nOK!")
        else:


            self.write("OK! %s MS" % time_diff)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hi!");


class DashboardHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            self.set_default_headers()
            self.set_header('Content-type', 'text/html')
            users, content, sessions, loads, reads, categories, sessionCounts, todayCounts, totalSessionCounts, top_read = NeoConnector().read_stats(1)

            l =  int(loads[0][0])
            if l ==0:
                pct=0
            else:
                pct=int(reads[0][0])/int(loads[0][0])

            self.render("dashboard.html", categories= categories, users=users[0][0], content=content[0][0], sessions=sessions[0][0], readpct=pct)
        except IOError as e:
            print e[1]
            self.write("WHU?!")



class PrettyDashboardHandler(tornado.web.RequestHandler):


    def get(self):
        try:
            self.set_default_headers()
            self.set_header('Content-type', 'text/html')

            try:
                url = self.request.uri
                query = urlparse(urllib.unquote(url),allow_fragments=False).query
                days = int(query.split("t=")[1])
                print days
                if days==0:
                    days=5
            except (IndexError, IOError) as e:
                print e
                days = 5
                pass

            users, content, sessions, loads, reads, categories, sessionCounts, todayCounts, totalSessionCounts, top_read = NeoConnector().read_stats(days)

            l =  int(loads[0][0])
            if l ==0:
                pct=0
            else:
                pct=round(Decimal(float(reads[0][0])/float(loads[0][0]))*100,2)

            now = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

            self.render("dashboard_n.html",now = now,reads=reads,top_read=top_read, loads=loads, totalSessionCounts=totalSessionCounts,todayCounts=todayCounts, visits = loads,categories= categories, users=users[0][0], content=content[0][0], sessions=sessions[0][0], readpct=pct, sessionCounts = sessionCounts)
        except IOError as e:
            print e[1]
            self.write("WHU?!")

class DataHandler(tornado.web.RequestHandler):

    def get(self, param1):
        self.set_default_headers()
        self.set_header('Content-type', 'application/json')
        days = 5
        self.write(json.dumps(NeoConnector().read_stats(days)[0][1]))



def make_app():

    #tornado.autoreload.start()
    for dir, _, files in os.walk('.'):
        [tornado.autoreload.watch(dir + '/' + f) for f in files]


    settings = {
                "debug": True,
            }
    app = tornado.web.Application([
        (r"/lana.js", MainHandler),
        (r"/read.js", ReadJSHandler),
        (r"/lana/events", EventHandler),
        (r"/lana/visits", EventHandler),
        (r"/", IndexHandler),
        (r"/dboard", DashboardHandler),
        (r"/pboard", PrettyDashboardHandler),
        (r"/data/(.*)", DataHandler),

        (r'/static/(.*)', tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "static"))),

    ])
    app.settings = settings
    return app

if __name__ == "__main__":
    app = make_app()
    for dir, _, files in os.walk('.'):
        [tornado.autoreload.watch(dir + '/' + f) for f in files]

    server = HTTPServer(app)
    server.bind(8888)
    server.start(4)
    tornado.ioloop.IOLoop.instance().start()
