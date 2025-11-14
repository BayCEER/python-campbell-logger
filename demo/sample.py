from campbell.logger import Logger
from datetime import timedelta

l = Logger("http://demo")

# Get all table uris
tabs = l.getTableUris()

# Get second table name
table = tabs[1]

# Get the 10 most recent records as a dictionary
data = l.dataMostRecent(table,10)

# Get all records since a specific amount of time  
clock = l.getClock()
data = l.dataSinceTime(table, clock - timedelta(seconds=120))

# Get all records with record nr >= 10
data = l.dataSinceRecord(table,10)

# Get all records stored since the last 2 minutes 
data = l.dataBackfill(table,120)