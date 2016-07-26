import Core
import Encrypt
import Decrypt
import random
import sys
import tkMessageBox
import ttk
from Tkinter import *
import os
import pickle
from tkFileDialog import askopenfilename, askdirectory

ASCII_UPPER_RANGE=127
ASCII_LOWER_RANGE = 65
BLOCK_SIZE = 8
global key, IV, EncryptedText


#Instant Encrypt Decrypt

def func():
    pass

def displayMessage():
    tkMessageBox.showwarning("Application Warning!","Please quit using exit button. ")
    
def InitializeMenu(root):
    menu=Menu(root)
    root.config(menu=menu)
    subMenu=Menu(menu)
    menu.add_cascade(label="File",menu=subMenu)
    subMenu.add_command(label="New Project",command=func)
    subMenu.add_command(label="New ",command=func)
    subMenu.add_separator()
    subMenu.add_command(label="Exit",command=sys.exit)

def TextButton(event, choice,entry1,entry2,keyEntry,label2,status):
    global key, IV, EncryptedText
    entry2.delete(1.0, END)

    if (choice == 1):
        keyEntry.delete(0, 'end')
        message = entry1.get(1.0,END)
        key = Core.keyGenerator()
        # msg=''
        # msg=msg+"Key="+key+"\n"
        IV, EncryptedText = Encrypt.Encrypt_all_blocks(message, key)
        # msg=msg+"Encrypted Text = "+EncryptedText+"\n"
        msg=''
        keyString=''
        for x in key:
            keyString+=chr(x)
        #msg+=keyString
        keyEntry.insert(0,keyString)
        IVString=''
        for x in IV:
            IVString+=chr(x)
        msg+=IVString
        msg+=EncryptedText
        label2.configure(text="Encrypted Text")
        entry2.insert(1.0, msg)
        status.configure(text="Encryption complete.....",bg='light green')
        #print msg
    else:
        # def DecryptTextButton(event):
        msg=entry1.get("1.0",'end-1c')
        #print msg
        keyString = keyEntry.get()
        keyList=[]
        for x in range(0,BLOCK_SIZE):
            keyList.append(ord(keyString[x]))
        #print keyList
        IVList=[]
        for x in range(0,BLOCK_SIZE):
            IVList.append(ord(msg[x]))
        #print IVList
        # text1.delete('1.0',END)
        EncryptedTextActual = msg[BLOCK_SIZE:]
        DecryptedText = Core.remove_nulls(Decrypt.Decrypt_all_blocks(EncryptedTextActual, keyList, IVList))
        label2.configure(text="Decrypted Text")
        entry2.insert(1.0, DecryptedText)
        status.configure(text="Decryption complete.....",bg='light green')
        #print DecryptedText


def option1(hello):
    hello.withdraw()
    root = Tk()
    root.title("Message Encrypt/Decrypt")
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    root.geometry("+250+250")
    root.protocol('WM_DELETE_WINDOW', displayMessage)
    #root.overrideredirect(True)

    InitializeMenu(root)
    Frame1=Frame(root)
    Frame1.grid(row=0, rowspan=3, pady=10,ipadx=10,padx=10,ipady=5,sticky=N+E+S+W)
    Frame1.rowconfigure(0,weight=1)
    Frame1.columnconfigure(0,weight=1)
    Frame1.rowconfigure(2, weight=1)
    Frame1.rowconfigure(3, weight=1)
    Frame1.columnconfigure(1, weight=3)
    """
    KeyFrame = Frame(root)
    KeyFrame.pack(fill=BOTH, expand=True, pady=10, ipadx=10, padx=10, ipady=5)
    """
    Frame2=Frame(root)
    Frame2.grid(row=3, rowspan = 1, pady=10, ipadx=10, padx=10, ipady=5,sticky=N+E+S+W)
    Frame2.rowconfigure(0,weight=1)
    Frame2.columnconfigure(0,weight=1)
    Frame2.columnconfigure(1, weight=1)
    Frame2.columnconfigure(2, weight=1)
    """
    Frame3=Frame(root)
    Frame3.pack(fill=BOTH,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    BottomFrame=Frame(root)
    BottomFrame.pack(fill=X,side=BOTTOM)
    """
    label1 = Label(Frame1, text="Enter the text")
    label1.grid(row=0,column=0,pady=10,ipadx=10,padx=10,ipady=5,sticky=N+E+S+W+W)
    keyLabel = Label(Frame1, text="Key")
    keyLabel.grid(row=2,column=0,pady=10,ipadx=10,padx=10,ipady=5)
    keyEntry = Entry(Frame1)
    keyEntry.grid(row=2,column=1,columnspan=5,pady=10,ipadx=10,padx=10,ipady=5)
    label2 = Label(Frame1, text="Encrypted Text")
    label2.grid(row=3,column=0,pady=10,ipadx=10,padx=10,ipady=5,sticky=N+E+S+W+W)
    entry1 = Text(Frame1,height= 5,width = 50)
    entry1.grid(row=0,column=1,columnspan=5,pady=10,ipadx=10,padx=10,ipady=5,sticky=N+E+S+W)
    entry2 = Text(Frame1,height= 5,width = 50)
    entry2.grid(row=3,column=1,columnspan=5,pady=10,ipadx=10,padx=10,ipady=5,sticky=N+E+S+W)

    button1 = ttk.Button(Frame2, text="Encrypt")
    button1.grid(row=0,column=0,rowspan = 2,padx=10,sticky=N+E+S+W)
    button1.bind("<Button-1>", lambda event: TextButton(event, 1,entry1,entry2,keyEntry,label2,status))
    button2 = ttk.Button(Frame2, text="Decrypt")
    button2.grid(row=0,column=1,rowspan = 2,padx=10,sticky=N+E+S+W)
    button2.bind("<Button-1>", lambda event: TextButton(event, 2,entry1,entry2,keyEntry,label2,status))
    button3 = ttk.Button(Frame2, text="Exit")
    button3.bind("<Button-1>", lambda event: ExitScreen(root,hello))
    button3.grid(row=0,column=2,rowspan = 2,padx=10,sticky=N+E+S+W)


    status=Label(root, text="Ready ......", bd=1, relief=SUNKEN, anchor=W, bg='light green', fg='black' )
    status.grid(row=4,sticky=N+E+S+W)
    root.mainloop

def TextButton2(event,choice,entry1,keyEntry,status):
    fileName =  entry1.get()
    if(choice==1):
        keyEntry.delete(0, 'end')
        try:
            keyText = Encrypt.Encrypt_File(fileName)
        except IOError:
            status.configure(text="File Not Found.....",bg='red')
            return
        keyEntry.insert(0,keyText)
        status.configure(text="Encryption complete.....",bg='light green')

    else:
        #status.configure(text="Decrypting.....", bg='orange')
        KeyText = keyEntry.get()
        #Take the key input from a text box HERE and replace keyText with that value.
        try:
            Decrypt.Decrypt_File(fileName,KeyText)
        except IOError:
            status.configure(text="File Not Found.....",bg='red')
            return
        status.configure(text="Decryption complete.....",bg='light green')

def getFileName(root,entry1):
    root.iconify()
    fileName = askopenfilename(title ='Choose file to Encrypt/Decrypt',initialdir = 'C:')
    entry1.insert(0,fileName)
    root.deiconify()

def ExecuteEncrypt(event,choice,entry1,keyEntry,status):
    status.configure(text="Encrypting.....", bg='orange')
    TextButton2(event,choice,entry1,keyEntry,status)

def ExecuteDecrypt(event,choice,entry1,keyEntry,status):
    status.configure(text="Decrypting.....", bg='orange')
    TextButton2(event,choice,entry1,keyEntry,status)


def option2(hello):
    global fileName
    hello.withdraw()
    root = Tk()
    root.title("File Encrypt/Decrypt")
    root.geometry("+250+250")
    #root.overrideredirect(True)
    root.protocol('WM_DELETE_WINDOW',displayMessage)
    InitializeMenu(root)

    Frame1=Frame(root)
    Frame1.pack(fill=BOTH,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    Frame2=Frame(root)
    Frame2.pack(fill=BOTH,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    KeyFrame = Frame(root)
    KeyFrame.pack(fill=BOTH, expand=True, pady=10, ipadx=10, padx=10, ipady=5)

    Frame3=Frame(root)
    Frame3.pack(fill=X,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    keyLabel = Label(KeyFrame, text="Key")
    keyLabel.pack(side=LEFT, fill=BOTH, expand=True)

    keyEntry = Entry(KeyFrame)
    keyEntry.pack(side=RIGHT, fill=BOTH, expand=True)

    BottomFrame=Frame(root)
    BottomFrame.pack(fill=X,side=BOTTOM)

    label1 = Label(Frame1, text="Enter the file's name \n(WITH EXTENSION) ")
    label1.pack(side=LEFT,fill=BOTH,expand=True)

    entry1 = Entry(Frame1)
    entry1.pack(side=RIGHT,fill=BOTH,expand=True)
    bbutton = ttk.Button(Frame1, text="Browse")
    bbutton.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    bbutton.bind("<Button-1>", lambda event: getFileName(root,entry1))
    button1 = ttk.Button(Frame3, text="Encrypt")
    button1.pack(side=LEFT,fill=BOTH,expand=True,padx=10)
    button1.bind("<Button-1>", lambda event: ExecuteEncrypt(event, 1,entry1,keyEntry,status))
    button2 = ttk.Button(Frame3, text="Decrypt")
    button2.pack(side=LEFT,fill=BOTH,expand=True,padx=10)
    button2.bind("<Button-1>", lambda event: ExecuteDecrypt(event, 2,entry1,keyEntry,status))
    button3 = ttk.Button(Frame3, text="Exit")
    button3.bind("<Button-1>", lambda event: ExitScreen(root,hello))
    button3.pack(side=LEFT,fill=BOTH,expand=True,padx=10)


    status=Label(BottomFrame, text="Ready ......",bd=1,relief=SUNKEN,anchor=W,bg='light green')
    status.pack(side=BOTTOM,fill=X)



def TextButton3(event, option, entry1,keyEntry, status):

    if option==1:
        path=entry1.get()
        keyEntry.delete(0, 'end')
        originalDirectory=os.getcwd()
        try:
            os.chdir(path)
        except WindowsError:
            status.configure(text="Path is invalid!",bg='red')
            return
        keyText = ''.join(Core.convert_to_chars(Core.keyGenerator()))
        DirectoryList = os.listdir(os.getcwd())
        for i,fileName in enumerate(DirectoryList):
            keyText = Encrypt.Encrypt_File(fileName,keyText)
            status.configure(text="Encrypted %d out of %d files"%(i,len(DirectoryList)), bg='orange')
        keyEntry.insert(0,keyText)
        status.configure(text="Folder Encryption complete.....",bg='light green')

    else:
        originalDirectory = os.getcwd()
        path=entry1.get()
        try:
            os.chdir(path)
        except WindowsError:
            status.configure(text="Path is invalid!",bg='red')
            return
        DirectoryList = os.listdir(os.getcwd())
        for i,fileName in enumerate(DirectoryList):
            KeyText = keyEntry.get()
            status.configure(text="Decrypted %d out of %d files" % (i, len(DirectoryList)), bg='orange')
            # Take the key input from a text box HERE and replace keyText with that value.
            Decrypt.Decrypt_File(fileName, KeyText)
        status.configure(text="Folder Decryption complete.....",bg='light green')

    os.chdir(originalDirectory)


def ExitScreen(root, hello):
    hello.deiconify()
    root.destroy()

def getDirectory(root,entry1):
    root.iconify()
    directory = askdirectory(title ='Choose folder to Encrypt/Decrypt',initialdir = 'C:')
    entry1.insert(0,directory)
    root.deiconify()

def option3(hello):
    hello.withdraw()
    root = Tk()
    root.title("Folder Encrypt/Decrypt")
    root.geometry("+250+250")
    root.protocol('WM_DELETE_WINDOW', displayMessage)
    #root.overrideredirect(True)

    InitializeMenu(root)

    Frame1 = Frame(root)
    Frame1.pack(fill=BOTH, expand=True, pady=10, ipadx=10, padx=10, ipady=5)

    Frame2 = Frame(root)
    Frame2.pack(fill=BOTH, expand=True, pady=10, ipadx=10, padx=10, ipady=5)

    KeyFrame = Frame(root)
    KeyFrame.pack(fill=BOTH, expand=True, pady=10, ipadx=10, padx=10, ipady=5)

    Frame3 = Frame(root)
    Frame3.pack(fill=X, expand=True, pady=10, ipadx=10, padx=10, ipady=5)

    BottomFrame = Frame(root)
    BottomFrame.pack(fill=X, side=BOTTOM)

    label1 = Label(Frame1, text="Enter the path name ")
    label1.pack(side=LEFT, fill=BOTH, expand=True)

    entry1 = Entry(Frame1)
    entry1.pack(side=RIGHT, fill=BOTH, expand=True)

    keyLabel = Label(KeyFrame, text="Key")
    keyLabel.pack(side=LEFT, fill=BOTH, expand=True)

    keyEntry = Entry(KeyFrame)
    keyEntry.pack(side=RIGHT, fill=BOTH, expand=True)

    bbutton = ttk.Button(Frame1, text="Browse")
    bbutton.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    bbutton.bind("<Button-1>", lambda event: getDirectory(root, entry1))

    button1 = ttk.Button(Frame3, text="Encrypt")
    button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    button1.bind("<Button-1>", lambda event: TextButton3(event, 1, entry1,keyEntry, status))
    button2 = ttk.Button(Frame3, text="Decrypt")
    button2.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    button2.bind("<Button-1>", lambda event: TextButton3(event, 2, entry1,keyEntry, status))
    button3 = ttk.Button(Frame3, text="Exit")
    button3.bind("<Button-1>", lambda event:ExitScreen(root,hello))
    button3.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    status = Label(BottomFrame, text="Ready ......", bd=1, relief=SUNKEN, anchor=W,bg = 'light green')
    status.pack(side=BOTTOM, fill=X)




''' First Page'''

hello= Tk()
hello.title('CBC Encryption/Decryption Tool')
#hello.overrideredirect(True)
hello.geometry("400x200")
hello.resizable(width=False,height=False)
#hello.wm_attributes("-topmost", True)
#hello.wm_attributes("-disabled", True)
hello.wm_attributes("-transparentcolor", "white")
helloLabel1=Label(hello,text = "Choose the feature you want to use")

helloButton1=ttk.Button(hello,text="Instant Encryption/Decryption")#bg='light green')
helloButton1.pack(side=TOP,padx=10,pady=10,anchor=W,fill=BOTH,expand=True)
helloButton1.bind("<Button-1>", lambda event: option1(hello))

helloButton2=ttk.Button(hello,text="File Encryption/Decryption")#bg='light green')
helloButton2.pack(side=TOP,padx=10,pady=10,anchor=W,fill=BOTH,expand=True)
helloButton2.bind("<Button-1>", lambda event: option2(hello))

helloButton3=ttk.Button(hello,text="Folder Encryption/Decryption")#bg='light green')
helloButton3.pack(side=TOP,padx=10,pady=10,anchor=W,fill=BOTH,expand=True)
helloButton3.bind("<Button-1>", lambda event: option3(hello))
#helloButton1=Button(hello,text="Next",command=selection)
#helloButton1.pack(side=RIGHT,padx=10,pady=10)

helloButtonE=ttk.Button(hello,text="Exit",command=hello.destroy)#bg='red')
helloButtonE.pack(side=BOTTOM,padx=10,pady=10,fill=X)

hello.mainloop()