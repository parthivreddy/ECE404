# Hw05
# Parthiv Reddy
# reddy89
# 2/21/2023

#Utilized code from lecture notes by Prof Kak
from BitVector import *
import sys
from AES import *

def x931Helper(v0, dt, keyWords, randomNumList, subTable):

    firstEDE = encryption(dt, keyWords, subTable)

    afterXOR = firstEDE ^ v0

    secondEDE = encryption(afterXOR, keyWords, subTable)

    randomNumList.append(secondEDE)

    aftersecondXOR = firstEDE ^ secondEDE

    vNext = encryption(aftersecondXOR, keyWords, subTable)

    return randomNumList, vNext


    #print("helper")


def x931(v0, dt, totalNum, key_file):
    # Arguments:
    # v0: 128-bit BitVector object containing the seed value
    # dt: 128-bit BitVector object symbolizing the date and time
    # totalNum: The total number of random numbers to generate
    # key_file: Filename for text file containing the ASCII encryption key for AES

    subTable, _ = genSubBytes() #obtaining substitution table for encryption
    FILEIN = open(key_file)
    key_bv = BitVector(textstring = FILEIN.read())
    FILEIN.close()
    keyWords = genKeys(key_bv, subTable) #generates key schedule
    keyWords = vectorizeKey(keyWords)

    randomNumList = []

    for i in range(totalNum):

        randomNumList, v0 = x931Helper(v0, dt, keyWords, randomNumList, subTable)


    return randomNumList


# v0 = BitVector(textstring='computersecurity') #v0 will be 128 bits
# #As mentioned before, for testing purposes dt is set to a predetermined value
# dt = BitVector(intVal=501, size=128)
# listX931 = x931(v0,dt,3,'keyX931.txt')
# #Check if list is correct
# print('{}\n{}\n{}'.format(int(listX931[0]),int(listX931[1]),int(listX931[2])))



    



