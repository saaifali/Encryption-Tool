import random

ASCII_UPPER_RANGE=127
ASCII_LOWER_RANGE = 65
BLOCK_SIZE = 8


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


def XOR_previous_block(plaintext_block, IV):
    outputList = []
    for (i, j) in zip(plaintext_block, IV):
        outputList.append(i ^ j)
    return outputList
	
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
