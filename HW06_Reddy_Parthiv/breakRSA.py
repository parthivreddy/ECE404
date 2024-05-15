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

def encryption(plainText, out1, out2, out3, nText):
    e = BitVector(intVal = 3)
    BLOCKSIZE = 128
    FILEIN = open(plainText)
    plaintext_bv = BitVector(textstring = FILEIN.read())
    FILEIN.close()

    if len(plaintext_bv) % BLOCKSIZE != 0:
        plaintext_bv.pad_from_right(BLOCKSIZE - len(plaintext_bv) % BLOCKSIZE)
    
    numblocks = int(len(plaintext_bv) / BLOCKSIZE)

    outfiles = [out1, out2, out3]
    pubKeys = []
    for j in range(3):
        encrypted_bv = BitVector(size = 0)
        p, q = checkValidPrimes(e)
        for i in range(numblocks):

            currblock_bv = plaintext_bv[i*BLOCKSIZE : (i+1) * BLOCKSIZE]
            currblock_bv.pad_from_left(BLOCKSIZE)
            intBlock = int(currblock_bv)

            temp_bv = BitVector(intVal = (pow(intBlock, int(e), p*q)), size = 256)

            encrypted_bv += temp_bv
        
        pubKeys.append(p*q)
        FILEOUT = open(outfiles[j], 'w')
        FILEOUT.write(encrypted_bv.get_bitvector_in_hex())
        FILEOUT.close()

    FILEOUT = open(nText, 'w')
    for i in range(3):
        FILEOUT.write(str(pubKeys[i]) + '\n')
    
    FILEOUT.close()

def cracking(enc1, enc2, enc3, pubKeyFile, outFile):
    FILEIN = open(pubKeyFile)
    pubkeys = FILEIN.readlines()
    FILEIN.close()
    #print(int(pubkeys[0]))
    N = 1
    files = [enc1, enc2, enc3]
    files_bv = []
    for i in range(3):
        N *= int(pubkeys[i])
        FILEIN = open(files[i])
        files_bv.append(BitVector(hexstring = FILEIN.read()))
        FILEIN.close()

    # assert N == int(pubkeys[0]) * int(pubkeys[1]) * int(pubkeys[2])

    assert N // int(pubkeys[0]) == int(pubkeys[1]) * int(pubkeys[2])
    assert N // int(pubkeys[1]) == int(pubkeys[0]) * int(pubkeys[2])
    assert N // int(pubkeys[2]) == int(pubkeys[1]) * int(pubkeys[0])

    # print(int((N / int(pubkeys[0]))))
    # print((N // int(pubkeys[0])))
    # assert int((N / int(pubkeys[0]))) == (N // int(pubkeys[0]))

    Cis = []

    for i in range(3):
        Mi = (N // int(pubkeys[i]))
        #print(Mi)
        Mi_bv = BitVector(intVal = Mi)
        Cis.append(Mi * int(Mi_bv.multiplicative_inverse(BitVector(intVal =int(pubkeys[i])))))
    #now reconstructin message modulo N
    numblocks = int(len(files_bv[2]) / 256)
    cracked_bv = BitVector(size = 0)
    for i in range(numblocks): #need to apply CRT for each block
        A=0
        for j in range(3):
            currblock_bv = files_bv[j][i*256 : (i+1) * 256]
            #assert int(currblock_bv) == (int(currblock_bv) % int(pubkeys[j]))
            A += (int(currblock_bv) * Cis[j])
        
        A = A % N
        A = solve_pRoot.solve_pRoot(3, A)
        

        A = A & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

        unpad_bv = BitVector(intVal = A, size = 128)
    
        cracked_bv += unpad_bv
    
    FILEOUT = open(outFile, 'w')
    FILEOUT.write(cracked_bv.get_text_from_bitvector())
    FILEOUT.close()


        



def main():
    if sys.argv[1] == '-e':
        encryption(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5], sys.argv[6])
        #print('encryption')
    elif sys.argv[1] == '-c':
        cracking(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        #print('cracking')

main()


