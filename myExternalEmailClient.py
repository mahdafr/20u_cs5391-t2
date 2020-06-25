""" Using sockets, connect to a popular webmail server,
      like AOL mail server.
    Then, perform the same task as Part I
      and implement the SMTP conversations in the python program
      which will contact with the SMTP server to send your email
      to "your_email@gmail.com"."""
import client

if __name__ == '__main__':
    # open the (secure) connection, using generic AOL SMTP server info
    clnt = client.EmailClient()
    path_to_cas = input('Enter the path to the directory/file with CAs stored as PEM(s):\t')
    clnt.establish_connection(path_to_cas, using_tls=True)

    # log in to user-provided credentials
    msg = '504'; user = None
    while '504' in msg:         # login info is incorrect
          user = input('Enter your username for ' + clnt.get_address() + ':\t')
          pswd = input('Enter your password for ' + user + ':\t')
          msg = clnt.log_in(user, pswd)
    print('Successfully logged in to:\t' + user + ' at ' + clnt.get_domain())

    # send a test email
    clnt.send_email()

    clnt.close()
