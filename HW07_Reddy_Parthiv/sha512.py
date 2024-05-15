# Hw07
# Parthiv Reddy
# reddy89
# 3/09/2023

#Utilized code from lecture notes by Prof Kak
from BitVector import *
import sys



def thetaFunc(bv, typeCheck): #function for helping generate key schedule
        if typeCheck == 1:
                return ((bv.deep_copy()>>19) ^ (bv.deep_copy()>>61) ^ (bv.deep_copy().shift_right(6)))
        else:
                return ((bv.deep_copy()>>1) ^ (bv.deep_copy() >> 8) ^ (bv.deep_copy().shift_right(7)))

def genMsg(currblock_bv): #Takes in the input block bitvector and outputs message schedule as bitvectors
        #Generates first 16 messages
        msgList = [currblock_bv[i*64 : (i+1)*64] for i in range(16)]

        #Loop for the rest of the messages
        for i in range(16,80):
                part1 = (int(msgList[i-16]) + int(thetaFunc(msgList[i-15], 0)))
                part2 = (int(msgList[i-7]) + int(thetaFunc(msgList[i-2], 1)))

                msgList.append(BitVector(intVal = ((part1 + part2) & 0xFFFFFFFFFFFFFFFF), size = 64)) #mod 2^64
        return msgList
                
def tONE(e,f,g,h,W,K): #Implements the T1 function 
        Ch = (e & f) ^ ((~e) & g)
        sigmaE = (e.deep_copy()>>14) ^ (e.deep_copy()>>18) ^ (e.deep_copy()>>41) #Must do deep copy to avoid changes in original e
        holder = int(h) + int(Ch) + int(sigmaE) + int(W) + int(K)
        return BitVector(intVal = (holder & 0xFFFFFFFFFFFFFFFF), size = 64) #mod 2^64

def tTWO(a,b,c): #Implements the T2 function
        sigmaA = (a.deep_copy()>>28) ^ (a.deep_copy()>>34) ^ (a.deep_copy()>>39) #Must do deep copy to avoid changes in original a
        Maj = (a & b) ^ (a & c) ^ (b & c)
        return BitVector(intVal = ((int(sigmaA) + int(Maj)) & 0xFFFFFFFFFFFFFFFF), size = 64) #mod 2^64


def hashing(inputFile, outFile): #Implements hashing function

        #Initialization vector 
        z1 = BitVector(hexstring = "6a09e667f3bcc908")
        z2 = BitVector(hexstring = "bb67ae8584caa73b")
        z3 = BitVector(hexstring = "3c6ef372fe94f82b")
        z4 = BitVector(hexstring = "a54ff53a5f1d36f1")
        z5 = BitVector(hexstring = "510e527fade682d1")
        z6 = BitVector(hexstring = "9b05688c2b3e6c1f")
        z7 = BitVector(hexstring = "1f83d9abfb41bd6b")
        z8 = BitVector(hexstring = "5be0cd19137e2179")

        #integer values of round constants
        roundConstants = [0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc, 0x3956c25bf348b538, 
                0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242, 0x12835b0145706fbe, 
                0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 
                0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 
                0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab, 
                0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725, 
                0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 
                0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b, 
                0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218, 
                0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 
                0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 
                0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec, 
                0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c, 
                0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6, 
                0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 
                0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
                ]
        #print(len(roundConstants))
        roundConstants_bv = [BitVector(intVal = x) for x in roundConstants] #changes them to bitvector
        #print(roundConstants[0])
        # print(roundConstants[0])
        # print(int(roundConstants_bv[0]))

        FILEIN = open(inputFile)
        plaintext_bv = BitVector(textstring = FILEIN.read())
        FILEIN.close()
        length = len(plaintext_bv)
        #print(length)
        bvPlusOne = plaintext_bv + BitVector(bitstring = "1") #need one in case empty input file

        #Now need to pad with zeros to get integral multiple of 1024 combined with 128 bits needed for message length
        # howmanyzeros = ((1024-128) - len(bvPlusOne)) % 1024
        # zerolist = [0] * howmanyzeros
        # bv2 = bvPlusOne + BitVector(bitlist = zerolist)
        

        bvPlusOne.pad_from_right((1024-128) - (len(bvPlusOne) % 1024)) #padding with necessary amount of zeros to produce integer multiple of 1024
        msg_length_bv = BitVector(intVal = length, size = 128)
        plaintext_bv = bvPlusOne + msg_length_bv #appending message length with 128 bits
        #plaintext_bv = bv2 + msg_length_bv
        
        assert len(plaintext_bv) % 1024 == 0

        numBlocks = int(len(plaintext_bv) / 1024)

        assert numBlocks == len(plaintext_bv) / 1024

        for blocks in range(numBlocks):
                currblock_bv = plaintext_bv[blocks*1024 : (blocks+1)*1024]
                msgSchedule = genMsg(currblock_bv)
                
                a,b,c,d,e,f,g,h = z1,z2,z3,z4,z5,z6,z7,z8 #resetting a-h values for each block

                for i in range(80):
                        #print(a)
                        tone = tONE(e,f,g,h,msgSchedule[i], roundConstants_bv[i])
                        tTwo = tTWO(a,b,c)
                        changeE = int(d) + int(tone)
                        changeE_bv = BitVector(intVal = (changeE & 0xFFFFFFFFFFFFFFFF), size = 64)
                        changeA = int(tone) + int(tTwo)
                        changeA_bv = BitVector(intVal = (changeA & 0xFFFFFFFFFFFFFFFF), size = 64)

                        # h = g
                        # g = f
                        # f = e
                        # e = changeE_bv
                        # d = c
                        # c = b 
                        # b = a 
                        # a = changeA_bv

                        #for each round permuting the a-h values
                        a,b,c,d,e,f,g,h = changeA_bv, a, b, c, changeE_bv, e, f, g

                
                #at the end of each processed block add the initialization to the current values mod 2^64
                z1 = BitVector(intVal = ((int(a) + int(z1)) & 0xFFFFFFFFFFFFFFFF), size = 64)
                z2 = BitVector(intVal = ((int(b) + int(z2)) & 0xFFFFFFFFFFFFFFFF), size = 64)
                z3 = BitVector(intVal = ((int(c) + int(z3)) & 0xFFFFFFFFFFFFFFFF), size = 64)
                z4 = BitVector(intVal = ((int(d) + int(z4)) & 0xFFFFFFFFFFFFFFFF), size = 64)
                z5 = BitVector(intVal = ((int(e) + int(z5)) & 0xFFFFFFFFFFFFFFFF), size = 64)
                z6 = BitVector(intVal = ((int(f) + int(z6)) & 0xFFFFFFFFFFFFFFFF), size = 64)
                z7 = BitVector(intVal = ((int(g) + int(z7)) & 0xFFFFFFFFFFFFFFFF), size = 64)
                z8 = BitVector(intVal = ((int(h) + int(z8)) & 0xFFFFFFFFFFFFFFFF), size = 64)
        
        hash = z1 + z2 + z3 + z4 + z5 + z6 + z7 + z8 #add the current values of the 64 bit blocks to create hash
        FILEOUT = open(outFile, 'w')
        FILEOUT.write(hash.get_bitvector_in_hex())
        FILEOUT.close()
    

def main():
        hashing(sys.argv[1], sys.argv[2])

main()
