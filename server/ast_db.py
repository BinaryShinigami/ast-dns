# Database functions for AST-DNS Server

import sqlite3	
	
def open_db(con, db_file):
	# Opens the database file
	con = sqlite3.connect(db_file)
	return con
	
def	init_db(con):
	# Initializes & sets up the database for the first run
	q = "CREATE TABLE mappings (id INTEGER PRIMARY KEY, hostname, ip)"
	con.execute(q)
	
	q = "CREATE UNIQUE INDEX map_host ON mappings(hostname)"
	con.execute(q)
	
def map_host(con, hostname, ip):
	# Stores a key value entry into the sqlite3 database for the host specified
	# Will update if the hostname already exists
	q = "SELECT * FROM mappings WHERE hostname = {0}".format(hostname)
	results = con.execute(q)
	results = results.fetchall()
	if (len(results) > 0):
		#Already Exists we need to update
		q = "UPDATE mappings SET ip = {0} WHERE hostname = {1}".format(ip, hostname)
	else:
		q = "INSERT INTO mappings(hostname, ip) VALUES('{0}','{1}')".format(hostname, ip)
	
	res = con.execute(q)
	if res.rowscount > 0:
		return TRUE
	else:
		return FALSE
