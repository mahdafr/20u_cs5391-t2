""" Using sockets, connect to a popular webmail server,
      like AOL mail server.
    Then, perform the same task as Part I
      and implement the SMTP conversations in the python program
      which will contact with the SMTP server to send your email
      to "your_email@gmail.com"."""
import client

if __name__ == '__main__':
    # open the (secure) connection, using generic AOL SMTP server info
    clnt = client.EmailClient(addr='smtp.gmail.com')
    clnt.establish_connection(domain='dns-admin.google.com')

    # log in to user-provided credentials
    success = False
    while not success:
        user = input('Enter your username for ' + clnt.get_domain() + ':\t')
        pswd = input('Enter your password for ' + user + ':\t')
        success = clnt.log_in(user, pswd, auth='LOGIN')

    # send a test email
    clnt.send_email(rcpt='<mafravi@miners.utep.edu>')

    clnt.close()
