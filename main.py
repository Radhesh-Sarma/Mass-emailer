from email_sender import send_mail
mail = {}
mail['sender'] = 'f20170886@hyderabad.bits-pilani.ac.in'
mail['reciever'] = 'chinmaygupta3@gmail.com,f20170130@goa.bits-pilani.ac.in'
mail['subject'] = 'DEMO SUBJECT'
mail['body'] = 'demo body'
x=input("Enter path to attach file \n Enter 0 if you dont want to attach a file")
mail['file']=x


#write sender email,receiver email,subject,body, path of file attachment above'
send_mail(mail)
