#!/usr/bin/python

import sys
import ast_db
import ast_network

def print_usage():
	print("Usage: {0} <db_file> <port number>\r\n".format(sys.argv[0]))
	print("Starts the AST DNS Server using <db_file> as the database file and listens on <port number> for clients")
	
# Main start of program
if len(sys.argv) < 3:
	print_usage()
	exit()
	
