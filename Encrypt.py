import pickle

import Core

ASCII_UPPER_RANGE=127
ASCII_LOWER_RANGE = 65
BLOCK_SIZE = 8



# Encrypt plain text block of size = BLOCK_SIZE
def encrypt_block(plaintextList, keyList):
    outputList = []
    for (i, j) in zip(plaintextList, keyList):
        r = i^j
        outputList.append(r)
    return outputList



def Encrypt_all_blocks(plaintext, key):
    plaintext_list = Core.convert_to_block(plaintext)
    Bit_List = Core.convert_to_ASCII(plaintext_list)
    IV = Core.keyGenerator()
    temp = IV[:]
    cipher = []
    for block in Bit_List:
        AfterXOR = Core.XOR_previous_block(block, temp)
        cipher_block = encrypt_block(AfterXOR, key)
        cipher.append(cipher_block)
        temp = cipher_block
    EncryptedText = Core.convert_all_blocks_to_chars(cipher)
    return IV, EncryptedText




#File Encryption and Decryption using Pickle
def Encrypt_File(filename,keyText=None):
    try:
        EncryptionFile = open(filename, 'rb')
    except IOError:
        raise IOError
    fileContent = EncryptionFile.read()
    EncryptionFile.close()
    key = []
    if keyText==None:
        key = Core.keyGenerator()
    else:
        key = Core.convert_block(list(keyText))

    IV, EncryptedText = Encrypt_all_blocks(fileContent,key)
    tempiv = ''.join(Core.convert_to_chars(IV))
    Final = tempiv+EncryptedText
    #for i,line in enumerate(fileContent):
        #IV.append(None)
       # EncryptedText.append(None)
        #IV[i], EncryptedText[i] = Encrypt_all_blocks(line[:-1], key)

        #Final.append([tempiv,EncryptedText[i]])
    keyFile = ''.join(Core.convert_to_chars(key))
    EncryptionFile = open(filename, 'w')
    #pickle.dump(keyFile, EncryptionFile)
    pickle.dump(Final,EncryptionFile)
    EncryptionFile.close()
    return keyFile


