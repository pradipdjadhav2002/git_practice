from socket import *
import sys
import datetime
import os
import time
import os.path	

Status_Code = {
	200:'OK', 201: 'Created', 204: 'No Content', 301: 'Moved Permanently',304: 'Not Modified',
				400:'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404:'Not Found', 408: 'Request Timeout',
				411: 'Length Required', 413: 'Payload Too Large', 414: 'URI Too Long', 
				415: 'Unsupported Media Type', 500: 'Internal Server Error', 501:'Not Implemented', 
				503: 'Service Unavailable',	505:'HTTP Version not Supported'	
}

content_types ={
	'html': 'text/html', 'txt': 'text/plain', 'pdf': 'application/pdf', 'mp3': 'audio/mpeg',
	'jpg': 'image/jpeg', 'png': 'image/png', 'csv': 'text/csv', 'mp4': 'video/mp4'
}

direct_extensions = ['jpg', 'jpeg', 'png', 'mp3', 'mp4', 'pdf']

versions = ['1.1', '1.0']



def date():
	x = datetime.datetime.now()
	return x.strftime("%a, %d %b %y %H:%M:%S GMT")

def Last_Modified(path):
	s = path.split('/')
	file_name = s[-1] 
	x = time.ctime(os.path.getmtime(file_name)).split(' ')
	if(len(x[3])):
		x[3] = "0" + x[3] 
	return x[0] + ","+ " " + x[3] + " " + x[1] + " " + x[5][2:] + " " + x[4] + " GMT"
	
def If_Modified_Since(date):
	mon = ['Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	x = Last_Modified(path).split(',')[1].split(' ')
	x = x[2] + str(mon.index(x[1]) + 1) + x[0] + x[3] + x[4]
	y = date.split(',')[1].split(' ') 
	y = y[2] + str(mon.index(x[1]) + 1) + y[0] + y[3] + y[4]
	
	if(x < y):
		return True
	else:
		return False






def client_fun(request_header, connectionsocket):
	data = response_header.split("\r\n")
	method_data = data[0].split(" ")
	path = method_data[1]	
	start_time = datetime.datetime.now()
	version = method_data[2].split('/')[1]
	try:
		
		diff = end_time - start_time
		minutes = diff / timedelta(minutes=1)
		if(abs(minutes) > 0.3):
			status_code = 408
			get_headers[status_code] = 408
			file_name = "408_error.html"
			ToSend = get_headers(status_code, file_name, request.method, request.server, request.language, request.encoding, cookie_flag, version)
			connectionSocket.send(ToSend.encode())
			file_length = get_file_length(file_name)
			#logging.info(f"{host_address}: \"{request.request_line}\" {status_code} {file_length} \"{request.server}\"\n")
			connectionSocket.close()
			
		if version not in versions:
			status_code = 505
			ToSend = f"{status_code} {status_codes[status_code]}\n\n"
			connectionSocket.send(ToSend.encode())
			#logging.info(f"{host_address}: \"{request.request_line}\" {status_code} \"{request.server}\"\n")
			#logging.error(f"{host_address}: [client {addr}] HTTP Version not Supported in Request {request.request_line} \n")

		else:	
			if(request.method == 'GET' or request.method == 'HEAD' or request.method == 'POST'):
				try:
					if('/' in request.uri):
								
						if((len(request.uri) - MAX_URI_LENGTH)<0):						
							PATH = os.getcwd()
							PATH += request.uri
							
							#redirection
							if(PATH == REDIRECTED_PAGE):
								status_code = 301
								logging.info(f"{host_address}: \"{request.request_line}\" {status_code} \"{request.server}\"\n")
								ToSend = f"HTTP/{version} {status_code} {status_codes[status_code]}\n"
								ToSend += f"Location: http://127.0.0.1:{serverPort}/website/new.html \n"										
								connectionSocket.send(ToSend.encode())

							else:
								if(os.path.isfile(PATH) or (request.uri == '/')):
									if(os.access(PATH, os.R_OK) and os.access(PATH, os.W_OK)):		
										#success
										status_code = 200
										file_name = request.uri.strip('/')
										if request.uri == '/':
											file_name = "index.html"
											spl = file_name.split('.')
											extension = spl[1]

										if(request.if_modified != None):
													status_code = if_modified_since(request.if_modified, file_name)

										if(request.method == "POST"):
											# print_post_data(request.user_data)
											print_post_data(ent_body)

										if(content_types.get(extension) == None):
											status_code = 415
											file_name = "415_error.html"
											ToSend = f"HTTP/{version} {status_code} {status_codes[status_code]} \n"
											ToSend += "Connection:close\n\n"
											# ToSend += "<h1> Unsupported Media Type </h1>"
											fr = open(file_name, 'r')
											data = fr.read()
											ToSend += data
																					connectionSocket.send(ToSend.encode())
													

										else:
											#other than html and txt
											if(extension in direct_extensions):
												if(request.method != "HEAD"):
													# modified
													if(status_code != 304):
														ToSend, data = get_headers(status_code, file_name, request.method, request.server, request.language, request.encoding, cookie_flag, version)
													
													connectionSocket.send(ToSend.encode())
																connectionSocket.send(data)
															else:
																ToSend = get_headers(status_code, file_name, request.method, request.server, request.language, request.encoding, cookie_flag, version)
																connectionSocket.send(ToSend.encode())																
														else:
															ToSend = get_headers(status_code, file_name, request.method, request.server, request.language, request.encoding, cookie_flag, version)
															connectionSocket.send(ToSend.encode())													
													#html files
													else:
														ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)
														connectionSocket.send(ToSend.encode())

											else:
												#forbidden file
												status_code = 403
												file_name = "403_error.html"	
												ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)
												connectionSocket.send(ToSend.encode())
										else:
											#file not found
											status_code = 404
											file_name = "404_error.html"
											ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)
											connectionSocket.send(ToSend.encode())
								else:
									#URI too long
									status_code = 414
									file_name = "414_error.html"
									ToSend = get_headers(status_code, file_name, request.method, request.server, request.language, request.encoding, cookie_flag, version)
									connectionSocket.send(ToSend.encode())
							
							file_length = get_file_length(file_name)
							logging.info(f"{host_address}: \"{request.request_line}\" {status_code} {file_length} \"{request.server}\"\n")

						except:					
							#Bad request
							status_code = 400
							file_name = "400_error.html"
							ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)	
							connectionSocket.send(ToSend.encode())

							file_length = get_file_length(file_name)
							logging.info(f"{host_address}: \"{request.request_line}\" {status_code} {file_length} \"{request.server}\"\n")


					elif(request.method == "DELETE"):
						try:
							if('/' in request.uri):
								if(len(request.uri) < MAX_URI_LENGTH):
									PATH = os.getcwd()
									PATH += request.uri
									if(os.path.isfile(PATH)):
										if(os.access(PATH, os.R_OK) and os.access(PATH, os.W_OK)):
											file_name = request.uri.strip('/')
											spl = file_name.split('.')
											extension = spl[1]
											
											if extension in direct_extensions:
												f = open(file_name, 'rb')
											else:
												f = open(file_name, 'r')
											text = f.read()
											file_length = get_file_length(file_name)
											
											#if user is authorized
											if(authorization(request.authorization)):
												if(int(len(text)) == 0):
													# No Content
													status_code = 204
													ToSend = f"HTTP/{version} {status_code} {status_codes[status_code]}\n\n"
													os.remove(file_name)
													connectionSocket.send(ToSend.encode())				
												else:
													#success
													status_code = 200
													ToSend = delete_headers(status_code, file_name, request.method, request.server, cookie_flag, version)
													connectionSocket.send(ToSend.encode())
											#user not authorized
											else:
												status_code = 401
												ToSend = f"HTTP/{version} {status_code} {status_codes[status_code]}\nDate:"
												date_time = parse_date_time()
												ToSend += date_time
												ToSend += "WWW-Authenticate: Basic realm=\"Access to staging site\", charset=\"UTF-8\""
												connectionSocket.send(ToSend.encode())		

										else:
											#forbidden file
											status_code = 403
											file_name = "403_error.html"	
											file_length = get_file_length(file_name)

											ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)
											connectionSocket.send(ToSend.encode())

									else:									
										#file not found
										status_code = 404
										file_name = "404_error.html"
										file_length = get_file_length(file_name)

										ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)
										connectionSocket.send(ToSend.encode())
								
								else:
									#URI too long
									status_code = 414
									file_name = "414_error.html"
									file_length = get_file_length(file_name)

									ToSend = get_headers(status_code, file_name, request.method, request.server, request.language, request.encoding, cookie_flag, version)

									connectionSocket.send(ToSend.encode())
							
							logging.info(f"{host_address}: \"{request.request_line}\" {status_code} {file_length} \"{request.server}\"\n")
							connectionSocket.close()
					
						except:
							#Bad request
							# print("except")
							status_code = 400
							file_name = "400_error.html"
							ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)			
							connectionSocket.send(ToSend.encode())

							file_length = get_file_length(file_name)
							logging.info(f"{host_address}: \"{request.request_line}\" {status_code} {file_length} \"{request.server}\"\n")

					
					elif(request.method == "PUT"):

						try:
							if('/' in request.uri):
								if(len(request.uri) < MAX_URI_LENGTH):

									PATH = os.getcwd()
									PATH += request.uri
									data = request.user_data
									file_name = request.uri.strip('/')

									if(request.content_length != None):										
										if(int(request.content_length) < MAX_PAYLOAD):
											if(os.path.isfile(PATH)):
												if(os.access(PATH, os.R_OK) and os.access(PATH, os.W_OK)):
													#success
													status_code = 200
													os.remove(file_name)
													ToSend = put_headers(connectionSocket, status_code, request.uri, ent_body, f_flag, cookie_flag, request.content_length, version)
													connectionSocket.send(ToSend.encode())

												else:
													#forbidden file
													status_code = 403
													file_name = "403_error.html"
													ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)
													connectionSocket.send(ToSend.encode())
											
											else:
												#new file created
												status_code = 201
												ToSend = put_headers(connectionSocket, status_code, request.uri, ent_body, f_flag, cookie_flag, request.content_length, version)
												connectionSocket.send(ToSend.encode())
										else:
											#payload too large
											status_code = 413
											file_name = "413_error.html"
											ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)
											connectionSocket.send(ToSend.encode())
									else:
										#length required
										status_code = 411
										file_name = "411_error.html"
										ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)
										connectionSocket.send(ToSend.encode())
										
								else:
									#URI too long
									status_code = 414
									file_name = "414_error.html"
									ToSend = get_headers(status_code, file_name, request.method, request.server, request.language, request.encoding, cookie_flag, version)
									connectionSocket.send(ToSend.encode())
									file_length = get_file_length(file_name)
									logging.info(f"{host_address}: \"{request.request_line}\" {status_code} {file_length} \"{request.server}\"\n")
								

								file_length = get_file_length(file_name)
								logging.info(f"{host_address}: \"{request.request_line}\" {status_code} {file_length} \"{request.server}\"\n")
								# print("logging")

						except:
							#Bad request
							status_code = 400
							file_name = "400_error.html"
							ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)			
							connectionSocket.send(ToSend.encode())
							
							file_length = get_file_length(file_name)
							logging.info(f"{host_address}: \"{request.request_line}\" {status_code} {file_length} \"{request.server}\"\n")

						connectionSocket.close()
			
					else:

						status_code = 501
						file_name = "501_error.html"
						ToSend = get_headers(status_code, file_name, request.method, request.server,  request.language, request.encoding, cookie_flag, version)
						connectionSocket.send(ToSend.encode())

						file_length = get_file_length(file_name)
						logging.info(f"{host_address}: \"{request.request_line}\" {status_code} {file_length} \"{request.server}\"\n")
						logging.error(f"{host_address}: [client {addr}] Invalid method in request {request.request_line} \n")

				if(version == '1.0'):
					connectionSocket.close()

			except:
				status_code = 500
				ToSend = f"HTTP/1.1 {status_code} {status_codes[status_code]}\n"
				connectionSocket.send(ToSend.encode())

				logging.info(f"{host_address}: {status_code} \n")
				logging.error(f"{host_address}: [client {addr}] Internal Server Error in request\n")

		except:
			
			conn = False
		
		end_time = datetime.datetime.now()
		
	













def GET(path, data_sliced, connectionsocket):
	
	header_dict = {} 
	for i in range(len(data_sliced)):
		temp = data_sliced[i].split(':')
		header_dict[temp[0]] = temp[1]
	print(header_dict)
	
	general_header = "HTTP/1.1 200 OK" +  "\nConnection: "+ header_dict['Connection']  + "\nDate: "+ date() + "\nserver : Apache/2.2" + "\nAccept - Ranges: Bytes" + "\nAccept-Language: en-US,en;q=0.9" + "\nLast_Modified: "  + Last_Modified(path) + "\r\n\r\n"
	
	
	
	
	return general_header 


def select_request(response_header, connectionsocket):
		#print(response_header)
		data = response_header.split("\r\n")
		print(data)
		method_data = data[0].split(" ")
		#print(method_data)
		path = method_data[1]
		print(path)
		if(method_data[0] == 'GET'):
			response_header = GET(path, data[1:len(data) -2], connectionsocket)
		else:
			response_header = 'HTTP/1.1 '
		
		return response_header

def main():
		socket_1 = socket(AF_INET,SOCK_STREAM)
		socket_1.bind(('127.0.0.1', int(sys.argv[1])))
		socket_1.listen(5)
		print("SERVER IS READY...\n")
		while True:
				connectionsocket, address = socket_1.accept()
				print("Request is received fron client IP address : \n",address)
				request_header = connectionsocket.recv(1024).decode()
				response_header = select_request(request_header, connectionsocket)
				print(response_header)
				response_header = response_header.encode()
				connectionsocket.send(response_header)
				
main()
