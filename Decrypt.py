import Core
import pickle

ASCII_UPPER_RANGE=127
ASCII_LOWER_RANGE = 65
BLOCK_SIZE = 8

# Decrypt Cipher block of size = BLOCK_SIZE
def decrypt_block(cipher_block, key_block):
    decrpyted = []
    for (c, k) in zip(cipher_block, key_block):
        decrpyted.append(c ^ k)
    return decrpyted

def Decrypt_all_blocks(ciphertext, key, IV):
    ciphertext_list = Core.convert_to_block(ciphertext)
    Bit_List = Core.convert_to_ASCII(ciphertext_list)
    plain = []
    temp = IV[:]
    for block in Bit_List:
        AfterDecrypt = decrypt_block(block, key)
        plain_block = Core.XOR_previous_block(AfterDecrypt, temp)
        plain.append(plain_block)
        temp = block
    DecryptedText = Core.convert_all_blocks_to_chars(plain)
    return DecryptedText
	
	
def Decrypt_File(filename,keyFile):
    try:
        DecryptionFile = open(filename, 'r')
    except IOError:
        raise IOError
    #keyFile = pickle.load(DecryptionFile)
    key = Core.convert_block(keyFile)
    msg = pickle.load(DecryptionFile)
    IVFile = msg[0:BLOCK_SIZE]
    line = msg[BLOCK_SIZE:]
    IV = Core.convert_block(list(IVFile))
    DecryptedText = Core.remove_nulls(Decrypt_all_blocks(line, key, IV))
    DecryptionFile = open(filename, 'wb')
    DecryptionFile.write((DecryptedText+"\n"))
    DecryptionFile.close()

	

