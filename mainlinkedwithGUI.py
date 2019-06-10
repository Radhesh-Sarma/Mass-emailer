from email_sender import send_mail

tempFile = open("tempData.dat","r")

mail = {}
mail['sender'] = 'f20170886@hyderabad.bits-pilani.ac.in'
batchSelect = tempFile.readline().split('\n')
batch=open(str(batchSelect[0]),"r")
mail['reciever'] = (batch.read().split('\n'))[0]

subject=tempFile.readline().split('\n')
mail['subject'] = (str(subject[0]))

attachmentStatus=str((tempFile.readline().split('\n'))[0])
mail['file']=attachmentStatus

body=str(tempFile.read())

mail['body'] = body
tempFile.close()

#write sender email,receiver email,subject,body, path of file attachment above'
send_mail(mail)
