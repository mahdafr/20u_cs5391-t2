# Assignment #2

In this task, you will be implementing a python-based simple mail client, which can send email to any recipient. Your email client should connect to a mail server and communicate using the SMTP protocol.

_Note_: You are not allowed to use the `smtplib` python library.

## Part I
Using sockets, connect to campus SMTP mail server. Then implement the smtp conversations in the python program `myUtepEmailClient` which will contact with the server to send your email to "your_email@utep.edu". 
- From [Microsoft's website](https://support.microsoft.com/en-us/office/pop-and-imap-email-settings-for-outlook-8361e398-8af4-4e97-b147-6c6c4ac95353?ui=en-us&rs=en-us&ad=us), the following settings are used for UTEP's Office365 SMTP settings:
    - Server: __smtp.office365.com__
    - Domain: __1417249971.mail.outlook.com__ (_from the NSLOOKUP command for domain `miners.utep.edu`_)
    - Port: __587__
    - Encryption: __STARTTLS__
- To create the mail client, I followed [this Python socket tutorial](https://realpython.com/python-sockets/) to better understand the socket commands
- For the syntax on socket communications when it comes to logging in to an SMTP mail server, I used [this resource on SMTP commands](https://blog.mailtrap.io/smtp-commands-and-responses/) to format my commands.
- However, there arose some issues when connecting to UTEP's domain mail server:
    - when starting TLS (encrypted connection)
    - does UTEP have issues because of SSO?
        - likely no if I can access the `miners.utep.edu` domain
    - or is it a setting I'd need to contact tech support/admin for? (see [this](https://docs.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/authenticated-client-smtp-submission) for more information)
        - all search results lead to this being the issue when attempting to login to my UTEP account through SMTP lines of communication (both on the command and in the scripts in this project)
    - in fact, the issue was in my sequence of calls to securing the connection:
        - `STARTTLS` must be sent to the server once the client establishes the secure TLS connection in order to make the handshake
        - then, re-connecting to the domain with the secure connection allowed the client to progress to the next stage of authentication
- Connecting to [UTEP's VPN](https://vpn.utep.edu) allows the client to successfully log in with UTEP credentials, with the username including the `miners.utep.edu` full domain.

## Part II
Using sockets, connect to a popular webmail server, like AOL mail server. Then perform the same task as Part-I and implement the smtp conversations in the python program `myExternalEmailClient.py` which will contact with the SMTP server to send your email to "your_email@gmail.com".
- From [Microsoft's website](https://support.microsoft.com/en-us/office/pop-and-imap-email-settings-for-outlook-8361e398-8af4-4e97-b147-6c6c4ac95353?ui=en-us&rs=en-us&ad=us), the following settings are used for AOL's SMTP settings:
    - Server: __smtp.aol.com__
    - Domain: __mx-aol.mail.gm0.yahoodns.net__ (_from the NSLOOKUP command for domain `smtp.aol.com`_)
    - Port: __587__
    - Encryption: __TLS__
- From [Microsoft's website](https://support.microsoft.com/en-us/office/pop-and-imap-email-settings-for-outlook-8361e398-8af4-4e97-b147-6c6c4ac95353?ui=en-us&rs=en-us&ad=us), the following settings are used for GMail's SMTP settings:
    - Server: __smtp.gmail.com__
    - Domain: __dns-admin.google.com__ (_from the NSLOOKUP command for domain `smtp.gmail.com`_)
    - Port: __587__
    - Encryption: __TLS__
- In addition to the commands list in Part 1, to connect to `smtp.aol.com` server,
    - I used [this page](https://www.samlogic.net/articles/smtp-commands-reference.htm) for the examples of commands in SMTP communications
    - I fixed my bug in logging in by following the solution to [this page](http://shareviewsnative.blogspot.com/2012/10/501-551-heloehlo-requires-domain-address.html) to debug my `AUTH PLAIN` errors and ended up using `AUTH LOGIN` for more security
    - I also followed the instructions in [this page](https://www.ndchost.com/wiki/mail/test-smtp-auth-telnet) to see if I can actually send an email through SMTP on the command line.

## Security
For the security aspect of this assignment, I followed these steps to allow for a secure TLS connection:
- I used the Python [SSL library](https://docs.python.org/3/library/ssl.html#module-ssl) to secure the connection with TLS encryption
    - [This Microsoft page](https://docs.microsoft.com/en-us/dotnet/framework/wcf/feature-details/how-to-view-certificates-with-the-mmc-snap-in) helped me to find the locations of all certificates on my system
    - But, instead of hard-coding the location, I used the `load_default_certs()` method of the Python SSL library. This requires creating a (default) context (instead of using the deprecated `wrap_socket()` function).
- On the server side, this requires removing 2FA (2 Factor Authentication) on accounts. Settings must also have Less Secure App Access enabled.
    - I could not adjust the settings for my AOL account (security options were not available to me in my new account) and therefore could not send an email through it.
    - But with GMail this was able to be completed and emails were successfully sent and received.

## Reference
- [4 Ways to Check Email Flow using SMTP Commands](https://medium.com/@david07russel/4-ways-to-check-email-flow-using-smtp-commands-caee57a8e68e)
- [List of All SMTP Commands and Response Codes](https://blog.mailtrap.io/smtp-commands-and-responses/)
- [ShellHacks: Command-Line Tips and Tricks](https://www.shellhacks.com/send-email-smtp-server-command-line/)
