""" Using sockets, connect to campus SMTP mail server.
    Then implement the SMTP conversations in the python program,
      which will contact with the server to send your email
      to "your_email@utep.edu". """
import client


if __name__ == '__main__':
    # open the (secure) connection
    clnt = client.EmailClient(addr='smtp.office365.com')
    clnt.establish_connection(domain='1417249971.mail.outlook.com')   # from NSLOOKUP

    # log in to user-provided credentials
    user = input('Enter your username for ' + clnt.get_domain() + ':\t')
    pswd = input('Enter your password for ' + user + ':\t')
    clnt.log_in(user, pswd, auth='LOGIN')

    # send a test email
    clnt.send_email(frm='<mafravi@miners.utep.edu>')

    clnt.close()
