import random
import sys
from Tkinter import *
import os
import pickle

ASCII_UPPER_RANGE=127
ASCII_LOWER_RANGE = 65
BLOCK_SIZE = 8
global key, IV, EncryptedText


# Encrypt plain text block of size = BLOCK_SIZE
def encrypt_block(plaintextList, keyList):
    outputList = []
    for (i, j) in zip(plaintextList, keyList):
        outputList.append(i ^ j)
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


def Encrpyt_all_blocks(plaintext, key):
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
    EncryptionFile = open(filename, 'r')
    fileContent = EncryptionFile.readlines()
    EncryptionFile.close()

    key = keyGenerator()

    IV = []
    EncryptedText = []
    Final = []
    for i,line in enumerate(fileContent):
        IV.append(None)
        EncryptedText.append(None)
        IV[i], EncryptedText[i] = Encrpyt_all_blocks(line[:-1], key)
        tempiv = ''.join(convert_to_chars(IV[i]))
        Final.append([tempiv,EncryptedText[i]])
    keyFile = ''.join(convert_to_chars(key))
    keyText = keyFile
    keyFile = list(keyFile)
    EncryptionFile = open(filename, 'w')
    pickle.dump(keyFile, EncryptionFile)
    for line in Final:
        pickle.dump(line,EncryptionFile)
    EncryptionFile.close()
    return keyText

def Decrypt_File(filename,keyFile=None):
    DecryptionFile = open(filename, 'r')
    keyFile = pickle.load(DecryptionFile)
    key = convert_block(keyFile)
    DecryptedText = []
    while True:
        try:
            msg = pickle.load(DecryptionFile)
        except EOFError:
            break
        IVFile = msg[0]
        line = msg[1]
        IV = convert_block(list(IVFile))
        DecryptedText.append(remove_nulls(Decrypt_all_blocks(line, key, IV)))


    DecryptionFile = open(filename, 'w')
    for line in DecryptedText:
        DecryptionFile.write((line+"\n"))
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

def TextButton(event, choice,entry1,entry2,label2,status):
    global key, IV, EncryptedText
    if (choice == 1):
        message = entry1.get()
        key = keyGenerator()
        # msg=''
        # msg=msg+"Key="+key+"\n"
        IV, EncryptedText = Encrpyt_all_blocks(message, key)
        # msg=msg+"Encrypted Text = "+EncryptedText+"\n"
        msg=''
        keyString=''
        for x in key:
            keyString+=chr(x)
        msg+=keyString
        IVString=''
        for x in IV:
            IVString+=chr(x)
        msg+=IVString
        msg+=EncryptedText
        label2.configure(text="Encrypted Text")
        entry2.insert(0, msg)
        status.configure(text="Encryption complete.....")
        print msg
    else:
        # def DecryptTextButton(event):
        entry2.delete(0, 'end')
        msg=entry1.get()
        print msg
        keyList=[]
        for x in range(0,8):
            keyList.append(ord(msg[x]))
        print keyList
        IVList=[]
        for x in range(8,16):
            IVList.append(ord(msg[x]))
        print IVList
        # text1.delete('1.0',END)
        EncryptedTextActual = msg[16:]
        DecryptedText = remove_nulls(Decrypt_all_blocks(EncryptedTextActual, keyList, IVList))
        label2.configure(text="Decrypted Text")
        entry2.insert(0, DecryptedText)
        status.configure(text="Decryption complete.....")
        print DecryptedText


def option1():

    root = Tk()

    InitializeMenu(root)

    Frame1=Frame(root)
    Frame1.pack(fill=BOTH,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    Frame2=Frame(root)
    Frame2.pack(fill=BOTH,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    Frame3=Frame(root)
    Frame3.pack(fill=X,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    BottomFrame=Frame(root)
    BottomFrame.pack(fill=X,side=BOTTOM)

    label1 = Label(Frame1, text="Enter the text   ")
    label1.pack(side=LEFT,fill=BOTH,expand=True)

    entry1 = Entry(Frame1)
    entry1.pack(side=RIGHT,fill=BOTH,expand=True)

    label2 = Label(Frame2, text="Encrypted Text")
    label2.pack(side=LEFT,fill=BOTH,expand=True)

    entry2 = Entry(Frame2)
    entry2.pack(side=RIGHT,fill=BOTH,expand=True)

    button1 = Button(Frame3, text="Encrypt")
    button1.pack(side=LEFT,fill=BOTH,expand=True,padx=10)
    button1.bind("<Button-1>", lambda event: TextButton(event, 1,entry1,entry2,label2,status))
    button2 = Button(Frame3, text="Decrypt")
    button2.pack(side=LEFT,fill=BOTH,expand=True,padx=10)
    button2.bind("<Button-1>", lambda event: TextButton(event, 2,entry1,entry2,label2,status))
    button3 = Button(Frame3, text="Exit",command=root.destroy)
    button3.pack(side=LEFT,fill=BOTH,expand=True,padx=10)


    status=Label(BottomFrame, text="Ready ......",bd=1,relief=SUNKEN,anchor=W)
    status.pack(side=BOTTOM,fill=X)

    '''
    button1=Button(root,text="Encrypt",command="EncryptTextButton")
    button1.pack(row=2,column=2)
    button2=Button(root,text="Encrypt",command="EncryptTextButton")
    button2.pack(row=2,column=2)
    button3=Button(root,text="Encrypt",command="EncryptTextButton")
    button3.pack(row=2,column=2)
    '''
    root.mainloop

hello= Tk()


def TextButton2(event,choice,entry1,status):

    if(choice==1):
        fileName=entry1.get()
        keyText = Encrypt_File(fileName)
        status.configure(text="Encryption complete.....")

    else:
        fileName=entry1.get()
        KeyText = None
        #Take the key input from a text box HERE and replace keyText with that value.
        Decrypt_File(fileName,KeyText)
        status.configure(text="Decryption complete.....")


def option2():
    root = Tk()

    InitializeMenu(root)

    Frame1=Frame(root)
    Frame1.pack(fill=BOTH,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    Frame2=Frame(root)
    Frame2.pack(fill=BOTH,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    Frame3=Frame(root)
    Frame3.pack(fill=X,expand=True,pady=10,ipadx=10,padx=10,ipady=5)

    BottomFrame=Frame(root)
    BottomFrame.pack(fill=X,side=BOTTOM)

    label1 = Label(Frame1, text="Enter the file's name \n(WITH EXTENSION) ")
    label1.pack(side=LEFT,fill=BOTH,expand=True)

    entry1 = Entry(Frame1)
    entry1.pack(side=RIGHT,fill=BOTH,expand=True)


    button1 = Button(Frame3, text="Encrypt")
    button1.pack(side=LEFT,fill=BOTH,expand=True,padx=10)
    button1.bind("<Button-1>", lambda event: TextButton2(event, 1,entry1,status))
    button2 = Button(Frame3, text="Decrypt")
    button2.pack(side=LEFT,fill=BOTH,expand=True,padx=10)
    button2.bind("<Button-1>", lambda event: TextButton2(event, 2,entry1,status))
    button3 = Button(Frame3, text="Exit",command=root.destroy)
    button3.pack(side=LEFT,fill=BOTH,expand=True,padx=10)


    status=Label(BottomFrame, text="Ready ......",bd=1,relief=SUNKEN,anchor=W)
    status.pack(side=BOTTOM,fill=X)



def TextButton3(event, option, entry1, status):

    if option==1:
        path=entry1.get()
        originalDirectory=os.getcwd()
        os.chdir(path)
        for fileName in os.listdir(os.getcwd()):
            EncryptionFile = open(fileName, 'r')
            content = EncryptionFile.readline()
            fileContent = ''
            while (content):
                fileContent += content
                content = EncryptionFile.readline()
            EncryptionFile.close()

            key = keyGenerator()
            # msg=''
            # msg=msg+"Key="+key+"\n"
            IV, EncryptedText = Encrpyt_all_blocks(fileContent, key)
            # msg=msg+"Encrypted Text = "+EncryptedText+"\n"
            msg = EncryptedText
            status.configure(text="Encryption complete.....")
            print msg
            EncryptionFile = open(fileName, 'w')
            keyFile = ','.join(str(x) for x in key)
            IVFile = ','.join(str(x) for x in IV)

            EncryptionFile.write(keyFile + "\n")
            EncryptionFile.write(IVFile + "\n")
            EncryptionFile.write(msg)
            EncryptionFile.close()

        os.chdir(originalDirectory)

    else:
        originalDirectory = os.getcwd()
        path=entry1.get()
        os.chdir(path)
        for fileName in os.listdir(os.getcwd()):
            DecryptionFile = open(fileName, 'r')
            keyFile = DecryptionFile.readline()
            IVFile = DecryptionFile.readline()
            key = keyFile.split(',')
            IV = IVFile.split(',')
            for i in range(0, 8):
                key[i] = int(key[i])
                IV[i] = int(IV[i])
            msg = ''
            for line in DecryptionFile:
                msg += line
                # def DecryptTextButton(event):
            # entry2.delete(0, 'end')
            # text1.delete('1.0',END)
            DecryptedText = remove_nulls(Decrypt_all_blocks(msg, key, IV))
            # msg=''
            # msg=msg+"Decrypted Text = "+DecryptedText
            # msg = DecryptedText
            # label2.configure(text="Decrypted Text")
            # entry2.insert(0, msg)
            status.configure(text="Decryption complete.....")
            # print msg
            DecryptionFile.close()

            DecryptionFile = open(fileName, 'w')
            DecryptionFile.write(DecryptedText)

    os.chdir(originalDirectory)


def option3():
    root = Tk()

    InitializeMenu(root)

    Frame1 = Frame(root)
    Frame1.pack(fill=BOTH, expand=True, pady=10, ipadx=10, padx=10, ipady=5)

    Frame2 = Frame(root)
    Frame2.pack(fill=BOTH, expand=True, pady=10, ipadx=10, padx=10, ipady=5)

    Frame3 = Frame(root)
    Frame3.pack(fill=X, expand=True, pady=10, ipadx=10, padx=10, ipady=5)

    BottomFrame = Frame(root)
    BottomFrame.pack(fill=X, side=BOTTOM)

    label1 = Label(Frame1, text="Enter the path name ")
    label1.pack(side=LEFT, fill=BOTH, expand=True)

    entry1 = Entry(Frame1)
    entry1.pack(side=RIGHT, fill=BOTH, expand=True)

    button1 = Button(Frame3, text="Encrypt")
    button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    button1.bind("<Button-1>", lambda event: TextButton3(event, 1, entry1, status))
    button2 = Button(Frame3, text="Decrypt")
    button2.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    button2.bind("<Button-1>", lambda event: TextButton3(event, 2, entry1, status))
    button3 = Button(Frame3, text="Exit", command=root.destroy)
    button3.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    status = Label(BottomFrame, text="Ready ......", bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)





''' First Page'''

def selection():
    sel=var.get()
    if(sel==1):
        option1()
    elif(sel==2):
        option2()
    else:
        option3()



helloLabel1=Label(hello,text = "Choose the feature you want to use")

var=IntVar()

helloRadioButton1=Radiobutton(hello,text="Instant Encryption/Decryption",variable=var,value=1)
helloRadioButton1.pack(side=TOP,padx=10,pady=10,anchor=W)

helloRadioButton2=Radiobutton(hello,text="File Encryption/Decryption",variable=var,value=2)
helloRadioButton2.pack(side=TOP,padx=10,pady=10,anchor=W)

helloRadioButton3=Radiobutton(hello,text="Folder Encryption/Decryption",variable=var,value=3)
helloRadioButton3.pack(side=TOP,padx=10,pady=10,anchor=W)

helloButton1=Button(hello,text="Next",command=selection)
helloButton1.pack(side=RIGHT,padx=10,pady=10)

helloButton2=Button(hello,text="Exit",command=hello.destroy)
helloButton2.pack(side=LEFT,padx=10,pady=10)

hello.mainloop()
