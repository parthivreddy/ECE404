# Hw06
# Parthiv Reddy
# reddy89
# 2/28/2023

#Utilized code from lecture notes by Prof Kak

import sys
from BitVector import *
import PrimeGenerator
import solve_pRoot

def gcd(a,b):
    while b:
        a, b = b, a % b
    return a

def checkValidPrimes(e):
    p = PrimeGenerator.PrimeGenerator(bits = 128).findPrime()
    #p = PrimeGenerator.findPrime()
    q = PrimeGenerator.PrimeGenerator(bits = 128).findPrime()
   
    valid = 0
    while not(valid):
        if not(((p>>126) & 3) == 3 and ((q>>126) & 3) == 3):
            p = PrimeGenerator.PrimeGenerator(bits = 128).findPrime()
            q = PrimeGenerator.PrimeGenerator(bits = 128).findPrime()
            continue
        if p == q:
            p = PrimeGenerator.PrimeGenerator(bits = 128).findPrime()
            q = PrimeGenerator.PrimeGenerator(bits = 128).findPrime()
            continue
        # p_bv = BitVector(intVal = p-1)
        # q_bv = BitVector(intVal = q-1)
        # gcd_p = e.gcd(p_bv)
        # gcd_q = e.gcd(q_bv)
        if (gcd(p-1,int(e)) != 1 or gcd(q-1, int(e)) != 1):
            p = PrimeGenerator.PrimeGenerator(bits = 128).findPrime()
            q = PrimeGenerator.PrimeGenerator(bits = 128).findPrime()
            continue
        valid = 1
    
    return p, q
        
        


def keyGeneration(pText, qText):
    e = BitVector(bitstring = '10000000000000001')
    p, q = checkValidPrimes(e)

    with open(pText,'w') as f:
        f.write(str(p))

    with open(qText, 'w') as f:
        f.write(str(q))


def encryption(plainText, pText, qText, outFile):
    e = BitVector(bitstring = '10000000000000001')
    BLOCKSIZE = 128
    FILEIN = open(plainText)
    plaintext_bv = BitVector(textstring = FILEIN.read())
    FILEIN.close()

    FILEp = open(pText)
    p = int(FILEp.read())
    FILEp.close()

    FILEq = open(qText)
    q = int(FILEq.read())
    FILEq.close()

    encrypted_bv = BitVector(size = 0)

    if len(plaintext_bv) % BLOCKSIZE != 0:
        plaintext_bv.pad_from_right(BLOCKSIZE - len(plaintext_bv) % BLOCKSIZE)
    
    numblocks = int(len(plaintext_bv) / BLOCKSIZE)
    
    for i in range(numblocks):
        currblock_bv = plaintext_bv[i*BLOCKSIZE : (i+1) * BLOCKSIZE]
        currblock_bv.pad_from_left(BLOCKSIZE)
        intBlock = int(currblock_bv)

        temp_bv = BitVector(intVal = (pow(intBlock, int(e), p*q)), size = 256)

        encrypted_bv += temp_bv
    
    FILEOUT = open(outFile, 'w')
    FILEOUT.write(encrypted_bv.get_bitvector_in_hex())
    FILEOUT.close()

def CRT(C, p, q, d):
    Vp = pow(C, int(d), p)
    Vq = pow(C, int(d), q)

    Xp = q * int(BitVector(intVal = q).multiplicative_inverse(BitVector(intVal = p)))
    Xq = p * int(BitVector(intVal = p).multiplicative_inverse(BitVector(intVal = q)))

    return (Vp * Xp + Vq * Xq) % (p*q)



def decryption(cipherText, pText, qText, outFile):
    e = BitVector(bitstring = '10000000000000001')
    BLOCKSIZE = 128
    FILEIN = open(cipherText)
    ciphertext_bv = BitVector(hexstring = FILEIN.read())
    FILEIN.close()

    FILEp = open(pText)
    p = int(FILEp.read())
    FILEp.close()

    FILEq = open(qText)
    q = int(FILEq.read())
    FILEq.close()

    plainText_bv = BitVector(size = 0)
    d = e.multiplicative_inverse(BitVector(intVal = (p-1)*(q-1)))

    numblocks = int(len(ciphertext_bv) / 256)
    
    for i in range(numblocks):
        currblock_bv = ciphertext_bv[i*256 : (i+1) * 256]
        intBlock = int(currblock_bv)

        temp_bv = BitVector(intVal = CRT(intBlock, p, q, d))
        #temp_bv = BitVector(intVal = (pow(intBlock, int(d), p*q)))
        #print(len(temp_bv))
        #print(int(temp_bv))
        temp_bv = int(temp_bv) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        
        #print(temp_bv)
        #print(len(temp_bv))
        unpad_bv = BitVector(intVal = temp_bv, size = 128)
        # print("hello")
        # print(temp_bv.get_text_from_bitvector())

        plainText_bv += unpad_bv

    FILEOUT = open(outFile, 'w')
    FILEOUT.write(plainText_bv.get_text_from_bitvector())
    FILEOUT.close()

        


def main():
    if sys.argv[1] == "-g":
        keyGeneration(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "-e":
        encryption(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        #print("encryption")
    elif sys.argv[1] == "-d":
        decryption(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        #print("decryption")

main()
