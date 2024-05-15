# Hw04
# Parthiv Reddy
# reddy89
# 2/14/2023

#Utilized code from lecture notes by Prof Kak
from BitVector import *
import sys

def makeStateArray(blocktext): #taking 128 bit block and putting them in 4 x 4 array in column order
    array = [[blocktext[(8 * row) + (col*32) : (row +1) * 8 + (col * 32)] for col in range(4)] for row in range(4)]
    return array #populated state array in columnwise fashion using a 128 bit block


def genSubBytes():
    AES_modulus = BitVector(bitstring='100011011') #irreducible polynomial in GF(2^8)
    subBytesTable = [] # SBox for encryption
    invSubBytesTable = [] # SBox for decryption
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))
    
    return subBytesTable, invSubBytesTable
    

def subStateArray(array, table): #replacing array values with S box values
    tempArray = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            tempArray[i][j] = BitVector(intVal = table[int(array[i][j])], size = 8)
    return tempArray


def shiftRows(subTable): #shifting rows for encryption
    # shiftedTable = [[0 for x in range(4)] for y in range(4)]
    # shiftedTable[0] = subTable[0]
    for i in range(1,4):
        subTable[i] = subTable[i][i:] + subTable[i][:i]
    # subTable = subTable[1][1:] + subTable[1][0]
    # subTable = subTable[2][2:] + subTable[2][:2]
    # subTable = subTable[3][3:] + subTable[3][:3]
    return subTable

def invShiftRows(subTable): #shifting rows for decryption
    for i in range(1,4):
        subTable[i] = subTable[i][3-i+1:] + subTable[i][:(3-i+1)]
    return subTable




def mixCols(subTable): #doing multiplication of columns in GF(2^8) for encryption
    AES_modulus = BitVector(bitstring='100011011')
    newTable = [[0 for x in range(4)] for y in range(4)]
    two = BitVector(intVal = 2)
    three = BitVector(intVal = 3)
    for i in range(4):
        for j in range(4):
            newTable[i][j] = subTable[i][j].gf_multiply_modular(two, AES_modulus, 8) ^ \
                             subTable[(i+1) % 4][j].gf_multiply_modular(three, AES_modulus, 8) ^ \
                             subTable[(i+2) % 4][j] ^ subTable[(i+3) % 4][j]
    return newTable

def invMixCols(subTable): #doing multiplication of columns in GF(2^8) for decryption
    AES_modulus = BitVector(bitstring='100011011')
    newTable = [[0 for x in range(4)] for y in range(4)]
    #constants to do multiplication
    E = BitVector(intVal = 0x0E)
    B = BitVector(intVal = 0x0B)
    D = BitVector(intVal = 0x0D)
    nine = BitVector(intVal = 0x09)
    for i in range(4):
        for j in range(4):
            newTable[i][j] = subTable[i][j].gf_multiply_modular(E, AES_modulus, 8) ^ \
                             subTable[(i+1)%4][j].gf_multiply_modular(B, AES_modulus, 8) ^ \
                             subTable[(i+2)%4][j].gf_multiply_modular(D, AES_modulus, 8) ^ \
                             subTable[(i+3)%4][j].gf_multiply_modular(nine, AES_modulus, 8)
    return newTable



def g(word, prevConstant, subTable): #function to be used when generating key schedule
    AES_modulus = BitVector(bitstring='100011011')
    shifted_word = word.deep_copy()
    shifted_word << 8
    subbedWord = BitVector(size = 0)
    for i in range(4):
        subbedWord += BitVector(intVal = subTable[shifted_word[i*8 : (i+1)*8].intValue()], size = 8)
    subbedWord[:8] ^= prevConstant
    prevConstant = prevConstant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return subbedWord, prevConstant


def genKeys(key, subTable): #given a 256 bit key
    keyWords = [None for i in range(60)] #60 words for 256 input
    roundConstant = BitVector(intVal = 1, size = 8) #starts off at 1 for first round
    for i in range(8):
        keyWords[i] = key[i*32: (i+1)*32] #first 8 words of key
    
    for i in range(8,60): #generating rest of key schedule depends on xoring of previous keys and function g
        if i%8 == 0:
            kwd, roundConstant = g(keyWords[i-1], roundConstant, subTable)
            keyWords[i] = keyWords[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            keyWords[i] = keyWords[i-8] ^ keyWords[i-1]
        elif (i - (i//8)*8) == 4:
            keyWords[i] = BitVector(size = 0)
            for j in range(4):
                keyWords[i] += BitVector(intVal =
                                        subTable[keyWords[i-1][8*j:8*j+8].intValue()], size = 8)
            keyWords[i] ^= keyWords[i-8]
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            keyWords[i] = keyWords[i-8] ^ keyWords[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return keyWords
    
def unravelTable(array): #assuming elements of array are in bitvector form. Turns array into concatenated bitvector
    vector = BitVector(size = 0)
    for i in range(4):
        for j in range(4):
            vector += array[j][i]
    return vector

def vectorizeKey(keyWords): #divide key schedule into 128 bit blocks for easy XORing
    key = []
    for i in range(15):
        keyBlock = keyWords[i*4] + keyWords[i*4+1] + keyWords[i*4 + 2] + keyWords[i*4 + 3]
        key.append(keyBlock)
    return key


def encryption(plainTextFile, keyFile, outFile): #implements AES encryption
    AES_modulus = BitVector(bitstring='100011011')
    BLOCKSIZE = 128 #128 bit block

    FILEIN = open(plainTextFile)
    plaintext_bv = BitVector(textstring = FILEIN.read())
    FILEIN.close()

    if len(plaintext_bv) % 128 != 0: #padding bitvector if not divisible by blocksize amount
        plaintext_bv.pad_from_right(128 - (len(plaintext_bv) % 128))
    
    assert len(plaintext_bv) / 128 == len(plaintext_bv) // 128
    numBlocks = int(len(plaintext_bv) / 128)

    subTable, _ = genSubBytes() #obtaining substitution table for encryption
    FILEIN = open(keyFile)
    key_bv = BitVector(textstring = FILEIN.read())
    FILEIN.close()
    keyWords = genKeys(key_bv, subTable) #generates key schedule
    encrypted_bv = BitVector(size = 0)

    keyWords = vectorizeKey(keyWords) #transorms the 32 bit keys into cohesive 128 bit blocks
    #print(len(keyWords))

    for i in range(numBlocks): #do for each 128 bit block
        currBlock = plaintext_bv[i*BLOCKSIZE : (i+1) * BLOCKSIZE]
        #print(type(currBlock))
        currBlock = currBlock ^ keyWords[0] #XOR with first 4 words before processing
        # num = int(currBlock)
        # print(hex(num))
        # print('\n')
        array = makeStateArray(currBlock) #making state array for each block

        for j in range(14): #14 rounds of processing for 256 bit key
            subbedArray = subStateArray(array, subTable) #sub the array

            # print(type(subbedArray[0][0]))
            # print(hex(int(unravelTable(subbedArray))))
            # print('\n')

            shiftedTable = shiftRows(subbedArray) #shifting rows

            # print(hex(int(unravelTable(shiftedTable))))
            # print('\n')

            if j != 13: #if not last round of encyrption mix columns
                stepThreeTable = mixCols(shiftedTable)
            else:
                stepThreeTable = shiftedTable
            
            #print(type(stepThreeTable[0][0]))
            stepThree_bv = unravelTable(stepThreeTable) #transforming array into 128 bit vector

            #print(hex(int(stepThree_bv)))
            

            stepFour_bv = stepThree_bv ^ keyWords[j+1] #XOR with current key round

            #print(hex(int(stepFour_bv)))
            
            array = makeStateArray(stepFour_bv) #remake the array for the next round
        
        encrypted_bv += stepFour_bv #adds processed vector to accumulating bitvector
            
    FILEOUT = open(outFile, 'w')
    FILEOUT.write(encrypted_bv.get_bitvector_in_hex())
    FILEOUT.close()




def decryption(cipherText, keyFile, plainText): #implements decryption
    AES_modulus = BitVector(bitstring='100011011')
    BLOCKSIZE = 128 #128 bit block

    FILEIN = open(cipherText)
    cipherText_bv = BitVector(hexstring = FILEIN.read())
    FILEIN.close()

    keysubTable, subTable = genSubBytes() #obtains s tables for encryption (needed for key schedule) and for decryption
    numBlocks = int(len(cipherText_bv) / 128) 

    FILEIN = open(keyFile)
    key_bv = BitVector(textstring = FILEIN.read())
    FILEIN.close()
    keyWords = genKeys(key_bv, keysubTable) 
    keyWords = vectorizeKey(keyWords) #obtains 128 bit blocks of key schedule
    #print(keyWords[0])
    keyWords = [x for x in keyWords[::-1]] #reverses key schedule for decryption
    
    #print(keyWords[-1])

    plaintext_bv = BitVector(size = 0)

    for i in range(numBlocks):
        currBlock = cipherText_bv[i*BLOCKSIZE : (i+1)*BLOCKSIZE]
        currBlock ^= keyWords[0] #XOR with first four keys before processing

        array = makeStateArray(currBlock) #creates state array

        for j in range(14):
            shiftedTable = invShiftRows(array) #first step is inverse shift rows

            subbedArray = subStateArray(shiftedTable, subTable) #next is using sub table

            stepThree_bv = unravelTable(subbedArray) #must turn array into 128 bit vector for key xoring
            stepThree_bv ^= keyWords[j+1] #XOR with current key round

            if j != 13: #if not last round of decryption do mix columns
                stepFourArr = makeStateArray(stepThree_bv) #must remake array before mixing cols
                array = invMixCols(stepFourArr)
        
        plaintext_bv += stepThree_bv #concatenates processed block of cipherText to plaintext output
    
    FILEOUT = open(plainText, 'w')
    FILEOUT.write(plaintext_bv.get_text_from_bitvector())
    FILEOUT.close()




def main():

    if sys.argv[1] == '-e':
        encryption(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == '-d':
        decryption(sys.argv[2], sys.argv[3], sys.argv[4])

main()