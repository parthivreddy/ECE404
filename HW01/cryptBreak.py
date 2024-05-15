# Hw01
# Parthiv Reddy
# reddy89
# 1/19/2023
from BitVector import *

#Utilized decrpytion code from lecture notes 2

def cryptBreak(ciphertextFile, key_bv):
    BLOCKSIZE = 16
    byteNum = BLOCKSIZE // 8 
    PassPhrase = "Hopes and dreams of a million years"
    pass_iv = BitVector(bitlist = [0] * BLOCKSIZE)
    for i in range(0, len(PassPhrase) // byteNum):
        charBlock = PassPhrase[i*byteNum : (i+1) * byteNum]
        pass_iv ^= BitVector(textstring = charBlock)
    
    FILEIN = open(ciphertextFile)
    cipherText_bv = BitVector(hexstring = FILEIN.read())
    FILEIN.close()

    decrypted_bv = BitVector(size = 0)

    prev_block = pass_iv

    for i in range(0, len(cipherText_bv) // BLOCKSIZE):
        curr_block_bv = cipherText_bv[i*BLOCKSIZE: (i+1)*BLOCKSIZE]
        prev_temp = curr_block_bv.deep_copy()
        curr_block_bv ^= prev_block
        prev_block = prev_temp
        curr_block_bv ^= key_bv
        decrypted_bv += curr_block_bv

    plainText = decrypted_bv.get_text_from_bitvector()
    return plainText
    # FILEOUT = open(plaintextFile, 'w')
    # FILEOUT.write(plainText)
    # FILEOUT.close()

if __name__ == "__main__":
    # for i in range(0, 2**16):
    #     key_bv = BitVector(intVal = i, size = 16)
    #     decryptedMessage = cryptBreak("ciphertextFile.txt", key_bv)
    #     if 'Sir Lewis' in decryptedMessage:
    #         print('Encryption Broken!')
    #         print(f"key: {i}")
    #         break
    #     else:
    #         print(f'{i}: Not decrypted yet')
    key_bv = BitVector(intVal = 4040, size = 16)
    decryptedMessage = cryptBreak("ciphertextFile.txt", key_bv)
    print(decryptedMessage)

    


