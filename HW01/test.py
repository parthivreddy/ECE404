import cryptBreak
from BitVector import *
someRandomInteger = 4040 #Arbitrary integer for creating a BitVector
key_bv = BitVector(intVal=someRandomInteger, size=16)
decryptedMessage = cryptBreak.cryptBreak('ciphertextFile.txt', key_bv)
if 'Sir Lewis' in decryptedMessage:
    print('Encryption Broken!')
else:
    print('Not decrypted yet!')
