import datetime
from datetime import timedelta

def compute_days_ago(days_ago):
    
    theday = datetime.datetime.now()
    date_array = []
    for n in range(0,days_ago):
        ymd = "%s%s%s" % (theday.year , theday.month, theday.day )
        date_array.append(ymd)
        theday = theday - timedelta(1)
        
    return date_array


print """MATCH (day)<-[:INITIATED]-(session),
	(session)<-[k:STARTED]-(user)
WHERE day.date in %s
WITH day.day as day, user.name as username, count(session) as SessionCount 
where SessionCount > 1 
RETURN username, SessionCount""" % compute_days_ago(5)

    

    


        
   