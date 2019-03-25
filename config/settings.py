import os
import tormysql

app_settings={
	
"autoreload":True,
"debug":False,
"static_path":os.path.join(os.path.dirname(os.path.dirname(__file__)),'asserts/static'),
"template_path":os.path.join(os.path.dirname(os.path.dirname(__file__)),'asserts')
}

db_pool = tormysql.ConnectionPool(
    max_connections = 20, #max open connections
    idle_seconds = 7200, #conntion idle timeout time, 0 is not timeout
    wait_connection_timeout = 3, #wait connection timeout
    host = "11.11.11.239",
    user = "root",
    passwd = "hm.2016",
    db = "amisxiamen",
    charset = "utf8"
)
