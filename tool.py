import random

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
def convert_block(block):
	result = []
	for character in block:
    	temp = ord(character)
        result.append(temp)
    return result

def convert_to_ASCII(plaintext_list):
    ASCII_list = []
    for i,block in enumerate(plaintext_list):
        ASCII_list.append(convert_block(block))
    return ASCII_list



#Converts a list of numbers to their corresponding characters. Has to be done individually for each block.
def convert_to_chars(message):
    finalMessage=[]
    for i in message:
        finalMessage.append(chr(i))
    return finalMessage

#Convert all blocks of characters to a string
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

#XOR previous block in CBC algorithm    
def XOR_previous_block(plaintext_block,IV):
    outputList=[]
    for (i,j) in zip(plaintext_block,IV):
        outputList.append(i^j)
    return outputList

#Complete CBC Encryption algorithm encryption
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
    IV_text = convert_to_chars(IV)
    return IV_text, EncrytedText

#Complete CBC Encryption algorithm decryption
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


#------ MAIN FUNCTION ---------->
print "<<------------------Encryption Decryption Tool------------------>>"
print "<<-----------------------------v1.0----------------------------->>"
ch=0
while True:
	print "1. Encrypt\n2. Decrypt\n3.Exit\n"
	ch = input("Enter choice : ")
	if ch == 1:
		message=raw_input("Enter message : ")
		key = keyGenerator()
		key_text = convert_to_chars(key)
		print "Key = ", key_text		
		IV_text, EncryptedText = Encrpyt_all_blocks(message,key)
		f = open("EncryptionDetails.txt",'a')
		f.write(key_text+"\n")
		f.write(IV_text+"\n")
		f.write(EncrytedText+"\n")
		print "\nEncrypted Text = ",EncryptedText
		f.close()
	elif ch==2:
		message=raw_input("Enter message : ")
		IV_text=raw_input("Enter IV : ")
		key_text=raw_input("Enter key : ")
		IV = list(IV_text)
		IV = 

print '-'*60
DecryptedText = remove_nulls(Decrypt_all_blocks(EncryptedText,key,IV))
print DecryptedText