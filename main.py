#this script sets the receiver emails,subject,body,attachments of the email and sends the email using the credentials provided 


from email_sender import send_mail
tempFile = open("tempData.dat","r")

mail = {}
mail['sender'] = 'Your Email'
#Please make sure that the above email file corresponds to the same email as in credentials.json

batchSelect = tempFile.readline().split('\n')
batch=open(str(batchSelect[0]),"r")
mail['reciever'] = (batch.read().split('\n'))[0]

subject=tempFile.readline().split('\n')
mail['subject'] = (str(subject[0]))

attachmentStatus=str((tempFile.readline().split('\n'))[0])
if attachmentStatus==1:
    attachmentPath=str((tempFile.readline().split('\n'))[0])
    mail['file']=attachmentPath
else:
    mail['file']='0'

body=str(tempFile.read())

mail['body'] = body
tempFile.close()

HTMLbodyText = "Hi"
for charReader in range(0, len(body)):
    if body[charReader]!='\n':
        HTMLbodyText=HTMLbodyText+body[charReader]
    else:
        HTMLbodyText=HTMLbodyText+"<br>"

mail['body']=HTMLbodyText
        


send_mail(mail)
