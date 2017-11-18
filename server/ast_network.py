# Network functions for AST_DNS Server

import socketserver
import ast_db

class ClientHandler(socketserver.BaseRequestHandler):
	# This class handles the actual client connections once connected
	global ast_database_lock
	
	def handle(self):
		#Handle client connection here
		print("Client Connected from {0}".format(self.client_address[0]))
	

def start_server(host, port):
	# Actually creates the TCP socket server and returns it, simply call serve_forever() to keep it going forever when ready
	server = socketserver.TCPServer((host, port), ClientHandler)
	return server
	