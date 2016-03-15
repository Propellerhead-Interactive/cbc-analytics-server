from py2neo import Graph, Path
import config


pw = config.neo4j_pw
host = config.neo4j_server

graph = Graph("http://neo4j:%s@%s:7474/db/data/"%(pw, host))

class NeoConnector():
    def __init__(self):
        """just set it up yo"""
        
    def write_to_neo(self, data): 
        uid = data["id"] 
        visitor = data["visitor"] 
        
        action = data["name"]
        url = data["properties"]["url"]
        title = data["properties"]["title"]
        category = data["properties"]["category"]
        
   
        tx = graph.cypher.begin()
        tx.append("merge (n:Person { name:{visitor} }) return id(n) as nid",visitor=visitor )
        result = tx.commit()
        user_nid = result[0][0]["nid"]
        tx2 = graph.cypher.begin()
        tx2.append("merge (n:Page { url : {url} , title: {title}}) return id(n) as nid",url=url, title=title )
        result_page = tx2.commit()
        page_nid = result_page[0][0]["nid"]
        tx2 = graph.cypher.begin()
        if action=="read":
            tx2.append("MATCH (user:Person {name:{user_uid}}) , (p:Page { url : {url} })  MERGE (user)-[r:VISITED]->(p) SET r.read = true RETURN id(r)", user_uid=visitor, url=url)
            
        else:
            tx2.append("MATCH (user:Person {name:{user_uid}}) , (p:Page { url : {url} })  MERGE (user)-[r:VISITED]->(p) RETURN id(r)", user_uid=visitor, url=url)
        
        result_visited = tx2.commit()
        tx2 = graph.cypher.begin()
        for c2 in category:
            tx2.append("merge (n:Category { name : {name} }) return id(n) as nid",name=c2 )
        result_cat = tx2.commit()
        tx3 = graph.cypher.begin()
        for c in category:
            tx3.append("MATCH (n:Category { name : {name} }) , (p:Page { url : {url} })  MERGE (n)<-[r:BELONGS]-(p) RETURN id(r)", name=c, url=url)
        z = tx3.commit()
 