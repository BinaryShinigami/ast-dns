# Network functions for AST_DNS Server

import socketserver
import threading
import ast_db

class ClientHandler(socketserver.BaseRequestHandler):
	# This class handles the actual client connections once connected
	
	def handle(self):
		# Handles individual Client connections and threads
		print("New Client Connected from {0}".format(self.client_address[0])
		
		# INSERT CODE TO GET HOSTNAMES HERE
		
		# Lock the database output here and write to the db file
		self.server.ast_db_lock.aquire() #blocks until aquired
		try:
			ast_db.map_host(self.server.ast_db, hostname, self.client_address[0])
		finally:
			self.server.ast_db_lock.release()
	

def start_server(host, port):
	# Actually creates the TCP socket server and returns it, simply call serve_forever() to keep it going forever when ready
	server = socketserver.TCPServer((host, port), ClientHandler)
	return server
	