# Assignment #2

In this task, you will be implementing a python-based simple mail client, which can send email to any recipient. Your email client should connect to a mail server and communicate using the SMTP protocol.

_Note_: You are not allowed to use the `smtplib` python library.

## Part I
Using sockets, connect to campus SMTP mail server. Then implement the smtp conversations in the python program `myUtepEmailClient` which will contact with the server to send your email to "your_email@utep.edu". 
- From [Microsoft's website](https://support.microsoft.com/en-us/office/pop-and-imap-email-settings-for-outlook-8361e398-8af4-4e97-b147-6c6c4ac95353?ui=en-us&rs=en-us&ad=us), the following settings are used for UTEP's Office365 SMTP settings:
    - Server: smtp.office365.com
    - Port: 587
    - Encryption: STARTTLS
- To create the mail server, I followed [this Python socket tutorial](https://realpython.com/python-sockets/)
- For the syntax on socket communications when it comes to logging in, I used [this resource on SMTP commands](https://blog.mailtrap.io/smtp-commands-and-responses/) to format my commands.
    - does UTEP have issues because of SSO?
    - or is it a setting I'd need to contact tech support for? (see [this](https://docs.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/authenticated-client-smtp-submission) for more infoormation)

## Part II
Using sockets, connect to a popular webmail server, like AOL mail server. Then perform the same task as Part-I and implement the smtp conversations in the python program `myExternalEmailClient.py` which will contact with the SMTP server to send your email to "your_email@gmail.com".
- From [Microsoft's website](https://support.microsoft.com/en-us/office/pop-and-imap-email-settings-for-outlook-8361e398-8af4-4e97-b147-6c6c4ac95353?ui=en-us&rs=en-us&ad=us), the following settings are used for UTEP's Office365 SMTP settings:
    - Server: smtp.aol.com
    - Port: 587
    - Encryption: TLS
- In addition to the commands list in Part 1, to connect to `smtp.aol.com` server, [this page on examples for commands in SMTP communications](http://shareviewsnative.blogspot.com/2012/10/501-551-heloehlo-requires-domain-address.html)
- I also used [this resource](https://www.samlogic.net/articles/smtp-commands-reference.htm) to debug my `AUTH LOGIN` errors

## Reference
- [4 Ways to Check Email Flow using SMTP Commands](https://medium.com/@david07russel/4-ways-to-check-email-flow-using-smtp-commands-caee57a8e68e)
- [List of All SMTP Commands and Response Codes](https://blog.mailtrap.io/smtp-commands-and-responses/)
- [ShellHacks: Command-Line Tips and Tricks](https://www.shellhacks.com/send-email-smtp-server-command-line/)
