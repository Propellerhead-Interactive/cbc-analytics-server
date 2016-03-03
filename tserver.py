import tornado.ioloop
import os, urllib
from urlparse import urlparse, parse_qs
import tornado.autoreload
import tornado.web
from tornado_json.routes import get_routes
from tornado_json.application import Application
import json
from py2neo import Graph, Path

graph = Graph("http://neo4j:neo4j@192.168.99.100:7474/db/data/")

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
        
    def doRequest(self):
        self.set_default_headers()
        #print self.request.uri
        url = self.request.uri
        query = urlparse(urllib.unquote(url) ).query
        data = json.loads(query)
        print data
        self.write_to_neo(data)
        self.write("OK")
    
    def write_to_neo(self, data): 
        uid = data["id"] 
        action = data["name"]
        url = data["properties"]["url"]
        title = data["properties"]["title"]
        category = data["properties"]["category"]
   
        tx = graph.cypher.begin()
        tx.append("merge (n:Person { uid : {uid}, name:{uid} }) return id(n) as nid",uid=uid )
        result = tx.commit()
        user_nid = result[0][0]["nid"]
        tx2 = graph.cypher.begin()
        tx2.append("merge (n:Page { url : {url} , title: {title}}) return id(n) as nid",url=url, title=title )
        result_page = tx2.commit()
        page_nid = result_page[0][0]["nid"]
        tx2 = graph.cypher.begin()
        if action=="read":
            tx2.append("MATCH (user:Person {uid:{user_uid}}) , (p:Page { url : {url} })  MERGE (user)-[r:READ]->(p) RETURN id(r)", user_uid=uid, url=url)
        
        else:
            tx2.append("MATCH (user:Person {uid:{user_uid}}) , (p:Page { url : {url} })  MERGE (user)-[r:VISITED]->(p) RETURN id(r)", user_uid=uid, url=url)
        
        result_visited = tx2.commit()
        tx2 = graph.cypher.begin()
        tx2.append("merge (n:Category { name : {name} }) return id(n) as nid",name=category )
        result_cat = tx2.commit()
        tx3 = graph.cypher.begin()
        tx3.append("MATCH (n:Category { name : {name} }) , (p:Page { url : {url} })  MERGE (n)<-[r:BELONGS]-(p) RETURN id(r)", name=category, url=url)
        z = tx3.commit()
      
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