#!/usr/bin/python

import sys
import threading
import os.path
import ast_db
import ast_network

def print_usage():
	print("Usage: {0} <db_file> <port number>\r\n".format(sys.argv[0]))
	print("Starts the AST DNS Server using <db_file> as the database file and listens on <port number> for clients")
	
# Main start of program
if len(sys.argv) < 3:
	print_usage()
	exit()
	
# Check to make sure parameters are good
if not sys.argv[2].isdigit():
	print_usage()
	exit()

# MAIN CODE BELOW ##################################

try:
	if os.path.isfile(sys.argv[1]):
		db_init = 0
	else:
		db_init = 1
	
	db = ast_db.open_db(sys.argv[1])
	if db_init:
		ast_db.init_db(db)
		hosts = {}
	else:
		hosts = ast_db.load_hosts(db)

	server = ast_network.start_server('', int(sys.argv[2]))

	#Setup shared properties
	server.ast_db_lock = threading.Lock()
	server.ast_db = db
	server.running = 1
	server.send_updates = 0
	server.host_table = hosts
	server.client_sockets = []

	server.serve_forever()
except Exception as e:
	print("An exception occurred!\r\n{0}\r\n Closing Server!".format(e))