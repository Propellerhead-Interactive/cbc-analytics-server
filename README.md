# tornado-analytics-server

Now with extra NEO!

## CONFIGURE

Edit the config.py file 
* neo4j server, 
* neo4j password (assumed username is neo4j) 
* server port (8888 for development)

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
			lana.debug(true);
      lana.track("load", trackingData);
		  /* configure readJS for this page */
			var readingJSConfig = {};
			readingJSConfig.el=".article-text";
			readingJSConfig.cb = function(){
		    lana.track("read", trackingData);
			}; 
		window.readingJSConfig = readingJSConfig;
	  </script>
    <script src="http://localhost:8888/read.js"></script>

```


## Running

> tornado -f tserver.py

