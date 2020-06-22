""" Using sockets, connect to campus SMTP mail server.
    Then implement the SMTP conversations in the python program,
      which will contact with the server to send your email
      to "your_email@utep.edu". """
import base64
import socket

s_addr = 'smtp.aol.com' # 'smtp.office365.com'
s_port = 465 #587

class UTEPEmailServer:
    def __init__(self, addr, prt):
        self.__server = None
        # utep email service
        self.__addr = addr
        self.__prt = prt

    """ Opens an internet stream to the addr:prt specified. """
    def __start_connection(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.connect((self.__addr, self.__prt))
        msg = self.__decode_receive()
        self.__check_closed(msg)
        if '220' not in msg:    # could not open connection
            error_report_and_quit('Could not open connection to\t' + str(self.__addr))

    """ Establish the connection by sending/receiving 'hello'/authentication message. """
    def establish_connection(self):
        self.__start_connection()
        self.__server.send('EHLO\r\n'.encode())
        msg = self.__decode_receive()
        self.__check_closed(msg)
        if '250' not in msg:        # 'hello' not received
            error_report_and_quit('Could not establish connection to\t' + str(self.__addr))
        print('Established connection to:\t' + self.__addr)

    """ Logs into the server using provided credentials """
    def log_in(self, user, pswd):
        b64 = base64.b64encode(("\x00"+user+"\x00"+pswd).encode())
        self.__server.send("AUTH PLAIN ".encode() + b64 + "\r\n".encode())
        msg = self.__decode_receive()
        self.__check_closed(msg)
        return msg

    """ Close the connection. """
    def close(self):
        self.__server.shutdown()
        self.__server.close()
        print('Closed connection.')

    """ Decodes the message received from base64. """
    def __decode_receive(self, msg=1024):
        return self.__server.recv(msg).decode()   # decode from base64

    """ Has the connection closed abruptly? """
    def __check_closed(self, msg):
        if not msg:             # connection closed
            error_report_and_quit()


""" Report error message to console and quit program unsuccessfully. """
def error_report_and_quit(msg='Connection was closed.'):
    print('ERROR: ' + msg)
    exit(1)

if __name__ == '__main__':
    # open the connection
    server = UTEPEmailServer(s_addr, s_port)
    server.establish_connection()

    # log in to user-provided credentials
    msg = '504'
    while '504' in msg:
        user = input('Enter your username for ' + s_addr + ':\t')
        pswd = input('Enter your password for ' + user + ':\t')
        msg = server.log_in(user, pswd)
        print(msg)
    print('Successfully logged in to:\t' + user + ' at ' + s_addr)

    server.close()
