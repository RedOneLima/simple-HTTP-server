import socket
import datetime, time

#---------------------------------------------------------------------------------------------------------------------#

#  takes the server response, breaks it into list items according to the newline character, iterates the lines until it
#  finds the line that contains the escape sequence, removes the empty lines, and writes the body to an output file.

def parse_html(received):
    server_response = received.split('\n\n')
    header = server_response[0]
    print header+'\n\n'

    if '\r\n\r\n\r\n\r\n' in server_response[-1]:
        lastLine = str(server_response[-1])
        lastLine = lastLine.split('\r')
        server_response[-1] = lastLine[0]
        outfile = open('CS3700.htm','w')
        toFile = '\n'.join(server_response[1:])
        outfile.write(toFile)
        outfile.close()


#---------------------------------------------------------------------------------------------------------------------#

#Reconnects to the socket on a new thread if the connection fails or disconnects.

def reconnect():
    print "Lost connection with server"
    time.sleep(.5)
    print 'Attempting to reconnect...'
    time.sleep(.5)
    print ' '
    time.sleep(.5)
    try:
        resendTime = str(datetime.datetime.now().time()).split(':')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, 5120))
        sock.sendall(data)
        received = sock.recv(10240)
    except socket.error:
        print 'Unable to reconnect'
        sock.close()
        print 'Socket closed.'
    else:
        reconnectTime =str(datetime.datetime.now().time()).split(':')
        RTTQuery = (float(reconnectTime[-1])-float(resendTime[-1]))*1000
        print '\nTotal Query Time: {} ms\n'.format(RTTQuery)
        parse_html(received)


#---------------------------------------------------------------------------------------------------------------------#

#Main function

data = ''
HOST = raw_input('Enter Host/DNS: ')
#create socket object: SOCK_STREAM means TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    currentTime = str(datetime.datetime.now().time()).split(':')
    sock.connect((HOST, 5120))#conncetion request
except socket.error:
    print 'Something went wrong trying to connect...'
    reconnect()
else:
    connectedTime =str(datetime.datetime.now().time()).split(':')
    RTTConnect = (float(connectedTime[-1])-float(currentTime[-1]))*1000
    print 'Connected in {} ms'.format(RTTConnect)

while data != 'n':

#User end info input

    request = raw_input("Request Line:\n>>")
    file_name = raw_input('File Name:\n>>')
    http_version = raw_input('HTTP Version:\n>>')
    user_agent = raw_input('User Agent:\n>>')
    data = request+'/'+file_name+'\nHOST:'+HOST+'\nUser Agent:'+user_agent+'\nHTTP Version: '+http_version+'\n\n'
    print 'Message to server: \n{}'.format(data)


    try:
        QuerySend = str(datetime.datetime.now().time()).split(':')
        sock.sendall(data)#send data to server
        received = sock.recv(10240)#recv data from server
        QueryRec =str(datetime.datetime.now().time()).split(':')
    except socket.error:
      reconnect()

    else:
        #once the server response is recived with no issues, calculate the RTT, and seperate the elements of the response
        RTTQuery = (float(QueryRec[-1])-float(QuerySend[-1]))*1000
        print '\nTotal Query Time: {} ms\n'.format(RTTQuery)
        parse_html(received)

    data = raw_input('Would you like to continue?(Y/n)\n>>')

else:
    sock.close()
    print 'socket closed'