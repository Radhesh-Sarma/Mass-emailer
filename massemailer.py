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
from apiclient import errors, discovery  # needed for gmail service

import tkinter
from tkinter import *
# from sys import exit
import os
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


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
    message = MIMEText(message_text, 'html')
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

    # -----About MimeTypes:
    # It tells gmail which application it should use to read the attachement (it acts like an 		   extension for windows).
    # If you dont provide it, you just wont be able to read the attachement (eg. a text) 		   within gmail. You'll have to download it to read it (windows will know how to read 		   it with it's extension).

    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text, 'html')
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)
    # If the extension is not recognized it will return: (None, None)
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
        message_sent = (service.users().messages().send(userId=user_id, body=message).execute())
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

    http = httplib2.Http()
    http = creds.authorize(http)
    service = discovery.build('gmail', 'v1', http=http)

    sender = mail['sender']
    reciever = mail['reciever']
    subject = mail['subject']
    msg_text = mail['body']
    attach = mail['file']
    if (attach == '0'):
        attach = None

    # msg = create_message(sender, reciever, subject, msg_text)
    if (attach != None):
        msg = create_message_with_attachment(sender, reciever, subject, msg_text, attach)
        try:
            send_message(service, "me", msg)
        except:
            print('ERROR : ' + mail[reciever])
    else:
        msg = create_message(sender, reciever, subject, msg_text)
        send_message(service, "me", msg)


# GUI SCRIPT STARTS HERE --->

window = tkinter.Tk()
window.title("Bulk Email")
window.config(width=640, height=480)


def attachmentSelect():
    attachmentBox.delete(0, END)
    if var.get() == 0:
        attachmentBox.config(state=DISABLED)
    else:
        attachmentBox.config(state=NORMAL)
        Tk().withdraw()
        filename = askopenfilename()
        attachmentBox.insert(0, filename)


# Select Label
batchSelectLabel = tkinter.Label(window, text="Select Batch")
batchSelectLabel.pack()
batchSelectLabel.place(height=50, relx=0.1)

# Subject Label
subjectLabel = tkinter.Label(window, text="Type Subject")
subjectLabel.pack()
subjectLabel.place(height=50, relx=0.5)

# ListBox
batchList = Listbox(window)
batchList.insert(1, " PG DIPLOMA COURSE FOR DISASTER PREPAREDNESS AND REHABILITATION")
batchList.insert(2, "HEALTH PROMOTION THROUGH AYURVEDA AND YOGA COURSE ")
batchList.pack()
batchList.place(height=100, width=200, relx=0.1, rely=0.08)

# Subject Entry Box
subjectBox = Entry(window, exportselection=0, width=50)
subjectBox.pack()
subjectBox.place(relx=0.5, rely=0.08)

# Message Type Label
messageLabel = tkinter.Label(window, text="Type Message Here")
messageLabel.pack()
messageLabel.place(height=50, relx=0.1, rely=0.35)

# Attachment checkbox
var = tkinter.IntVar()
attachmentCheckbox = tkinter.Checkbutton(window, text="Include Attachment", variable=var,
                                         command=lambda: attachmentSelect())
attachmentCheckbox.pack()
attachmentCheckbox.place(relx=0.5, rely=0.15)

# Attachment Label
attachmentLabel = tkinter.Label(window, text="Attachment path")
attachmentLabel.pack()
attachmentLabel.place(relx=0.5, rely=0.22)

# Attachment Entry Box
attachmentBox = Entry(window, exportselection=0, width=50)
attachmentBox.pack()
attachmentBox.place(relx=0.5, rely=0.3)

# TextArea
TextArea = Text(window)
ScrollBar = Scrollbar(TextArea)
ScrollBar.config(command=TextArea.yview)
TextArea.config(yscrollcommand=ScrollBar.set)
ScrollBar.pack(side=RIGHT, fill=Y)
TextArea.pack()
TextArea.place(height=200, width=500, relx=0.1, rely=0.45)


# Algorithm: Save contents of TextArea into a temp file. Main Script opens Database that is selected in List and Temp text file and sends Email


# Creating temp file
def extractText():
    batch = batchList.curselection()
    filename = "tempData.dat"
    tempFile = open(filename, "w")
    content = TextArea.get("1.0", "end-1c")
    subject = subjectBox.get()
    attachmentStatus = var.get()
    attachmentPath = attachmentBox.get()
    tempFile.write(
        str(batch[0]) + "\n" + subject + "\n" + str(attachmentStatus) + "\n" + attachmentPath + "\n" + content)
    tempFile.close()

    tempFile = open("tempData.dat", "r")
    mail = {}
    mail['sender'] = 'Indian Red Cross Society <indianredcrosssociety1@gmail.com>'
    # Please make sure that the above email file corresponds to the same email as in credentials.json

    batchSelect = tempFile.readline().split('\n')
    batch = open(str(batchSelect[0]), "r")
    mail['reciever'] = (batch.read().split('\n'))[0]

    subject = tempFile.readline().split('\n')
    mail['subject'] = (str(subject[0]))

    attachmentStatus = str((tempFile.readline().split('\n'))[0])
    if attachmentStatus == '1':
        attachmentPath = str((tempFile.readline().split('\n'))[0])
        mail['file'] = attachmentPath
    else:
        mail['file'] = '0'

    body = str(tempFile.read())

    # mail['body'] = body
    tempFile.close()

    HTMLbodyText = ""
    for charReader in range(0, len(body)):
        if body[charReader] != '\n':
            HTMLbodyText = HTMLbodyText + body[charReader]
        else:
            HTMLbodyText = HTMLbodyText + "<br>"

    mail['body'] = HTMLbodyText
    send_mail(mail)
    messagebox.showinfo("Success", "Emails sent successfully!")

    os._exit(0)


# Button
btnFrame = Frame(window)
sendBtn = tkinter.Button(window, text="Send Email", command=lambda: extractText())
sendBtn.pack()
sendBtn.place(bordermode=OUTSIDE, height=30, width=100, relx=0.7, rely=0.9)

window.mainloop()


