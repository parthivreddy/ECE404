# Hw03
# Parthiv Reddy
# reddy89
# 2/2/2023

#MI code taken from lecture slides by Avi Kak
import sys

#num,mod = int(sys.argv[1]), int(sys.argv[2])



# def modulo(x,y): #x % y
#     return (x - ((x//y) * y))

def multiplication(x, y):
    #x is number multiplying and y is the number being multiplied
    addTemp = 0
    while (x>>1) > 0:
        if(x & 1): #if x has an extra 1 at the end (can't account for that by bit shifting)
            addTemp += y
            x = x & ~1
        else:
            x >>= 1
            y <<= 1
    y += addTemp
    return y
        
def division(x, y): #integer division may have to write it recursively
    #x is the number being divided and y is number doing the division

    #divide number initially when x < y then subtract original x from current x*y then add this quotient to original quotient
    #ex 20 / 3 = 4 from bit shifting so now divide 8 / 3 = 2 from bit shifting now add 4+2 = 6
    if x < y:
        return 0
    if x == y:
        return 1

    quotient = 1
    origX = x
    while (x>>1) > y:
        quotient <<= 1
        x >>= 1
    #quotient might be equal to 1
    #print(quotient)
    return quotient + division(origX-(multiplication(quotient,y)), y)

NUM, MOD = int(sys.argv[1]), int(sys.argv[2])
def MI(num, mod):
    trueMod = mod
    NUM = num; MOD = abs(mod)
    mod = abs(mod)
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = division(num, mod)
        num, mod = mod, num % mod
        x, x_old = x_old - multiplication(q,x), x
        y, y_old = y_old - multiplication(q,y), y
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, trueMod, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, trueMod, MI))


# def findMI(num, mod):
#     NUM = num; MOD = abs(mod)
#     trueMod = mod
#     mod = abs(mod)
#     x, x_old = 0, 1
#     y, y_old = 1, 0
#     while mod:
#         q = num//mod
#         num, mod = mod, num % mod
#         x, x_old = x_old - q*x, x
#         y, y_old = y_old - q*y, y
#     if num != 1:
#         print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, trueMod, num))
#     else:
#         MI = (x_old + MOD) % MOD
#         print("\nMI of %d modulo %d is: %d\n" % (NUM, trueMod, MI))

MI(NUM, MOD)
# # findMI(NUM,MOD)

# assert MI(NUM, MOD) == findMI(NUM, MOD)

#print(NUM % abs(MOD))