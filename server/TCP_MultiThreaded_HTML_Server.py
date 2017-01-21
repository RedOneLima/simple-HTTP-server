import threading
import SocketServer
import datetime


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        server_name = 'Simple Python Server 2.7'#name sent as server name
        while 1:
            try:
                in_data = self.request.recv(1024)#listen/recv
                data = in_data.split('\n')#seperate the incoming data from single string to a list
                request_header = str(data[0]).split('/')#seperate the request from the file name
                request = request_header[0]#save request(get)
                file_name= request_header[1]#save file name
                http_version = data[2]#not used
                user_agent = data[3]#not used
            except Exception:#when connection is closed
                print 'Client {} on {} closed'.format(self.client_address, threading.current_thread().name)
                break
            else:
                if str(request).upper() == 'GET':
                    request_code = '200 OK'
                    try:
                        file = open(file_name,'r')
                        request_file = file.read()
                    except IOError:
                        request_code = '404 Not Found'
                else:
                    request_code = '400 Bad Request'

                print 'From {} on {}: \n{}'.format(self.client_address,threading.current_thread().name, in_data)

                if request_code == '200 OK':
                    response =('\n'+request_code+'\nDate: '+str(datetime.datetime.now())+'\nServer: '+server_name+'\n\n'+str(request_file)+'\r\n\r\n\r\n\r\n')
                    print 'To {} on {}: {}'.format(self.client_address, threading.current_thread().name,'\n'+request_code+'\nDate: '+str(datetime.datetime.now())+'\nServer: '+server_name+'\n\n')
                    self.request.sendall(response)
                else:
                    response = ('\n'+request_code+'\nDate: '+str(datetime.datetime.now())+'\nServer: '+server_name+'\n\n')
                    print 'To {} on {}: \n{}'.format(self.client_address,threading.current_thread().name, response)
                    self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = 'cs3700.msudenver.edu',5120
    server = ThreadedTCPServer((HOST,PORT), ThreadedTCPRequestHandler)#create a threaded TCP server
    server_thread = threading.Thread(target=server.serve_forever)#run the threaded server until terminated
    server_thread.start()
    print "Server loop running in thread:", server_thread.name