import Core
import Encrypt
import Decrypt
import sys
import tkMessageBox
import ttk
import os
import time
import traceback

from Tkinter import *
from tkFileDialog import askopenfilename, askdirectory
from PIL import Image, ImageTk


ASCII_UPPER_RANGE=127
ASCII_LOWER_RANGE = 65
BLOCK_SIZE = 8
global key, IV, EncryptedText

#Helper Functions
def func():
    pass

def displayMessage():
    tkMessageBox.showwarning("Application Warning!", "Please quit using exit button. ")

def displayError():
    msg = str(traceback.print_exc())
    tkMessageBox.showwarning("Unknown Error!", "Please report/email the error to any of the authors!\n"+msg)

def askToQuit():
    if tkMessageBox.askyesno("Confirm!", "Do you really want to quit such an awesome program? "):
        sys.exit()

def ExitScreen(root, hello):
    hello.deiconify()
    root.destroy()
    
#Menu for Each Window
def InitializeMenu(root):
    menu=Menu(root)
    root.config(menu=menu)
    subMenu=Menu(menu)
    menu.add_cascade(label="Options",menu=subMenu)
    #subMenu.add_command(label="New Project",command=func)
    #subMenu.add_command(label="New ",command=func)
    subMenu.add_separator()
    subMenu.add_command(label="Exit Application",command=askToQuit)


    
#Main Window
class MainWindow:
    def __init__(self,hello):
        try:
            hello.title('CBC Encryption/Decryption Tool')
            hello.protocol('WM_DELETE_WINDOW', askToQuit)
            self.bg_image = ImageTk.PhotoImage(Image.open("src/bg.png"))
            self.b1_image = ImageTk.PhotoImage(Image.open("src/b1.png"))
            self.b2_image = ImageTk.PhotoImage(Image.open("src/b2.png"))
            self.b3_image = ImageTk.PhotoImage(Image.open("src/b3.png"))
            # exit_image = ImageTk.PhotoImage(Image.open("src/b1.png"))

            w = self.bg_image.width()
            h = self.bg_image.height()
            hello.geometry("%dx%d" % (w, h))
            hello.resizable(width=False, height=False)
            hello.wm_attributes("-transparentcolor", "white")

            self.bglabel = Label(hello, image=self.bg_image)
            self.bglabel.pack(side='top', fill='both', expand='yes')
            self.bglabel.image = self.bg_image

            self.helloLabel1 = Label(self.bglabel, text="Choose the feature you want to use")

            helloButton1 = ttk.Button(self.bglabel, text="Instant Encryption/Decryption", image=self.b1_image)
            helloButton1.pack(side=TOP, padx=10, pady=10, anchor=CENTER, fill=None, expand=True)
            helloButton1.bind("<Button-1>", lambda event: self.option1(hello))

            helloButton2 = ttk.Button(self.bglabel, text="File Encryption/Decryption", image=self.b2_image)
            helloButton2.pack(side=TOP, padx=10, pady=10, anchor=CENTER, fill=None, expand=True)
            helloButton2.bind("<Button-1>", lambda event: self.option2(hello))

            helloButton3 = ttk.Button(self.bglabel, text="Folder Encryption/Decryption", image=self.b3_image)
            helloButton3.pack(side=TOP, padx=10, pady=10, anchor=CENTER, fill=None, expand=True)
            helloButton3.bind("<Button-1>", lambda event: self.option3(hello))

            helloButtonE = ttk.Button(self.bglabel, text="Exit", command=askToQuit)
            helloButtonE.pack(side=BOTTOM, padx=10, pady=10, fill=BOTH)
        except:
            displayError()


    def option1(self, hello):
        hello.iconify()
        root = Toplevel()
        InstantWindow = InstantEnc(root)
        
    def option2(self,hello):
        hello.iconify()
        root2 = Toplevel()
        FileWindow = FileEnc(root2)

    def option3(self, hello):
        hello.iconify()
        root3 = Toplevel()
        FolderWindow = FolderEnc(root3)


#Instant Encrypt Decrypt Window
class InstantEnc:
    def __init__(self,root):
        root.title("Message Encrypt/Decrypt")
        root.protocol('WM_DELETE_WINDOW', displayMessage)
        root.resizable(width=False, height=False)
        self.bg1_image = ImageTk.PhotoImage(Image.open("src/bg3.jpg"))
        self.w = self.bg1_image.width()
        self.h = self.bg1_image.height()
        root.geometry("%dx%d" % (self.w, self.h))
        self.bg1label = Label(root, image=self.bg1_image)
        self.bg1label.pack(side='top', fill='both', expand='yes')
        self.bg1label.image = self.bg1_image

        InitializeMenu(root)
        self.Frame1 = Frame(self.bg1label)
        self.Frame1.pack(fill=X, expand = True, pady=10, padx=10)
 
        self.KeyFrame = Frame(self.bg1label)
        self.KeyFrame.pack(fill=None, expand=True, pady=10, padx=10)

        self.Frame2 = Frame(self.bg1label)
        self.Frame2.pack(fill=X, expand=True, pady=10, padx=10)

        self.Frame3 = Frame(self.bg1label)
        self.Frame3.pack(fill=X, expand=True, pady=10, padx=10)

        self.label1 = Label(self.Frame1, text="Enter Message :", anchor=CENTER)
        self.label1.pack(side = LEFT,fill=None)
        self.entry1 = Text(self.Frame1, height=5,width=60)
        self.entry1.pack(side=RIGHT)

        self.keyLabel = Label(self.KeyFrame, text="KEY")
        self.keyLabel.pack(side=TOP)
        self.keyEntry = Entry(self.KeyFrame)
        self.keyEntry.pack(side=BOTTOM)

        self.label2 = Label(self.Frame2, text="Encrypted/Decrypted Text :", anchor=CENTER)
        self.label2.pack( side=LEFT)
        self.entry2 = Text(self.Frame2, height=5,width=60)
        self.entry2.pack(side=RIGHT)

        self.button1 = ttk.Button(self.Frame3, text="Encrypt")
        self.button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        self.button1.bind("<Button-1>", lambda event: self.TextButton(1))
        self.button2 = ttk.Button(self.Frame3, text="Decrypt")
        self.button2.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        self.button2.bind("<Button-1>", lambda event: self.TextButton(2))
        self.button3 = ttk.Button(self.Frame3, text="Exit")
        self.button3.bind("<Button-1>", lambda event: ExitScreen(root, hello))
        self.button3.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        self.status = Label(self.bg1label, text="Ready.", bd=1, relief=SUNKEN, anchor=CENTER, bg='light green', fg='black')
        self.status.pack(side=BOTTOM, fill=X)

    def TextButton(self,choice):
        global key, IV, EncryptedText
        self.entry2.delete(1.0, END)
        if (choice == 1):
            self.keyEntry.delete(0, 'end')
            message = self.entry1.get(1.0, END)
            key = Core.keyGenerator()
            IV, EncryptedText = Encrypt.Encrypt_all_blocks(message, key)
            msg = ''
            keyString = ''
            for x in key:
                keyString += chr(x)
            self.keyEntry.insert(0, keyString)
            IVString = ''
            for x in IV:
                IVString += chr(x)
            msg += IVString
            msg += EncryptedText
            self.label2.configure(text="Encrypted Text :")
            self.entry2.insert(1.0, msg)
            self.status.configure(text="Encryption complete.", bg='light green')
        else:
            msg = self.entry1.get("1.0", 'end-1c')
            keyString = self.keyEntry.get()
            keyList = []
            if len(keyString)!=BLOCK_SIZE:
                self.status.configure(text="Key Length Error.",bg='orange')
                return
            for x in range(0, BLOCK_SIZE):
                keyList.append(ord(keyString[x]))
            IVList = []
            for x in range(0, BLOCK_SIZE):
                IVList.append(ord(msg[x]))
            EncryptedTextActual = msg[BLOCK_SIZE:]
            DecryptedText = Core.remove_nulls(Decrypt.Decrypt_all_blocks(EncryptedTextActual, keyList, IVList))
            self.label2.configure(text="Decrypted Text :")
            self.entry2.insert(1.0, DecryptedText)
            self.status.configure(text="Decryption complete.", bg='light green')


class FileEnc:
    def __init__(self,root):
        root.title("File Encrypt/Decrypt")
        root.protocol('WM_DELETE_WINDOW', displayMessage)
        root.resizable(width=False, height=False)
        self.bg1_image = ImageTk.PhotoImage(Image.open("src/bg2.jpg"))
        self.w = self.bg1_image.width()
        self.h = self.bg1_image.height()
        root.geometry("%dx%d" % (self.w, self.h))
        self.bg1label = Label(root, image=self.bg1_image)
        self.bg1label.pack(side='top', fill='both', expand='yes')
        self.bg1label.image = self.bg1_image
        InitializeMenu(root)

        self.Frame1 = Frame(self.bg1label)
        self.Frame1.pack(fill=X, expand=True, pady=10, padx=10)

        self.KeyFrame = Frame(self.bg1label)
        self.KeyFrame.pack(fill=None, expand=True, pady=10, padx=10)

        self.Frame3 = Frame(self.bg1label)
        self.Frame3.pack(fill=X, expand=True, pady=10,padx=10)

        self.keyLabel = Label(self.KeyFrame, text="KEY")
        self.keyLabel.pack(side=TOP, fill=Y, expand=True)

        self.keyEntry = Entry(self.KeyFrame)
        self.keyEntry.pack(side=BOTTOM, fill=Y, expand=True, anchor = CENTER )

        self.BottomFrame = Frame(self.bg1label)
        self.BottomFrame.pack(fill=X, side=BOTTOM)

        self.label1 = Label(self.Frame1, text="Choose File : ")
        self.label1.pack(side=LEFT, fill=None)

        self.entry1 = Entry(self.Frame1)
        self.entry1.pack(side=LEFT, fill=BOTH, expand=True)
        self.bbutton = ttk.Button(self.Frame1, text="Browse")
        self.bbutton.pack(side=LEFT, fill=None,padx=5)
        self.bbutton.bind("<Button-1>", lambda event: self.getFileName(root))
        self.button1 = ttk.Button(self.Frame3, text="Encrypt")
        self.button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        self.button1.bind("<Button-1>", lambda event: self.ExecuteEncrypt())
        self.button2 = ttk.Button(self.Frame3, text="Decrypt")
        self.button2.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        self.button2.bind("<Button-1>", lambda event: self.ExecuteDecrypt())
        self.button3 = ttk.Button(self.Frame3, text="Exit")
        self.button3.bind("<Button-1>", lambda event: ExitScreen(root, hello))
        self.button3.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        self.status = Label(self.BottomFrame, text="Ready.", bd=1, relief=SUNKEN, anchor=CENTER, bg='light green')
        self.status.pack(side=BOTTOM, fill=X)

    def getFileName(self,root):
        root.iconify()
        fileName = askopenfilename(title='Choose file to Encrypt/Decrypt', initialdir='C:')
        self.entry1.insert(0, fileName)
        self.status.configure(text="Ready.", bg='light green')
        root.deiconify()

    def ExecuteEncrypt(self):
        self.status.configure(text="Encrypting.", bg='orange')
        self.TextButton2(1)

    def ExecuteDecrypt(self):
        # type: (object, object, object, object, object) -> object
        self.status.configure(text="Decrypting.", bg='orange')
        self.TextButton2(2)

    def TextButton2(self,choice):
        fileName = self.entry1.get()
        if (choice == 1):
            self.keyEntry.delete(0, 'end')
            try:
                keyText = Encrypt.Encrypt_File(fileName)
            except IOError:
                self.status.configure(text="File Not Found.", bg='red')
                return
            self.keyEntry.insert(0, keyText)
            self.status.configure(text="Encryption complete.", bg='light green')
        else:
            KeyText = self.keyEntry.get()
            try:
                Decrypt.Decrypt_File(fileName, KeyText)
            except IOError:
                self.status.configure(text="File Not Found.", bg='red')
                return
            self.status.configure(text="Decryption complete.", bg='light green')

class FolderEnc:
    def __init__(self,root):
        root.title("Folder Encrypt/Decrypt")
        root.geometry("+250+250")
        root.protocol('WM_DELETE_WINDOW', displayMessage)
        root.resizable(width=False, height=False)
        self.bg1_image = ImageTk.PhotoImage(Image.open("src/bg2.jpg"))
        self.w = self.bg1_image.width()
        self.h = self.bg1_image.height()
        root.geometry("%dx%d" % (self.w, self.h))
        self.bg1label = Label(root, image=self.bg1_image)
        self.bg1label.pack(side='top', fill='both', expand='yes')
        self.bg1label.image = self.bg1_image
        InitializeMenu(root)

        self.Frame1 = Frame(self.bg1label)
        self.Frame1.pack(fill=X, expand=True, pady=10, padx=10)

        self.KeyFrame = Frame(self.bg1label)
        self.KeyFrame.pack(fill=None, expand=True, pady=10, padx=10)

        self.Frame3 = Frame(self.bg1label)
        self.Frame3.pack(fill=X, expand=True, pady=10, padx=10, )

        self.keyLabel = Label(self.KeyFrame, text="KEY")
        self.keyLabel.pack(side=TOP, fill=Y, expand=True)

        self.keyEntry = Entry(self.KeyFrame)
        self.keyEntry.pack(side=BOTTOM, fill=Y, expand=True, anchor=CENTER)

        self.BottomFrame = Frame(self.bg1label)
        self.BottomFrame.pack(fill=X, side=BOTTOM)

        self.label1 = Label(self.Frame1, text="Choose Directory : ")
        self.label1.pack(side=LEFT, fill=None)

        self.entry1 = Entry(self.Frame1)
        self.entry1.pack(side=LEFT, fill=BOTH, expand=True)
        self.bbutton = ttk.Button(self.Frame1, text="Browse")
        self.bbutton.pack(side=LEFT, fill=None, padx=5)
        self.bbutton.bind("<Button-1>", lambda event: self.getDirectory(root))

        self.button1 = ttk.Button(self.Frame3, text="Encrypt")
        self.button1.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        self.button1.bind("<Button-1>", lambda event: self.TextButton3(event, 1))
        self.button2 = ttk.Button(self.Frame3, text="Decrypt")
        self.button2.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        self.button2.bind("<Button-1>", lambda event: self.TextButton3(event, 2))
        self.button3 = ttk.Button(self.Frame3, text="Exit")
        self.button3.bind("<Button-1>", lambda event: ExitScreen(root, hello))
        self.button3.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        self.status = Label(self.BottomFrame, text="Ready.", bd=1, relief=SUNKEN, anchor=CENTER, bg='light green')
        self.status.pack(side=BOTTOM, fill=X)

    def getDirectory(self,root):
        root.iconify()
        directory = askdirectory(title='Choose folder to Encrypt/Decrypt', initialdir='C:')
        self.entry1.insert(0, directory)
        self.status.configure(text="Ready.", bg='light green')
        root.deiconify()

    def TextButton3(self,event, option):
        if option == 1:
            path = self.entry1.get()
            self.keyEntry.delete(0, 'end')
            originalDirectory = os.getcwd()
            try:
                os.chdir(path)
            except WindowsError:
                self.status.configure(text="Path is invalid!", bg='red')
                return
            keyText = ''.join(Core.convert_to_chars(Core.keyGenerator()))
            DirectoryList = os.listdir(os.getcwd())
            for i, fileName in enumerate(DirectoryList):
                keyText = Encrypt.Encrypt_File(fileName, keyText)
                self.status.configure(text="Encrypted %d out of %d files" % (i, len(DirectoryList)), bg='orange')
            self.keyEntry.insert(0, keyText)
            self.status.configure(text="Folder Encryption complete.", bg='light green')
        else:
            originalDirectory = os.getcwd()
            path = self.entry1.get()
            try:
                os.chdir(path)
            except WindowsError:
                self.status.configure(text="Path is invalid!", bg='red')
                return
            DirectoryList = os.listdir(os.getcwd())
            for i, fileName in enumerate(DirectoryList):
                KeyText = self.keyEntry.get()
                self.status.configure(text="Decrypted %d out of %d files" % (i, len(DirectoryList)), bg='orange')
                Decrypt.Decrypt_File(fileName, KeyText)
            self.status.configure(text="Folder Decryption complete.", bg='light green')
        os.chdir(originalDirectory)

''' Main Window'''

hello= Tk()
RootWindow = MainWindow(hello)
hello.mainloop()