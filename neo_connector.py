from py2neo import Graph, Path
import config
import datetime
import calendar
import time
from datetime import timedelta


pw = config.neo4j_pw
host = config.neo4j_server

graph = Graph("http://neo4j:%s@%s:7474/db/data/"%(pw, host))

debug=False

class NeoConnector():
    def __init__(self):
        """just set it up yo"""
        
    def compute_days_ago(self,days_ago):
        theday = datetime.datetime.now()
        date_array = []
        for n in range(0,days_ago):
            ymd = "%s%s%s" % (theday.year , theday.month, theday.day )
            date_array.append(ymd)
            theday = theday - timedelta(1)
    
        return date_array
        
        
    
    def read_stats(self):
        """reads the stats yo"""
        try:
            users = graph.cypher.execute("MATCH (n:User) return count(n)")
            content = graph.cypher.execute("MATCH (n:Content) return count(n)")
            sessions = graph.cypher.execute("MATCH (n:Session) return count(n)")
            loads = graph.cypher.execute("MATCH (n)-[k:LOADED]-(m) return count(k)")
            reads = graph.cypher.execute("MATCH (n)-[k:READ]-(m) return count(k)")
            
            
            
            # Thanks for the reminder.
 #            I don't have the capacity to add it myself.
 #            Appreciate it if you could give your thoughts on adding the 5 queries below in the dashboard.
 #            The first 3 queries below we could use from the Neo4j Bootcamp.
 #            The last 2 queries below I thought of but don't have the time to write the cypher.

            # 1) Find me all the users that have visited the CBC website x times in the last y days
            date_array_exploded = self.compute_days_ago(5)
            q1="""MATCH (day)<-[:INITIATED]-(session),
            	(session)<-[k:STARTED]-(user)
            WHERE day.date in %s
            WITH day.date as day,  count(session) as SessionCount 
            where SessionCount > 2 
            RETURN day, SessionCount ORDER BY day""" % date_array_exploded
            
            sessionCounts = graph.cypher.execute(q1)
            
            
            
            q_session_today="""MATCH (day)<-[:INITIATED]-(session),
            	(session)<-[k:STARTED]-(user)
            WHERE day.date in %s
            WITH day.date as day,  count(session) as SessionCount 
            where SessionCount > 1 
            RETURN day, SessionCount ORDER BY day""" % self.compute_days_ago(1)
            
            todayCounts = graph.cypher.execute(q_session_today)
            
            q_total_session_today="""MATCH (day)<-[:INITIATED]-(session),
            	(session)<-[k:STARTED]-(user)
            WHERE day.date in %s
            WITH day.date as day,  count(session) as SessionCount 
            where SessionCount > 0 
            RETURN day, SessionCount ORDER BY day""" % self.compute_days_ago(1)
            
            totalSessionCounts = graph.cypher.execute(q_total_session_today)

            # 2) Some Statistical queries to get Story by the action on that whether READ or LOADED or SHARED counts.

            q2="""match (session)-[r]->(story:story)
            return  type(r),count(*) as Counts
            order by Counts"""
            categories = graph.cypher.execute(q2)

            # 3) Statistical query to get counts by User, Session and the type of READ or LOADED or SHARED.

            q3="""match (n:User)-[:STARTED]->(session)-[r]->(story:Story)
            return n.name,session.id, type(r),count(*) as Counts
            order by n.name, Counts"""
            categories = graph.cypher.execute(q2)

            # 4) What are the top 10 categories, people, companies, organizations, locations and subjects in the last x days?
            
            q_top_read = "Match (n:Content)-[:READ]-(s:Session) with count(n) as count, n.name as name return name, count order by count desc limit 10"
            top_read  = graph.cypher.execute(q_top_read)
            
            q_people = "MATCH (n:Subject)-[]-(c:Content)-[:VISITED]-(s:Session)-[]-(d:Day) return n limit 25"
 # #
 
            working = "MATCH (n:Subject)-[k]-(c:Content)-[:LOADED]-(s:Session)-[j]-(d:Day) where (d.date='2016421') return collect(n.name) ;"
 
            # 5) What parts of the day are the top 10 subjects/topics in #4 getting traction from?
            # a) dark morning [12-6am]
            # b) early morning [6-9am]
            # c) late morning [9am-12pm]
            # d) afternoon [12-4pm]
            # e) evening [4-8pm]
            # f) late night [8-12pm]
            #
            
            
            
            
            
            a= users, content, sessions, loads, reads, categories, sessionCounts, todayCounts, totalSessionCounts, top_read
            return a
        except IOError as e:
            if debug:
                print e
            return None
 
    def write_to_neo(self, data): 
        try:
            visit_timestamp = calendar.timegm(time.gmtime()) #visitor.split("-")[0]
            
            
            uid = data["id"] 
            visitor = data["visitor"]   #user - permenant cookie
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
            subjects = []
            
            
            if "company" in data["properties"]["tagged"]:
                companies = data["properties"]["tagged"]["company"] # :TAGGED_C
            if "organization" in data["properties"]["tagged"]:
                organizations = data["properties"]["tagged"]["organization"]  # :TAGGED_O
            if "location" in data["properties"]["tagged"]:
                locations = data["properties"]["tagged"]["location"]  # :TAGGED_L
            if "person" in data["properties"]["tagged"]:
                people = data["properties"]["tagged"]["person"]  # :TAGGED_P
            if "tag" in data["properties"]["tagged"]:
                tags = data["properties"]["tagged"]["tag"] #SUBJECT (  :TAGGED_S)
            if "subject" in data["properties"]["tagged"]:
                subjects = data["properties"]["tagged"]["subject"] #SUBJECT (  :TAGGED_S)
            
            publicationDate = data["properties"]["publicationDate"] #  day-[:PART_OF] -> (month/year)
            
            publicationDateParts = datetime.datetime.utcfromtimestamp((float(publicationDate)/1000))
            pd_ym = "%s%s" % (publicationDateParts.year , publicationDateParts.month )
            pd_dd = str(publicationDateParts.day).zfill(2)
            pd_ymd = "%s%s" % (pd_ym, pd_dd)
            
            timeStampParts = datetime.datetime.utcfromtimestamp(float(visit_timestamp))
            ts_ym = "%s%s" % (timeStampParts.year , timeStampParts.month )
            ts_dd = str(timeStampParts.day).zfill(2)
            ts_ymd = "%s%s" % (ts_ym, ts_dd)
            
         
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
            tx.append("MERGE (n:User { name:{visitor} }) return id(n) as nid",visitor=visitor )
            tx.append("MERGE (n:Session { id : {session} }) return id(n) as nid",session=session)
            tx.append("MATCH (m:Session { id : {session} }),(n:User { name:{visitor} }) MERGE (n)-[:STARTED]->(m)",visitor=visitor ,session=session)
            result = tx.commit()

            #match user to session
            
            tx_user_session = graph.cypher.begin()
            
            ux = "MATCH (user:User {name:{visitor}}),(session:Session {id:{name}}) MERGE (user)-[r:STARTED]->(session)  RETURN r "
            tx_user_session.append(ux,  name=session, visitor=visitor)
            
            cq = "MERGE (content:Content { url:{url}}) ON CREATE set content={url: '%s',name:'%s', publicationDate:'%s'}" % (url, title.replace("'", r"\'")  , publicationDate) 
            cq_label  = "MATCH (n:Content {url:{url}}) set n :%s " % contenttype
           
            tx_user_session.append(cq,url=url )
            tx_user_session.append(cq_label,url=url)
            tx_user_session.append("MATCH (day:Day {date:{pd_ymd}}), (content:Content{url:{url}}) MERGE (content)-[:PUBLISHED]->(day);", url=url, pd_ymd=pd_ymd)
            tx_user_session.append("MATCH (session:Session { id:{session} } ), ( day:Day { date:{ts_ymd} } ) MERGE (session)-[:INITIATED]->(day)", session=session, ts_ymd=ts_ymd )
            
           
            #check for load type (read, visited)
            if action=="load":
                tx_user_session.append("MATCH (m:Session { id : {session} }),(n { url:{url} }) MERGE (m)-[:LOADED]->(n)",url=url ,session=session)
            else:
                tx_user_session.append("MATCH (m:Session { id : {session} }),(n { url:{url} }) MERGE (m)-[:READ]->(n)",url=url ,session=session)
                
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
            for subject in subjects:
                r_tx.append("MERGE (subject:Subject { name:{tag}})", tag=subject)
                r_tx.append("MATCH (content:Content{url:{url}}),(subject:Subject { name:{tag}}) MERGE (content)-[k:TAGGED_S]->(subject)", tag=subject, url=url)
            #r_tx.commit()
            #tx_categories = graph.cypher.begin()
            
            categories = data["properties"]["category"]
            contentarea =  data["properties"]["category"]["contentarea"] # :TAGEED_CAT
            if "contentarea" in categories:
                r_tx.append("MERGE (c:ContentArea {name:{name}})", name=contentarea)
                r_tx.append("MATCH (content:Content {url:{url}}), (c:ContentArea {name:{name}}) MERGE (c)-[:TAGGED_CAT]->(content)", url=url, name=contentarea)
                for x in range(1, 4): 
                    ss = "subsection%s" % str(x)
                    if (ss) in categories:
                        if categories[ss]!="":
                            r_tx.append("MERGE (category:Category {name:{name}}) return category", name=categories[ss])
                            if x==1:
                                r_tx.append("MATCH (category:Category {name:{name}}), (ca:ContentArea {name:{name2}}) MERGE category-[:BELONGS_TO]->(ca)", name=categories[ss], name2=contentarea)
                            else:
                                ssm = "subsection%s" % str(x-1)
                                r_tx.append("MATCH (category:Category {name:{name}}), (category2:Category {name:{name2}}) MERGE (category)-[:BELONGS_TO]->(category2)", name=categories[ss], name2=categories[ssm])
            r_tx.commit()
            
         
        except IOError as e:
            if debug:
                print e
            return False
        else:
            return True
 