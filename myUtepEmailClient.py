""" Using sockets, connect to campus SMTP mail server.
    Then implement the SMTP conversations in the python program,
      which will contact with the server to send your email
      to "your_email@utep.edu". """
import client

addr='smtp.office365.com'
prt=587

if __name__ == '__main__':
    # open the (secure) connection
    clnt = client.EmailClient(addr=addr, prt=prt)
    path_to_cas = input('Enter the path to the directory/file with CAs stored as PEM(s):\t')
    clnt.establish_connection(path_to_cas, domain='1417249971.mail.outlook.com')   # from NSLOOKUP

    # log in to user-provided credentials
    msg = '504'; user = None
    while '504' in msg:         # login info is incorrect
        user = input('Enter your username for ' + clnt.get_domain() + ':\t')
        pswd = input('Enter your password for ' + user + ':\t')
        msg = clnt.log_in(user, pswd, auth='LOGIN')
        print(msg)
    print('Successfully logged in to:\t' + user + ' at ' + clnt.get_address())

    # send a test email
    clnt.send_email(frm='<mafravi@miners.utep.edu>')

    clnt.close()
