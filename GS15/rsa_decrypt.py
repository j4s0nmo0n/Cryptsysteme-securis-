#!/usr/bin/python
# -*-coding:Latin-1 -*

from __future__ import print_function

def main():

    keys = []  # list to store text from key_generator.txt
    with open("key_generator.txt", 'r') as file:
        for line in file:
            for a in line.split():  # split text by space
                #print(a)
                keys.append(a)  # add text to keys list
    keysLength = len(keys)
    d = keys[10]
    n = keys[2]
    e = keys[4]
    
    nums = []
    with open("encryptedText.txt", 'r') as file:
        for line in file:
            for string in line.split():
                nums.append(int(string, 16))
    l=len(nums)
    i = 0
    print ("\nDECHIFFREMENT : \n")
    decrypted_Mess = open("decryptText.txt", 'w')
    while i < l :
        x = decrypt(nums[i], int(d), int(n))
        y = chr(x)
        print(y, file=decrypted_Mess)
        print(x)
        print(y)
        i+=1
    with open("decryptText.txt", 'r') as decrypted_Mess:
        f = decrypted_Mess.read()
    decrypted_Mess = open("decryptText.txt", 'w')
    string = f.split("\n")
    print ("\n")
    print("".join(string))
    print("".join(string), file = decrypted_Mess)

def decrypt(c,d,n):
    x = pow(c,d,n)
    return x

if __name__ == "__main__":
   main()
