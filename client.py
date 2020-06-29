import base64
import socket
import time
import ssl

END = '\r\n'
sign = 'Mahdokht Afravi' + END


class EmailClient:
    # fixme this is where to change the server info
    def __init__(self, addr='smtp.aol.com', prt=587):
        self.__server = None
        self.__addr = addr
        self.__prt = prt
        self.__domain = None

    """ Opens an internet stream to the addr:prt specified. """
    def __start_connection(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.connect((self.__addr, self.__prt))
        self.__respond_to('','Could not open connection to\t' + str(self.__addr), '220')

    """ Begin communications by sending/receiving 'hello' message. """
    def establish_connection(self, domain='mx-aol.mail.gm0.yahoodns.net', using_tls=True):
        self.__domain = domain
        self.__start_connection()
        self.__respond_to('EHLO ' + self.__domain, 'Could not establish connection to\t' + str(self.__addr))   # ESMTP
        if using_tls:
            self.__respond_to('STARTTLS', 'Could not begin TLS encryption to\t' + str(self.__addr), exp_code='220')
            context = ssl.create_default_context()      # allow certifications
            context.load_default_certs()                # using default certifications in the system
            self.__server = context.wrap_socket(self.__server, server_hostname=self.__addr)
            self.__respond_to('EHLO ' + domain, 'Could not establish secure TLS connection to\t' + str(self.__addr))
        print('Successfully established a' + (' secure ' if using_tls else ' ') + 'connection to ' + self.__addr)

    """ Logs into the server using provided credentials """
    def log_in(self, user, pswd, auth='PLAIN'):
        wrap = '' if auth!='PLAIN' else '\x00'
        u64 = base64.b64encode((wrap + user + wrap).encode())
        self.__server.send(('AUTH ' + auth + ' ').encode() + u64 + END.encode())
        resp = self.__decode_receive()
        if not resp:
            self.__error_report_and_quit()
        if '334' not in resp:
            print('Username is rejected. Try again.')
            return False
        self.__server.send(base64.b64encode((pswd).encode()) + END.encode())
        resp = self.__decode_receive()
        if not resp:
            self.__error_report_and_quit()
        if '235' not in resp:
            print('Authentication unsuccessful. Try again.')
            return False
        print('Successfully logged in to:\t' + user + ' at ' + self.__domain)
        return True

    """ Send an email with a FRM, RCPT, SUBJ, and a MSG """
    def send_email(self, frm='<mmafravi@aol.com>', rcpt='<mmafravi@gmail.com>', subj="Test Email Message",
                   msg='This is a test email' + END + 'Yay, your homework (maybe?) works'):
        # the sender/recipient and subject information
        self.__respond_to('MAIL FROM:' + frm, 'Sender\'s address is rejected.')
        self.__respond_to('RCPT TO:' + rcpt, 'Recipient\'s address is rejected.')
        self.__respond_to('DATA', 'Cannot start message.', exp_code='354')
        # the message
        self.__respond_to('SUBJECT:' + subj + END + END + msg + END + END + sign + '.', '')          # end the message
        print('Message sent to\t' + rcpt)

    """ Close the connection. """
    def close(self):
        self.__respond_to('QUIT', 'Server rejected exit command.', exp_code='221')
        self.__server.shutdown(socket.SHUT_RD)          # no more proc
        self.__server.close()
        print('Closed connection.')

    """ Decodes the message received from base64. """
    def __decode_receive(self, buff_size=2048):         # in bytes
        return self.__server.recv(buff_size).decode()   # decode from base64

    """ Send a message (if any), and report errors (if any) """
    def __respond_to(self, msg, msg_on_fail, exp_code='250'):
        if msg!='':                                     # data to send, in ASCII
            # print('SENT:\t' + str(msg))
            msg = (msg+END).encode('ascii')
            self.__server.send(msg)
        response = self.__decode_receive()
        # print('RESP:\t' + response)
        if not response:                                # connection closed?
            self.__error_report_and_quit()
        if exp_code not in response:                    # msg not received?
            self.__error_report_and_quit(msg_on_fail)

    """ Report error message to console and quit program. """
    def __error_report_and_quit(self, msg='Connection was closed.'):
        print('ERROR: ' + msg + '\nProgram terminating...')
        exit(1)

    """ Getters """
    def get_address(self):
        return self.__addr

    def get_domain(self):
        return self.__domain
