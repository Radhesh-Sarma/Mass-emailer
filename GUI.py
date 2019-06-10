import tkinter
from tkinter import *
window=tkinter.Tk()
window.title("Bulk Email")
window.config(width=640, height=480)

from tkinter.filedialog import askopenfilename


def attachmentSelect():
    attachmentBox.delete(0,END)
    if var.get()==0:
        attachmentBox.config(state=DISABLED)
    else:
        attachmentBox.config(state=NORMAL)
        Tk().withdraw() 
        filename = askopenfilename()
        attachmentBox.insert(0, filename)




#Select Label
batchSelectLabel=tkinter.Label(window, text="Select Batch")
batchSelectLabel.pack()
batchSelectLabel.place(height=50, relx=0.1)

#Subject Label
subjectLabel=tkinter.Label(window, text="Type Subject")
subjectLabel.pack()
subjectLabel.place(height=50, relx=0.5)

#ListBox
batchList=Listbox(window)
batchList.insert(1,"2017")
batchList.insert(2,"2018")
batchList.pack()
batchList.place(height=50, width=200, relx=0.1, rely=0.08)

#Subject Entry Box
subjectBox = Entry(window, exportselection=0, width=50)
subjectBox.pack()
subjectBox.place(relx=0.5, rely=0.08)

#Message Type Label
messageLabel=tkinter.Label(window, text="Type Message Here")
messageLabel.pack()
messageLabel.place(height=50, relx=0.1, rely=0.35)

#Attachment checkbox
var=tkinter.IntVar()
attachmentCheckbox=tkinter.Checkbutton(window, text="Include Attachment",variable=var, command=lambda:attachmentSelect())
attachmentCheckbox.pack()
attachmentCheckbox.place(relx=0.5, rely=0.15)

#Attachment Label
attachmentLabel=tkinter.Label(window, text="Attachment path")
attachmentLabel.pack()
attachmentLabel.place(relx=0.5, rely=0.22)

#Attachment Entry Box
attachmentBox = Entry(window, exportselection=0, width=50)
attachmentBox.pack()
attachmentBox.place(relx=0.5, rely=0.3)


#TextArea
TextArea = Text(window)
ScrollBar = Scrollbar(TextArea)
ScrollBar.config(command=TextArea.yview)
TextArea.config(yscrollcommand=ScrollBar.set)
ScrollBar.pack(side=RIGHT, fill=Y)
TextArea.pack()
TextArea.place(height=200, width=500, relx=0.1, rely=0.45)

#Algorithm: Save contents of TextArea into a temp file. Main Script opens Database that is selected in List and Temp text file and sends Email

#Creating temp file
def extractText():
    batch = batchList.curselection()
    filename="tempData.dat"
    tempFile=open(filename,"w")
    content=TextArea.get("1.0","end-1c")
    subject=subjectBox.get()
    attachmentStatus=var.get()
    attachmentPath=attachmentBox.get()
    tempFile.write(str(batch[0])+"\n"+subject + "\n" + str(attachmentStatus)+ "\n"+ attachmentPath+"\n"+content)
    tempFile.close()


#Button
btnFrame=Frame(window)
sendBtn=tkinter.Button(window, text="Send Email", command=lambda:extractText())
sendBtn.pack()
sendBtn.place(bordermode=OUTSIDE, height=30, width=100, relx=0.7, rely=0.9)

window.mainloop()
