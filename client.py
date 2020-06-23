import base64
import socket
import time

END = '\r\n'

class EmailClient:
    # fixme this is where to change the server info
    def __init__(self, addr='smtp.aol.com', prt=587):
        self.__server = None
        self.__addr = addr
        self.__prt = prt

    """ Opens an internet stream to the addr:prt specified. """
    def __start_connection(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # no TLS?
        self.__server.connect((self.__addr, self.__prt))
        self.__respond_to('','Could not open connection to\t' + str(self.__addr), '220')

    """ Establish the connection by sending/receiving 'hello'/authentication message. """
    def establish_connection(self, domain='mail.aol.com', using_tls=False):
        self.__start_connection()
        self.__respond_to('EHLO ' + domain, 'Could not establish connection to\t' + str(self.__addr))
        if using_tls:
            self.__respond_to('STARTTLS', 'Could not TLS encryption with\t' + str(self.__addr), err_code='220')
            self.__respond_to('EHLO ' + domain, 'Could not establish secure connection to\t' + str(self.__addr))
        print('Successfully established secure connection to ' + self.__addr)

    """ Logs into the server using provided credentials """
    def log_in(self, user, pswd, auth='PLAIN'):
        b64 = base64.b64encode(('\x00' + user +'\x00' + pswd).encode())
        self.__server.send(('AUTH ' + auth + ' ').encode() + b64 + END.encode())
        msg = self.__decode_receive()
        if not msg:                            # connection closed?
            self.__error_report_and_quit()
        return msg

    """ Send an email with a FRM, RCPT, SUBJ, and a MSG """
    def send_email(self, frm='<mmafravi@aol.com>', rcpt='<mmafravi@gmail.com>', subj="Test Email Message",
                   msg='This is a test email.'):
        self.__respond_to('MAIL FROM:' + frm, 'Sender\'s address is rejected.')
        self.__respond_to('MAIL RCPT TO:'+rcpt, 'Recipient\'s address is rejected.')
        self.__respond_to('DATA','Data not accepted to message.', err_code='354')
        self.__respond_to('Subject:'+subj+END, 'Data not accepted to message.')
        # the time and the message
        date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        self.__respond_to(date, '')
        self.__respond_to(END + msg, '')
        self.__respond_to(END + '.', '')
        self.__respond_to('QUIT', 'Server rejected exit command.', err_code='221')
        print('Message sent to\t' + rcpt)

    """ Close the connection. """
    def close(self):
        self.__server.shutdown(socket.SHUT_RD)      # no more proc
        self.__server.close()
        print('Closed connection.')

    """ Decodes the message received from base64. """
    def __decode_receive(self, buff_size=2048):
        return self.__server.recv(buff_size).decode()  # decode from base64

    """ Getters """
    def get_address(self):
        return self.__addr

    """ Send a message (if any), and  """
    def __respond_to(self, msg, msg_on_fail, err_code='250'):
        if msg!='':                                             # data to send
            self.__server.send((msg + END).encode('utf-8'))
        response = self.__decode_receive()
        print( response )
        if not response:                                # connection closed?
            self.__error_report_and_quit()
        if err_code not in response:       # msg not received?
            self.__error_report_and_quit(msg_on_fail)

    """ Report error message to console and quit program unsuccessfully. """
    def __error_report_and_quit(self, msg='Connection was closed.'):
        print('ERROR: ' + msg)
        exit(1)
