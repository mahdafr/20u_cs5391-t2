""" Using sockets, connect to campus SMTP mail server.
    Then implement the SMTP conversations in the python program,
      which will contact with the server to send your email
      to "your_email@utep.edu". """
import client

addr='smtp.office365.com'
prt=587

if __name__ == '__main__':
    # open the connection
    server = client.EmailClient(addr=addr, prt=prt)
    server.establish_connection(domain='miners.utep.edu', using_tls=True)

    # log in to user-provided credentials
    msg = '504'; user = None
    while '504' in msg:
        user = input('Enter your username for ' + server.get_address() + ':\t')
        pswd = input('Enter your password for ' + user + ':\t')
        msg = server.log_in(user, pswd, auth='CRAM-MD5')
        print(msg)
    print('Successfully logged in to:\t' + user + ' at ' + server.get_address())

    # send a test email
    server.send_email(frm='mafravi@miners.utep.edu')

    server.close()
