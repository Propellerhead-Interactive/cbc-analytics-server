from py2neo import Graph, Path
import config


pw = config.neo4j_pw
host = config.neo4j_server

graph = Graph("http://neo4j:%s@%s:7474/db/data/"%(pw, host))

debug=False

class NeoConnector():
    def __init__(self):
        """just set it up yo"""
        
    def write_to_neo(self, data): 
        try:
            uid = data["id"] 
            visitor = data["visitor"]   #user - permenant cookie
            session = data["visit"]   #user - permenant cookie
            
            action = data["name"]
            timestamp = data["time"]
            url = data["properties"]["url"] #content
            
            
            title = data["properties"]["title"] #property of content
            
           
            contenttype =  data["properties"]["category"]["contenttype"] # LABEL ON CONTENT
            companies = data["properties"]["tagged"]["company"] # :TAGGED_C
            organizations = data["properties"]["tagged"]["organization"]  # :TAGGED_O
            locations = data["properties"]["tagged"]["location"]  # :TAGGED_L
            people = data["properties"]["tagged"]["person"]  # :TAGGED_P
            
            publicationDate = data["properties"]["publicationDate"] #  day-[:PART_OF] -> (month/year)
            
            tag = data["properties"]["tagged"]["tag"] #SUBJECT (  :TAGGED_S)
            
            contentarea =  data["properties"]["category"]["contentarea"] # :TAGEED_CAT
            category_ss1 = data["properties"]["category"]["subsection1"]  # :BELONGS_TO ->(contentarea)
            category_ss2 = data["properties"]["category"]["subsection2"] # :BELONGS_TO -> subsection1
            category_ss3 = data["properties"]["category"]["subsection3"] # :BELONGS_TO -> subsection2
            category_ss4 = data["properties"]["category"]["subsection4"] # :BELONGS_TO -> subsection3
            
            #READ AND VISITED ARE NOW  SEPARETE RELATIONSHIPS
            
            print visitor, action, timestamp, url, title, company, organization, tag, publicationDate
            print category_ss1, category_ss2, category_ss3, category_ss4


            #visitor / session
            tx = graph.cypher.begin()
            tx.append("merge (n:User { name:{visitor} }) return id(n) as nid",visitor=visitor )
            tx.append("merge (n:Sesson { id : {session} }) return id(n) as nid",session=session)
            result = tx.commit()
            #match user to session
            
            tx_user_session = graph.cypher.begin()
            ux = "MATCH (user:User {name:{visitor}}),(session:Session {name:{name}}) MERGE (user)-[r:STARTED]->(session)  RETURN r "
            tx_user_session.append(ux,  user_uid=visitor, visitor=visitor)
            cq = "MERGE (content:Content:{contenttype} { title:{title}, url:{url}, publicationdate:{publicationDate} }) return content;"
            tx_user_session.append(cq, contenttype=contenttype, url=url,title=title,publicationDate=publicationDate )
            tx_user_session.commit()
            
            
            r_tx = graph.cypher.begin()
            for location in locations:
                r_tx.append("MERGE (location:Location { name:{location} }) ;", location=location)
                r_tx.append("MATCH (content:Content{url:{url}}),(location:Location{name:{location}}) MERGE (content)-[k:TAGGED_L]->(location)  RETURN k;",location=location, url=url)
            for person in people:     
                r_tx.append("MERGE (person:Person { name:{person} }) return person;",person=person)
                r_tx.append("MATCH (content:Content{url:{url}}),(person:Person{name:{person}}) MERGE (content)-[k:TAGGED_P]->(person)  RETURN k;",person=person, url=url)
            for company in companies:
                r_tx.append( "MERGE (company:Company { name:{company} }) ;",company=company) 
                r_tx.append("MATCH (content:Content{url:{url}}),(company:Company { name:{company}}) MERGE (content)-[k:TAGGED_C]->(company)  RETURN k;",company=company, url=url)
                
            for organization in organizations:
                r_tx.append("MERGE (organization:Organization { name:{organization}}) ;", organization=organization)
                r_tx.append("MATCH (content:Content{url:{url}}),(organization:Organization { name:{organization}) MERGE (content)-[k:TAGGED_O]->(organization)  RETURN k;", organization=organization, url=url)
             r_tx.commit()
                
            
            
            
            #tx_categories = graph.cypher.begin()
            #MERGE (location:Location { name:"Toronto" }) ;

            #tx_categories.append()
            
            page_nid = result_page[0][0]["nid"]
            tx2 = graph.cypher.begin()
            if action=="read":
                tx2.append("MATCH (user:Person {name:{user_uid}}) , (p:Page { url : {url} })  MERGE (user)-[r:VISITED]->(p) RETURN id(r)", user_uid=visitor, url=url)
                tx2.append("MATCH (user:Person {name:{user_uid}})-[r:VISITED]->(p:Page { url : {url} }) SET r.read = true, r.last_read_time={lvt} RETURN id(r)", lvt=timestamp, user_uid=visitor, url=url)
            else:
                tx2.append("MATCH (user:Person {name:{user_uid}}) , (p:Page { url : {url} })  MERGE (user)-[r:VISITED]->(p) RETURN id(r)",user_uid=visitor, url=url)
                tx2.append("MATCH (user:Person {name:{user_uid}})-[r:VISITED]->(p:Page { url : {url} }) SET r.read = true, r.last_read_time={lvt} RETURN id(r)", lvt=timestamp, user_uid=visitor, url=url)
        
            result_visited = tx2.commit()
            tx2 = graph.cypher.begin()
            for c2 in category:
                tx2.append("merge (n:Category { name : {name} }) return id(n) as nid",name=c2 )
            result_cat = tx2.commit()
            tx3 = graph.cypher.begin()
            for c in category:
                tx3.append("MATCH (n:Category { name : {name} }) , (p:Page { url : {url} })  MERGE (n)<-[r:BELONGS]-(p) RETURN id(r)", name=c, url=url)
            z = tx3.commit()
        except IOError as e:
            if debug:
                print e
            return False
        else:
            return True
 