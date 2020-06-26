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
    clnt.establish_connection()

    # log in to user-provided credentials
    user = input('Enter your username for ' + clnt.get_domain() + ':\t')
    pswd = input('Enter your password for ' + user + ':\t')
    clnt.log_in(user, pswd)

    # send a test email
    clnt.send_email()

    clnt.close()
