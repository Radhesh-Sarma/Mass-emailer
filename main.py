#this script sets the receiver emails,subject,body,attachments of the email and sends the email using the credentials provided 


from email_sender import send_mail
tempFile = open("tempData.dat","r")

mail = {}
mail['sender'] = 'chinmaygupta3@gmail.com'
#Please make sure that the above email file corresponds to the same email as in credentials.json

batchSelect = tempFile.readline().split('\n')
batch=open(str(batchSelect[0]),"r")
mail['reciever'] = (batch.read().split('\n'))[0]

subject=tempFile.readline().split('\n')
mail['subject'] = (str(subject[0]))

attachmentStatus=str((tempFile.readline().split('\n'))[0])
if attachmentStatus==0:
    pass
else:
    attachmentPath=str((tempFile.readline().split('\n'))[0])
    mail['file']=attachmentPath

body=str(tempFile.read())

mail['body'] = body
tempFile.close()


send_mail(mail)
