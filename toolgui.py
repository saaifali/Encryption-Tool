import random
import sys
from Tkinter import*

ASCII_UPPER_RANGE=256
BLOCK_SIZE = 8

#Encrypt plain text block of size = BLOCK_SIZE
def encrypt_block(plaintextList,keyList):
    outputList=[]
    for (i,j) in zip(plaintextList,keyList):
        outputList.append(i^j)
    return outputList

#Generates a random key sequence
def keyGenerator():
    key=[]
    for i in range(0,BLOCK_SIZE):
        key.append(random.randrange(0,ASCII_UPPER_RANGE))
    return key

#Sets length of plaintext to be divisible by BLOCK_SIZE
def set_length(plaintext):
        while (len(plaintext)%BLOCK_SIZE)!=0:
            plaintext = chr(0)+plaintext
        return plaintext


#Convert a string (plaintext) to a list each containing a list of 8 characters each. --> [[1,2,3,4,5,6,7,8],[...],[...],.....]
def convert_to_block(plaintext):
        plaintext=set_length(plaintext)
        plaintext_list=[]
        for i in range (0,len(plaintext),8):
                block=[]
                for j in range(0,8):
                        block.append(plaintext[i+j])
                plaintext_list.append(block)
        #print plaintext_list
        return plaintext_list

    
#Decrypt Cipher block of size = BLOCK_SIZE
def decrypt_block(cipher_block, key_block):
        decrpyted = []
        for (c,k) in zip(cipher_block,key_block):
                decrpyted.append(c^k)
        return decrpyted


#Convert the list of blocks of 8 characters to their equivalent integer form
def convert_to_ASCII(plaintext_list):
        ASCII_list = []
        for i,block in enumerate(plaintext_list):
                ASCII_list.append([])
                for character in block:
                        temp = ord(character)
                        ASCII_list[i].append(temp)
        return ASCII_list

#Converts a list of numbers to their corresponding characters. Has to be done individually for each block.
def convert_to_chars(message):
    finalMessage=[]
    for i in message:
        finalMessage.append(chr(i))
    return finalMessage

def convert_all_blocks_to_chars(messageList):
    result = []
    for message in messageList:
        result.extend(convert_to_chars(message))
    resultString = ''.join(result)
    return resultString


#Removes all Null values added to pad a string to required block size
def remove_nulls(decrypted):
    count = 0
    for c in decrypted:
        if c==chr(0):
            count+=1
        else:
            break
    if not count<0:
        return decrypted[count:]
    else:
        return decrypted     
    
def XOR_previous_block(plaintext_block,IV):
    outputList=[]
    for (i,j) in zip(plaintext_block,IV):
        outputList.append(i^j)
    return outputList


def Encrpyt_all_blocks(plaintext,key):
    plaintext_list = convert_to_block(plaintext)
    Bit_List = convert_to_ASCII(plaintext_list)
    IV = keyGenerator()
    temp = IV[:]
    cipher = []
    for block in Bit_List:
        AfterXOR = XOR_previous_block(block,temp)
        cipher_block = encrypt_block(AfterXOR,key)
        cipher.append(cipher_block)
        temp = cipher_block
    EncrytedText = convert_all_blocks_to_chars(cipher)
    return IV, EncrytedText

def Decrypt_all_blocks(ciphertext,key,IV):
    ciphertext_list = convert_to_block(ciphertext)
    Bit_List = convert_to_ASCII(ciphertext_list)
    plain = []
    temp = IV[:]
    for block in Bit_List:
        AfterDecrypt = decrypt_block(block,key)
        plain_block = XOR_previous_block(AfterDecrypt,temp)
        plain.append(plain_block)
        temp = block
    DecryptedText = convert_all_blocks_to_chars(plain)
    return DecryptedText

'''
message=raw_input("Enter message : ")
key = keyGenerator()
#print "Key = ", key
IV, EncryptedText = Encrpyt_all_blocks(message,key)
print "Encrypted Text = ",EncryptedText
print '='*120
DecryptedText = remove_nulls(Decrypt_all_blocks(EncryptedText,key,IV))
print "Decrypted Text = ",DecryptedText'''

def TextButton(event,choice):
    global key,IV,EncryptedText
    if(choice==1):
        message=entry1.get()
        key=keyGenerator()
        #msg=''
        #msg=msg+"Key="+key+"\n"
        IV, EncryptedText = Encrpyt_all_blocks(message,key)
        #msg=msg+"Encrypted Text = "+EncryptedText+"\n"
        msg=EncryptedText
        entry2.insert(0,msg)
        print msg
    else:
    #def DecryptTextButton(event):
        entry2.delete(0,'end')
        #text1.delete('1.0',END)
        DecryptedText = remove_nulls(Decrypt_all_blocks(EncryptedText,key,IV))
        #msg=''
        #msg=msg+"Decrypted Text = "+DecryptedText  
        msg=DecryptedText
        entry2.insert(0,msg)
        print msg  

root=Tk()
root.columnconfigure(0, weight=1)


label1=Label(root,text="Enter the text")
label1.grid(row=0,column=0,sticky=W)

entry1=Entry(root,text="Enter the text here")
entry1.grid(row=0,column=1,sticky=W)


label2=Label(root,text="Encrypted Text")
label2.grid(row=1,column=0,sticky=W)

entry2=Entry(root)
entry2.grid(row=1,column=1,sticky=W)


button1=Button(root,text="Encrypt")
button1.grid(row=2,column=0)
button1.bind("<Button-1>",lambda event: TextButton(event,1))
button2=Button(root,text="Decrypt")
button2.grid(row=2,column=1)
button2.bind("<Button-1>",lambda event: TextButton(event,2))
button3=Button(root,text="Exit")
button3.grid(row=2,column=2)
button3.bind("<Button-1>",sys.exit)

'''
button1=Button(root,text="Encrypt",command="EncryptTextButton")
button1.pack(row=2,column=2)
button2=Button(root,text="Encrypt",command="EncryptTextButton")
button2.pack(row=2,column=2)
button3=Button(root,text="Encrypt",command="EncryptTextButton")
button3.pack(row=2,column=2)
'''

root.mainloop()
