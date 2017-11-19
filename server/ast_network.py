# Network functions for AST_DNS Server

import socketserver
import socket
import threading
import select
import ast_db

class ClientHandler(socketserver.BaseRequestHandler):
	# This class handles the actual client connections once connected
	
	cur_hostname = ""
	
	def handle(self):
		# Handles individual Client connections and threads
		print("New Client Connected from {0}".format(self.client_address[0]))
		
		while self.server.running:
			# Handle reading from individual clients
			
			poller = select.epoll()
			poller.register(self.request.fileno(), select.EPOLLIN)
			
			try:
				
				events = poller.poll(0)
				
				# If any updates, send them to the client
				if self.server.send_updates:
					print("Updates Ready to Send!\r\nSending data: {0}\r\n".format(self.make_host_string(self.server.host_table)))
					self.server.ast_db_lock.acquire()
					self.server.send_updates = 0
					self.server.ast_db_lock.release()
			
				for sock, evt_type in events:
					if evt_type & select.EPOLLIN:
						data = self.request.recv(1024)
						
						if len(data) >= 1:
							data = data.strip().decode('utf-8')
							print("New hostname reported from: {0}, new hostname is {1}\r\n".format(self.client_address[0], data))
							
							# Lock the database output here and write to the db file
							#print("Attempting to acquire DB map_host Lock on {0}\r\n".format(self.server.ast_db_lock))
							self.server.ast_db_lock.acquire() #blocks until acquired
							try:
								#ast_db.map_host(self.server.ast_db, data.strip(), self.client_address[0])
								if len(self.cur_hostname) > 0:
									del self.server.host_table[self.cur_hostname];
								self.server.host_table[data] = self.client_address[0]
								self.cur_hostname = data
								self.server.send_updates = 1
							finally:
								self.server.ast_db_lock.release()
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
				
			except Exception as e:
				print("Exception occurred! Closing connection from {0}\r\n{1}\r\n".format(self.client_address[0], e))
				self.request.shutdown(socket.SHUT_RDWR)
				self.request.close()
				break;
	
	def make_host_string(self, hosts):
		output = "{0}:".format(len(hosts))
		for host in hosts:
			output = "{0}{1}={2}--".format(output, host, hosts[host])
		return output
			
class ASTSocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass
	

def start_server(host, port):
	# Actually creates the TCP socket server and returns it, simply call serve_forever() to keep it going forever when ready
	server = ASTSocketServer((host, port), ClientHandler)
	return server
	