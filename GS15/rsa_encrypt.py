#!/usr/bin/python
# -*-coding:Latin-1 -*
from __future__ import print_function

def main(key):
    keys = []                                       #On cree une liste afin de stocker les clés 
    with open("key_generator.txt", 'r') as file:    #On ouvre le fichier qui contient les clés
        for line in file:
            for a in line.split():                  #On divise le texte contenu dans le fichier par espaces
                #print(a)
                keys.append(a)                      #On complète note liste
    n = int(keys[2])                                #On récupère n dans notre liste
    e = int(keys[4])                                #On récupère e dans notre liste
    encrypted_mess = open("encryptedText.txt", 'w') #On crée le fichier qui contiendra le message signé 
    plainText = str(key)

    #plainText = raw_input("\nVeuillez entrer le message que vous souhaitez signer : ") #On demande à l'utilisateur d'entrer le message qu'il souhaite signer
    txt_to_sign = open("txt_to_sign.txt", 'w') 
    txt_to_sign.write(plainText) #On écrie le texte à signer dans un fichier
    txt_to_sign.close()
    with open("txt_to_sign.txt") as newFile:
        for word in newFile:
            for char in word:
                print(encryption(ord(char),e,n),file=encrypted_mess) #On chiffre le texte contenu dans notre fichier                             
    #On affiche la signature en hexadecimal et en une seule ligne
    with open("encryptedText.txt", 'r') as encrypted_mess:
        file=encrypted_mess.read()
        print("\nCHIFFREMENT : \n")
        print(file)

def encryption(m,e,n): #Fonction de signature RSA
    x = hex(pow(m,e,n))[2:] #x=m^e mod n
    return x

if __name__ == "__main__":
   main(key)

