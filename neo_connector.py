from py2neo import Graph, Path
import config
import datetime


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
            
            visit_timestamp = visitor.split("-")[0]
            
            session = data["visit"]   #user - permenant cookie
            
            action = data["name"]
            timestamp = data["time"]
            url = data["properties"]["url"] #content
            
            
            title = data["properties"]["title"] #property of content
            
           
            contenttype =  data["properties"]["category"]["contenttype"] # LABEL ON CONTENT
            companies =  []
            organizations = []
            locations = []
            people = []
            tags = []
            
            if "company" in data["properties"]["tagged"]:
                companies = data["properties"]["tagged"]["company"] # :TAGGED_C
            if "organization" in data["properties"]["tagged"]:
                organizations = data["properties"]["tagged"]["organization"]  # :TAGGED_O
            if "location" in data["properties"]["tagged"]:
                locations = data["properties"]["tagged"]["location"]  # :TAGGED_L
            if "people" in data["properties"]["tagged"]:
                people = data["properties"]["tagged"]["person"]  # :TAGGED_P
            if "tag" in data["properties"]["tagged"]:
                tags = data["properties"]["tagged"]["tag"] #SUBJECT (  :TAGGED_S)
            
            publicationDate = data["properties"]["publicationDate"] #  day-[:PART_OF] -> (month/year)
            
            
           
            #READ AND VISITED ARE NOW  SEPARETE RELATIONSHIPSc
          
            #print category_ss1, category_ss2, category_ss3, category_ss4

            #figure out the dates
            publicationDateParts = datetime.datetime.utcfromtimestamp((float(publicationDate)/1000))
            pd_ym = "%s%s" % (publicationDateParts.year , publicationDateParts.month )
            pd_dd = str(publicationDateParts.day).zfill(2)
            pd_ymd = "%s%s" % (pd_ym, pd_dd)
            
            timeStampParts = datetime.datetime.utcfromtimestamp(float(visit_timestamp)/1000)
            ts_ym = "%s%s" % (timeStampParts.year , timeStampParts.month )
            ts_dd = str(timeStampParts.day).zfill(2)
            ts_ymd = "%s%s" % (pd_ym, pd_dd)
            
         
            tx_dates = graph.cypher.begin()
            
            #tx_dates.append("MATCH (m) detach delete m;")
            
            d11 = "MERGE (year_month:Year_Month {id:{ym}});"
            d12 = "MERGE (day:Day {day:{dd},date:{ymd} });"
            d13 = "MATCH (year_month:Year_Month {id:{ym}}),(day:Day {date:{ymd}}) MERGE (year_month)-[:PART_OF]->(day);"
            
            
            tx_dates.append(d11, ym=pd_ym)
            tx_dates.append(d12, ymd = pd_ymd, dd=pd_dd)
            tx_dates.append(d13, ym=pd_ym, ymd=pd_ymd)
            
            tx_dates.append(d11, ym=ts_ym)
            tx_dates.append(d12, ymd = ts_ymd, dd = ts_dd)
            tx_dates.append(d13, ym=ts_ym, ymd=ts_ymd)
            tx_dates.commit()
            
            tx = graph.cypher.begin()
            tx.append("merge (n:User { name:{visitor} }) return id(n) as nid",visitor=visitor )
            tx.append("merge (n:Session { id : {session} }) return id(n) as nid",session=session)
            
            
            tx.append("MATCH (m:Session { id : {session} }),(n:User { name:{visitor} }) MERGE (n)-[:STARTED]->(m)",visitor=visitor ,session=session)
            
            
            result = tx.commit()

            #match user to session
            
            tx_user_session = graph.cypher.begin()
            
            ux = "MATCH (user:User {name:{visitor}}),(session:Session {id:{name}}) MERGE (user)-[r:STARTED]->(session)  RETURN r "
            tx_user_session.append(ux,  name=session, visitor=visitor)
            cq = "MERGE (content:Content { name:{title}, url:{url}, publicationDate:{publicationDate} }) return content;"
            cq_label  = "MATCH (n:Content {url:{url}}) set n :%s " % contenttype
            
            tx_user_session.append(cq,url=url,title=title,publicationDate=publicationDate )
            tx_user_session.append(cq_label,url=url)
            tx_user_session.append("MATCH (day:Day {date:{pd_ymd}}), (content:Content{url:{url}}) MERGE (content)-[:PUBLISHED]-(day);", url=url, pd_ymd=pd_ymd)
            tx_user_session.append("MATCH (session:Session { id:{session} } ), ( day:Day { date:{ts_ymd} } ) MERGE (session)-[:INITIATED]->(day)", session=session, ts_ymd=ts_ymd )
            
            #check for load type (read, visited)
            if action=="load":
                tx_user_session.append("MATCH (m:Session { id : {session} }),(n { url:{url} }) MERGE (m)-[:LOADED]->(n)",url=url ,session=session)
            else:
                tx_user_session.append("MATCH (m:Session { id : {session} }),(n { url:{url} }) MERGE (m)-[:VISITED]->(n)",url=url ,session=session)
                
            tx_user_session.commit()
            
            #usersession connect to 
            
            
            
            
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
                r_tx.append("MATCH (content:Content {url:{url} }),(organization:Organization { name:{organization}}) MERGE (content)-[k:TAGGED_O]->(organization)  RETURN k;", organization=organization, url=url)
            for tag in tags:
                r_tx.append("MERGE (subject:Subject { name:{tag}})", tag=tag)
                r_tx.append("MATCH (content:Content{url:{url}}),(subject:Subject { name:{tag}}) MERGE (content)-[k:TAGGED_S]->(subject)", tag=tag, url=url)
            
            r_tx.commit()
            
            tx_categories = graph.cypher.begin()
            categories = data["properties"]["category"]
            
            contentarea =  data["properties"]["category"]["contentarea"] # :TAGEED_CAT
            if "contentarea" in categories:
                tx_categories.append("MERGE (c:ContentArea {name:{name}})", name=contentarea)
                tx_categories.append("MATCH (content:Content {url:{url}}), (c:ContentArea {name:{name}}) MERGE (c)-[:TAGGED_CAT]->(content)", url=url, name=contentarea)
                for x in range(1, 4): 
                    ss = "subsection%s" % str(x)
                    print ss
                    
                    if (ss) in categories:
                        print categories[ss]
                        tx_categories.append("MERGE (category:Category {name:{name}}) return category", name=categories[ss])
                        if x==1:
                            tx_categories.append("MATCH (category:Category {name:{name}}), (ca:ContentArea {name:{name2}}) MERGE category-[:BELONGS_TO]->(ca)", name=categories[ss], name2=contentarea)
                        else:
                            ssm = "subsection%s" % str(x-1)
                            tx_categories.append("MATCH (category:Category {name:{name}}), (category2:Category {name:{name2}}) MERGE (category)-[:BELONGS_TO]->(category2)", name=categories[ss], name2=categories[ssm])
            
            tx_categories.commit()
            
            
         
        except IOError as e:
            if debug:
                print e
            return False
        else:
            return True
 