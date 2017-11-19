# Network functions for AST_DNS Server

import socketserver
import threading
import select
import ast_db

class ClientHandler(socketserver.BaseRequestHandler):
	# This class handles the actual client connections once connected
	
	def handle(self):
		# Handles individual Client connections and threads
		print("New Client Connected from {0}".format(self.client_address[0]))
		
		while self.server.running:
			# Handle reading from individual clients
			
			poller = select.epoll()
			poller.register(self.request.fileno(), select.EPOLLIN)
			
			try:
				
				events = poller.poll(0)
			
				for sock, evt_type in events:
					if evt_type & select.EPOLLIN:
						data = self.request.recv(1024)
						
						if len(data) >= 1:
							print("New hostname reported from: {0}, new hostname is {1}\r\n".format(self.client_address[0], data.strip()))
							
							# Lock the database output here and write to the db file
							#self.server.ast_db_lock.aquire() #blocks until aquired
							#try:
							#	ast_db.map_host(self.server.ast_db, hostname, self.client_address[0])
							#finally:
							#	self.server.ast_db_lock.release()
						else:
							print("Client host {0} closed connection!\r\n".format(self.client_address[0]))
							self.request.shutdown(socket.SHUT_RDWR)
							self.request.close()
							break;
							
					elif evt_type & select.EPOLLHUP:
						print("Client host {0} closed connection!\r\n".format(self.client_address[0]))
						self.request.shutdown(socket.SHUT_RDWR)
						self.request.close()
						break;
						
					elif evt_type & select.EPOLLERR:
						print("Client host {0} closed connection!\r\n".format(self.client_address[0]))
						self.request.shutdown(socket.SHUT_RDWR)
						self.request.close()
						break;
				
			except:
				print("Exception occurred! Closing connection from {0}\r\n".format(self.client_address[0]))
				self.request.shutdown(socket.SHUT_RDWR)
				self.request.close()
				break;
			
class ASTSocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass
	

def start_server(host, port):
	# Actually creates the TCP socket server and returns it, simply call serve_forever() to keep it going forever when ready
	server = ASTSocketServer((host, port), ClientHandler)
	return server
	