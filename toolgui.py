import random
import sys
from Tkinter import *
import os
import pickle
from tkFileDialog import askopenfilename

ASCII_UPPER_RANGE=127
ASCII_LOWER_RANGE = 65
BLOCK_SIZE = 8
global key, IV, EncryptedText,fileName


# Encrypt plain text block of size = BLOCK_SIZE
def encrypt_block(plaintextList, keyList):
    outputList = []
    for (i, j) in zip(plaintextList, keyList):
        r = i^j
        outputList.append(r)
    return outputList


#Generates a random key sequence
def keyGenerator():
    key=[]
    for i in range(0,BLOCK_SIZE):
        key.append(random.randrange(ASCII_LOWER_RANGE,ASCII_UPPER_RANGE))
    return key

#Sets length of plaintext to be divisible by BLOCK_SIZE
def set_length(plaintext):
    while (len(plaintext)%BLOCK_SIZE)!=0:
        plaintext = chr(0)+plaintext
    return plaintext


# Convert a string (plaintext) to a list each containing a list of 8 characters each. --> [[1,2,3,4,5,6,7,8],[...],[...],.....]
def convert_to_block(plaintext):
    plaintext = set_length(plaintext)
    plaintext_list = []
    for i in range(0, len(plaintext), 8):
        block = []
        for j in range(0, 8):
            block.append(plaintext[i + j])
        plaintext_list.append(block)
    # print plaintext_list
    return plaintext_list


# Decrypt Cipher block of size = BLOCK_SIZE
def decrypt_block(cipher_block, key_block):
    decrpyted = []
    for (c, k) in zip(cipher_block, key_block):
        decrpyted.append(c ^ k)
    return decrpyted


#Convert the list of blocks of 8 characters to their equivalent integer form
def convert_block(block):
    result = []
    for character in block:
        temp = ord(str(character))
        result.append(temp)
    return result

def convert_to_ASCII(plaintext_list):
    ASCII_list = []
    for i,block in enumerate(plaintext_list):
        ASCII_list.append(convert_block(block))
    return ASCII_list


# Converts a list of numbers to their corresponding characters. Has to be done individually for each block.
def convert_to_chars(message):
    finalMessage = []
    for i in message:
        finalMessage.append(chr(i))
    return finalMessage


def convert_all_blocks_to_chars(messageList):
    result = []
    for message in messageList:
        result.extend(convert_to_chars(message))
    resultString = ''.join(result)
    return resultString


# Removes all Null values added to pad a string to required block size
def remove_nulls(decrypted):
    count = 0
    for c in decrypted:
        if c == chr(0):
            count += 1
        else:
            break
    if not count < 0:
        return decrypted[count:]
    else:
        return decrypted


def XOR_previous_block(plaintext_block, IV):
    outputList = []
    for (i, j) in zip(plaintext_block, IV):
        outputList.append(i ^ j)
    return outputList


def Encrypt_all_blocks(plaintext, key):
    plaintext_list = convert_to_block(plaintext)
    Bit_List = convert_to_ASCII(plaintext_list)
    IV = keyGenerator()
    temp = IV[:]
    cipher = []
    for block in Bit_List:
        AfterXOR = XOR_previous_block(block, temp)
        cipher_block = encrypt_block(AfterXOR, key)
        cipher.append(cipher_block)
        temp = cipher_block
    EncryptedText = convert_all_blocks_to_chars(cipher)
    return IV, EncryptedText


def Decrypt_all_blocks(ciphertext, key, IV):
    ciphertext_list = convert_to_block(ciphertext)
    Bit_List = convert_to_ASCII(ciphertext_list)
    plain = []
    temp = IV[:]
    for block in Bit_List:
        AfterDecrypt = decrypt_block(block, key)
        plain_block = XOR_previous_block(AfterDecrypt, temp)
        plain.append(plain_block)
        temp = block
    DecryptedText = convert_all_blocks_to_chars(plain)
    return DecryptedText

#File Encryption and Decryption using Pickle
def Encrypt_File(filename):
    try:
        EncryptionFile = open(filename, 'r')
    except IOError:
        raise IOError
    fileContent = EncryptionFile.read()
    EncryptionFile.close()

    key = keyGenerator()

    IV, EncryptedText = Encrypt_all_blocks(fileContent,key)
    tempiv = ''.join(convert_to_chars(IV))
    Final = tempiv+EncryptedText
    #for i,line in enumerate(fileContent):
        #IV.append(None)
       # EncryptedText.append(None)
        #IV[i], EncryptedText[i] = Encrypt_all_blocks(line[:-1], key)

        #Final.append([tempiv,EncryptedText[i]])
    keyFile = ''.join(convert_to_chars(key))
    EncryptionFile = open(filename, 'w')
    #pickle.dump(keyFile, EncryptionFile)
    pickle.dump(Final,EncryptionFile)
    EncryptionFile.close()
    return keyFile

def Decrypt_File(filename,keyFile):
    try:
        DecryptionFile = open(filename, 'r')
    except IOError:
        raise IOError
    #keyFile = pickle.load(DecryptionFile)
    key = convert_block(keyFile)
    msg = pickle.load(DecryptionFile)
    IVFile = msg[0:BLOCK_SIZE]
    line = msg[BLOCK_SIZE:]
    IV = convert_block(list(IVFile))
    DecryptedText = remove_nulls(Decrypt_all_blocks(line, key, IV))


    DecryptionFile = open(filename, 'w')
    DecryptionFile.write((DecryptedText+"\n"))
    DecryptionFile.close()



#Instant Encrypt Decrypt

def func():
    pass

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
        key = keyGenerator()
        # msg=''
        # msg=msg+"Key="+key+"\n"
        IV, EncryptedText = Encrypt_all_blocks(message, key)
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
        print msg
    else:
        # def DecryptTextButton(event):
        msg=entry1.get("1.0",'end-1c')
        print msg
        keyString = keyEntry.get()
        keyList=[]
        for x in range(0,BLOCK_SIZE):
            keyList.append(ord(keyString[x]))
        print keyList
        IVList=[]
        for x in range(0,BLOCK_SIZE):
            IVList.append(ord(msg[x]))
        print IVList
        # text1.delete('1.0',END)
        EncryptedTextActual = msg[BLOCK_SIZE:]
        DecryptedText = remove_nulls(Decrypt_all_blocks(EncryptedTextActual, keyList, IVList))
        label2.configure(text="Decrypted Text")
        entry2.insert(1.0, DecryptedText)
        status.configure(text="Decryption complete.....",bg='light green')
        print DecryptedText


def option1(hello):
    hello.withdraw()
    root = Tk()
    root.title("Message Encrypt/Decrypt")
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    root.geometry("+250+250")
    root.overrideredirect(True)

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

    button1 = Button(Frame2, text="Encrypt")
    button1.grid(row=0,column=0,rowspan = 2,padx=10,sticky=N+E+S+W)
    button1.bind("<Button-1>", lambda event: TextButton(event, 1,entry1,entry2,keyEntry,label2,status))
    button2 = Button(Frame2, text="Decrypt")
    button2.grid(row=0,column=1,rowspan = 2,padx=10,sticky=N+E+S+W)
    button2.bind("<Button-1>", lambda event: TextButton(event, 2,entry1,entry2,keyEntry,label2,status))
    button3 = Button(Frame2, text="Exit")
    button3.bind("<Button-1>", lambda event: ExitScreen(root,hello))
    button3.grid(row=0,column=2,rowspan = 2,padx=10,sticky=N+E+S+W)


    status=Label(root, text="Ready ......", bd=1, relief=SUNKEN, anchor=W, bg='light green', fg='black' )
    status.grid(row=4,sticky=N+E+S+W)

    root.mainloop


def TextButton2(event,choice,entry1,keyEntry, status,fileName):

    #fileName =  entry1.get()
    if(choice==1):

        keyEntry.delete(0, 'end')
        try:
            keyText = Encrypt_File(fileName)
        except IOError:
            status.configure(text="File Not Found.....",bg='red')
            return
        keyEntry.insert(0,keyText)
        status.configure(text="Encryption complete.....",bg='light green')

    else:

        KeyText = keyEntry.get()
        #Take the key input from a text box HERE and replace keyText with that value.
        try:
            Decrypt_File(fileName,KeyText)
        except IOError:
            status.configure(text="File Not Found.....",bg='red')
            return
        status.configure(text="Decryption complete.....",bg='light green')

def getFileName(root,entry1):
    global fileName
    root.withdraw()
    fileName = askopenfilename(title ='Choose file to Encrypt')
    entry1.insert(0,fileName)
    root.deiconify()

def option2(hello):
    global fileName
    hello.withdraw()
    root = Tk()
    root.title("File Encrypt/Decrypt")
    root.geometry("+250+250")
    root.overrideredirect(True)

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
    bbutton = Button(Frame1, text="Browse")
    bbutton.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    bbutton.bind("<Button-1>", lambda event: getFileName(root,entry1))
    button1 = Button(Frame3, text="Encrypt")
    button1.pack(side=LEFT,fill=BOTH,expand=True,padx=10)
    button1.bind("<Button-1>", lambda event: TextButton2(event, 1,entry1,keyEntry,status,fileName))
    button2 = Button(Frame3, text="Decrypt")
    button2.pack(side=LEFT,fill=BOTH,expand=True,padx=10)
    button2.bind("<Button-1>", lambda event: TextButton2(event, 2,entry1,keyEntry,status,fileName))
    button3 = Button(Frame3, text="Exit")
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
        for fileName in os.listdir(os.getcwd()):
            keyText = Encrypt_File(fileName)
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
        for fileName in os.listdir(os.getcwd()):
            KeyText = keyEntry.get()
            # Take the key input from a text box HERE and replace keyText with that value.
            Decrypt_File(fileName, KeyText)
        status.configure(text="Folder Decryption complete.....",bg='light green')

    os.chdir(originalDirectory)


def ExitScreen(root, hello):
    hello.deiconify()
    root.destroy()

def option3(hello):
    hello.withdraw()
    root = Tk()
    root.title("Folder Encrypt/Decrypt")
    root.geometry("+250+250")
    root.overrideredirect(True)

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

    button1 = Button(Frame3, text="Encrypt")
    button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    button1.bind("<Button-1>", lambda event: TextButton3(event, 1, entry1,keyEntry, status))
    button2 = Button(Frame3, text="Decrypt")
    button2.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    button2.bind("<Button-1>", lambda event: TextButton3(event, 2, entry1,keyEntry, status))
    button3 = Button(Frame3, text="Exit")
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

helloButton1=Button(hello,text="Instant Encryption/Decryption",bg='light green')
helloButton1.pack(side=TOP,padx=10,pady=10,anchor=W,fill=BOTH,expand=True)
helloButton1.bind("<Button-1>", lambda event: option1(hello))

helloButton2=Button(hello,text="File Encryption/Decryption",bg='light green')
helloButton2.pack(side=TOP,padx=10,pady=10,anchor=W,fill=BOTH,expand=True)
helloButton2.bind("<Button-1>", lambda event: option2(hello))

helloButton3=Button(hello,text="Folder Encryption/Decryption",bg='light green')
helloButton3.pack(side=TOP,padx=10,pady=10,anchor=W,fill=BOTH,expand=True)
helloButton3.bind("<Button-1>", lambda event: option3(hello))
#helloButton1=Button(hello,text="Next",command=selection)
#helloButton1.pack(side=RIGHT,padx=10,pady=10)

helloButton2=Button(hello,text="Exit",command=hello.destroy,bg='red')
helloButton2.pack(side=BOTTOM,padx=10,pady=10,fill=X)

hello.mainloop()
