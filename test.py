#locust -f test.py

from locust import HttpLocust, TaskSet, task
import random

"""
This code creates random pages based on the CBC digital 
"""
class WebsiteTasks(TaskSet):
    def on_start(self):
            # assume all users arrive at the index page
        self.index()
        
    
    @task(1)
    def index(self):
        variant = random.randint(1, 20) #user
        n = random.randint(1, 1000) #page
        #nc = interests.interests[int(n/10)] #category
        r = random.randint(1, 5)
        x="viewed"
        if r==2:
            x="read"
            
        json = """{
  "visit": "1459451668464-99d9d637-e97f-4c47-a3a3-bc9533784eac",
  "visitor": "1459451668465-201688db-8897-436c-8364-635c07f4e8c3",
  "id": "1459455807203-898b918b-9b24-4d94-80f5-915fc77abc29",
  "name": "load",
  "properties": {
    "tagged": {
      "company": ["cbc"],
      "organization": ["who"],
      "tag": ["death"],
      "location": ["toronto"]
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
"""
        url = """/lana/events?%s""" % (json)
        
        self.client.get(url)
   

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://localhost:8888"
    min_wait = 1
    max_wait = 3
    
    
