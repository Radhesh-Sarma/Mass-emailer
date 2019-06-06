from email_sender import send_mail
mail = {}
mail['sender'] = 'Your Email'
mail['reciever'] = 'reciever Email'
mail['subject'] = 'demo subject'
mail['body'] = 'demo body'
mail['file'] = 'demo path of file '
#write sender email,receiver email,subject,body, path of file attachment above'
send_mail(mail)
