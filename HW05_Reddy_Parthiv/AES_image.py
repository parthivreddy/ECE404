# Hw05
# Parthiv Reddy
# reddy89
# 2/21/2023

#Utilized code from lecture notes by Prof Kak

from BitVector import *
import sys
from AES_imageHelper import *

def ctr_aes_image(iv, image_file='image.ppm', out_file='enc_image.ppm', key_file='keyCTR.txt'):

    f = open(image_file, 'rb')
    headerlength = 0
    headerLines = f.readlines()[:3]
    for i in headerLines:
        headerlength += len(i)
    
    f.seek(0,0)
    f.seek(0,2)

    fileBits = f.tell() * 8
    headerBits = headerlength * 8

    ppm = BitVector(filename = image_file)
    ppm_bv = ppm.read_bits_from_file(fileBits)
    header_bv = ppm_bv[:headerBits]
    ppm_bv = ppm_bv[headerBits:]
    f.close()

    subTable, _ = genSubBytes() #obtaining substitution table for encryption
    FILEIN = open(key_file)
    key_bv = BitVector(textstring = FILEIN.read())
    FILEIN.close()
    keyWords = genKeys(key_bv, subTable) #generates key schedule
    #encrypted_bv = BitVector(size = 0)

    keyWords = vectorizeKey(keyWords) #transorms the 32 bit keys into cohesive 128 bit blocks
    #print(len(keyWords))

    encryption(ppm_bv, keyWords, out_file, iv, subTable, header_bv)


# iv = BitVector(textstring='computersecurity') #iv will be 128 bits
# ctr_aes_image(iv,'image.ppm','enc_image.ppm','keyCTR.txt')
