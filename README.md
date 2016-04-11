# tornado-analytics-server

Now with extra NEO!

## CONFIGURE

* pip install -t requirements.txt 

Edit the config.py file 
* neo4j server, 
* neo4j password (assumed username is neo4j) 
* server port 

## IMPLEMENTATION

Add the following code to your web pages (based on the CBC tagged properties)
```

    <script type="text/javascript">
        /* TESTING ONLY */
        var CBC = {};
        CBC.APP = {};
        var s = CBC.APP.SC = {};
        s.keywords = "Idaho, United States, General news, Lotteries, Bernie Sanders, Arizona, U.S. Democratic Party, Primary elections, Caucuses, Government and politics, Donald Trump, Voting, Ted Cruz, Hillary Clinton, Utah, Weapons of mass destruction";
        /* END TESTING */
        
        var category=CBC.APP.SC.keywords.split(","); //OR HOWEVER YOU WANT TO GENERATE AN ARRAY
    </script>
    ....
    <script src="http://localhost:8888/lana.js"></script>
    <script type="text/javascript">
			/* setup analytics for this page */
			
			var trackingData = {"category":category};
			//lana.debug(true);
    			lana.track("load", trackingData);
		  /* configure readJS for this page */
			var readingJSConfig = {};
			readingJSConfig.el=".article-text";
			readingJSConfig.cb = function(){
		    		lana.track("read", trackingData);
			}; 
		window.readingJSConfig = readingJSConfig;
    </script>
    <script src="http://{your_analytics_server}:{analytics_port}/read.js"></script>

```
Your API JSON string should look like: 

```

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
```


## Running

> tornado -f tserver.py

