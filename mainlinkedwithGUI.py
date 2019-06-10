from email_sender import send_mail

tempFile = open("tempData.dat","r")

mail = {}
mail['sender'] = 'chinmaygupta3@gmail.com'
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

#write sender email,receiver email,subject,body, path of file attachment above'
send_mail(mail)
