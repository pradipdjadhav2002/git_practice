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






#def client_fun():
	














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
