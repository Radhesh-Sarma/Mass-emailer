from googleapiclient.discovery import build
from email import encoders
import httplib2
import smtplib
import mimetypes
from oauth2client import file, client, tools
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.mime.application import MIMEApplication
from email.message import Message
import base64
import os
from apiclient import errors, discovery #needed for gmail service

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text,'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message_no_attachment = base64.urlsafe_b64encode(message.as_bytes())
    raw_message_no_attachment = raw_message_no_attachment.decode()
    body = {'raw': raw_message_no_attachment}
    return body

def create_message_with_attachment(
    sender, to, subject, message_text, file):
    """Create a message for an email.

      Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file: The path to the file to be attached.

      Returns:
        An object containing a base64url encoded email object.
    """


	 #-----About MimeTypes:
    	 # It tells gmail which application it should use to read the attachement (it acts like an 		   extension for windows).
   	 # If you dont provide it, you just wont be able to read the attachement (eg. a text) 		   within gmail. You'll have to download it to read it (windows will know how to read 		   it with it's extension).
	
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text, 'html')
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)
	#If the extension is not recognized it will return: (None, None)
    # If it's an .mp3, it will return: (audio/mp3, None) (None is for the encoding)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file, 'r')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'application' and sub_type == 'pdf':
         fp = open(file,'rb')
         msg = MIMEApplication(temp.read(),_sub_type)
         temp.close()
    else:
        msg = MIMEBase(main_type, sub_type)
        fp = open(file, 'rb')
        msg.set_payload(fp.read())
        fp.close()

    encoders.encode_base64(msg)
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    message_as_bytes = message.as_bytes()
    message_as_base64 = base64.urlsafe_b64encode(message_as_bytes)
    raw = message_as_base64.decode()
    
    return {'raw': raw}
def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """

   
    try:
        message_sent= (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message_sent['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: {error}')





# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.send'

def send_mail(mail):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    http=httplib2.Http()
    http=creds.authorize(http)
    service = discovery.build('gmail', 'v1', http=http)

    sender = mail['sender']
    reciever = mail['reciever']
    subject = mail['subject']
    msg_text = mail['body']
    attach=mail['file']
    if(attach=='0'):
        attach=None

    #msg = create_message(sender, reciever, subject, msg_text)
    if (attach != None) :
        msg = create_message_with_attachment(sender, reciever, subject, msg_text, attach)
        try :
        	send_message(service, "me", msg)
       	except :
       		print ('ERROR : ' + mail[reciever])
    else:
        msg = create_message(sender, reciever, subject, msg_text)
        send_message(service, "me", msg)
