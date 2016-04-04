MERGE (n:User { name:"12345" }) return id(n) as nid;
MERGE (n:Session { name:"123456" }) return id(n) as nid;
MATCH (user:User {name:"12345"}),(session:Session { name : "123456" })  MERGE  (user)-[r:STARTED]->(session)  RETURN r, user, session;
MERGE (content:Content:Story { name:"Orion Mars-mission launch delayed for 24 hours - Technology & Science - CBC", url:"http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true", publicationdate:"1417713392711" }) return content;


MATCH (content:Content{url:"http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true"}),(session:Session{name:"123456"}) MERGE (session)-[k:LOADED]->(content)  RETURN k;
MATCH (content:Content{url:"http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true"}),(session:Session{name:"123456"}) MERGE (session)-[k:READ]->(content)  RETURN k;

#loop
MERGE (location:Location { name:"Toronto" }) ;
MATCH (content:Content{url:"http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true"}),(location:Location{name:"Toronto"}) MERGE (content)-[k:TAGGED_L]->(location)  RETURN k;

#loop
MERGE (person:Person { name:"Rob Ford" }) return person;
MATCH (content:Content{url:"http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true"}),(person:Person{name:"Rob Ford"}) MERGE (content)-[k:TAGGED_P]->(person)  RETURN k;

#loop
MERGE (company:Company { name:"cbc" }) ;
MATCH (content:Content{url:"http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true"}),(company:Company { name:"cbc" }) MERGE (content)-[k:TAGGED_C]->(company)  RETURN k;

#loop
MERGE (organization:Organization { name:"who" }) ;
MATCH (content:Content{url:"http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true"}),(organization:Organization { name:"who" }) MERGE (content)-[k:TAGGED_O]->(organization)  RETURN k;




#nesting - up to 5 items
MERGE (category:Category { name:"news" }) ;
MERGE (category:Category { name:"technology" }); 
MATCH (category:Category { name:"news" }),(category2:Category { name:"technology" }) MERGE (category2)-[k:BELONGS_TO]->(category)  RETURN k;


MATCH (content:Content{url:"http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true"}),(category2:Category { name:"technology" }) MERGE (content)-[k:TAGGED_CAT]->(category2)  RETURN k;


MERGE (year_month:Year_Month {id:"201603"});
MERGE (day:Day {day:"23",date:"20160323" });
MATCH (year_month:Year_Month {id:"201603"}),(day:Day {date:"20160323"}) MERGE (year_month)-[:PART_OF]->(day);
MATCH (day:Day{date:"20160323"}), (content:Content{url:"http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true"}) MERGE (content)-[:PUBLISHED]-(day);

MERGE (year_month:Year_Month {id:"201603"});
MERGE (day:Day {day:"31",date:"20160331" });
MATCH (year_month:Year_Month {id:"201603"}),(day:Day {date:"20160331"}) MERGE (year_month)-[:PART_OF]->(day);
MATCH (session:Session{name:"123456"}),(day:Day {date:"20160331"}) MERGE (session)-[:INITIATED]->(day);

{
  "visit": "1459451668464-99d9d637-e97f-4c47-a3a3-bc9533784eac",
  "visitor": "1459451668465-201688db-8897-436c-8364-635c07f4e8c3",
  "id": "1459455807203-898b918b-9b24-4d94-80f5-915fc77abc29",
  "name": "load",
  "properties": {
    "tagged": {
      "company": ["cbc"],
      "organization": ["who"],
      "tag": ["death"],
      "location": ["toronto"],
      "person":["Rob Ford"]
    },
    "publicationDate": "1417713392711",
    "title": "Orion Mars-mission launch delayed for 24 hours - Technology & Science - CBC",
    "url": "http://www.qa.nm.cbc.ca/news/technology/orion-mars-mission-launch-delayed-for-24-hours-1.342598?statsDebug=true",
    "category": {
      "subsection3": "",
      "subsection4": "",
      "subsection1": "technology",
      "subsection2": "",
      "contentarea": "news",
      "contenttype": "story"
    }
  },
  "time": 1459455807.203
}
