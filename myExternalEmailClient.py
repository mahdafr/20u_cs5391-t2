""" Using sockets, connect to a popular webmail server,
      like AOL mail server.
    Then, perform the same task as Part I
      and implement the SMTP conversations in the python program
      which will contact with the SMTP server to send your email
      to "your_email@gmail.com"."""
import client

if __name__ == '__main__':
    # open the connection, using generic AOL SMTP server info
    server = client.EmailClient()
    server.establish_connection()

    # log in to user-provided credentials
    msg = '504'; user = None
    while '504' in msg:
          user = input('Enter your username for ' + server.get_address() + ':\t')
          pswd = input('Enter your password for ' + user + ':\t')
          msg = server.log_in(user, pswd)
    print('Successfully logged in to:\t' + user + ' at ' + server.get_address())

    # send a test email
    server.send_email()

    server.close()
