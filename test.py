#pip install -t requirements.txt 
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
        n = random.randint(1, 5) #page
        #nc = interests.interests[int(n/10)] #category
        r = str(random.randint(1, 5))
        titles = ["Orion Mars-mission launch delayed for 24 hours - Technology & Science - CBC", "Rob ford dies", "Jian Makes a cake", "Sarah Fulford is cool","YAY " ,"Mansbridge FTW"]
        urls = ["https://cbc.ca/1","https://cbc.ca/2","https://cbc.ca/3","https://cbc.ca/4","https://cbc.ca/5","https://cbc.ca/6"  ]
        x="viewed"
        if r==2:
            x="read"
        else:
            x="load"
            
        json = """{
  "visit": "1459451668464-99d9d637-e97f-4c47-a3a3-bc9533784e%s",
  "visitor": "1459451668465-201688db-8897-436c-8364-635c07f4e8c%s",
  "id": "1459455807203-898b918b-9b24-4d94-80f5-915fc77abc29",
  "name": "%s",
  "properties": {
    "tagged": {
      "company": ["cbc", "ITG", "wpp"],
      "organization": ["who","what"],
      "tag": ["death","taxes"],
      "location": ["toronto","beaverton","hamilton"]
    },
    "publicationDate": "1417713392711",
    "title": "%s",
    "url": "%s",
    "category": {
      "subsection3": "c language",
      "subsection4": "low-level",
      "subsection1": "technology",
      "subsection2": "programming",
      "contentarea": "news",
      "contenttype": "story"
    }
  },
  "time": 1459455807.203
}
""" % (r,r,x, titles[n] ,urls[n] )
        url = """/lana/events?%s""" % (json)
        try:
            self.client.get(url)
        except IOError as e:
            print e
            
   

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://cbc.propellerheadlabs.io:8888"
    min_wait = 1
    max_wait = 3
    
    
