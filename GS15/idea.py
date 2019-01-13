#!/usr/bin/python
# -*-coding:Latin-1 -*
import fileinput
import numpy as np
import random
import os
import binascii
from bitstring import BitArray

def menu_cle():
  taille = input("Veuillez entrer la taille de votre clé:  ")
  return int(taille)

def generer_la_cle():
    # On demande à l'utilisateur d'écrire sa clé composée de 16 caractères ascii
    #random_key = str(raw_input(" veuillez entrer une clé de 16 caractères : "))

    #clé arbitraire à changer: 
    random_key = "otdepasse0000000"
    result = []
    key_hex = binascii.hexlify(random_key)
    #print "key = ", key_hex
    return key_hex

def generer_la_cle2():
    # On demande à l'utilisateur d'écrire sa clé composée de 16 caractères ascii
    #random_key = str(raw_input(" veuillez entrer une clé de 16 caractères : "))
    random_key = ""
    taille = menu_cle()
    if taille == 128:
      random_key = "otdepasse0000000"
    elif taille == 96:
      random_key = "otdepasse000"
    elif taille == 160:
      random_key = "motdepasse00000000000"
    elif taille == 256:
      random_key = "otdepasse0000000otdepasse0000000"
    else:
       random_key = "0000000000000000"
    result = []
    key_hex = binascii.hexlify(random_key)
    #print "key = ", key_hex
    #print key_hex
    return key_hex

################ Fonction qui transforme le fichier entré en hexa #######""
def file_to_hex(file):
    handler = open(file, "rb+")
    hex_fichier= binascii.hexlify(handler.read())

    return hex_fichier 

############### Fonction qui transforme hexa en block de 4 hexa = 16 bits #######""
def hex_to_block(text):
    if(len(text)%16!=0):
        for i in range(16-(len(text)%16)):
            text=text+'0'
    blocks = map(''.join,zip(*[iter(text)]*4))     
    return blocks

        #arrayContentTxt = list(mytextstring)

    #binarray = ' '.join(format(ch, 'b') for ch in bytearray(mytextstring))
    
############### Fonction qui transforme les blocks de hexa en texte  #######
def block_to_strings(block):
    #print "hello "
    #print block
    strings = binascii.unhexlify("".join(block))
    
    return strings


############### Fonction qui met le texte dans un fichier  #######
def strings_to_file(strings,filename):
  f = open(filename,'ab+')
  for mot in strings:
    f.write(mot)
  f2 = open(filename, "r")
  return f2


############### Fonction qui transforme les hexa en binaire  #######
def hex_to_bin(text):
  #print (bin(int(text, 16))[2:].zfill(16))
  return str(bin(int(text, 16))[2:].zfill(16)) 

def bin_to_hex(text):
  #text = str(text)
  return str(hex(int(text,2))[:-1])  

def blocks_to_file(blocks,filename):
  blocks = map(''.join,zip(*[iter("".join(blocks))]*2))

  with open(filename, 'ab+') as f:
    for bit in blocks:
      f.write(binascii.unhexlify(bit))


def addition_modulo(blocks1,blocks2):
  nombre1 = str(blocks1)
  nombre2 = str(blocks2)
  nombre1 = (int(nombre1,16) + int(nombre2,16))%65536
  return str(format(nombre1,'04x'))  

def multiplication_modulo(blocks1,blocks2):
  if int(blocks1,16)==0:
    nombre1 = "0x10000"
  if int(blocks2,16)==0:
    nombre2 = "0x10000"

  nombre1 = str(blocks1)
  nombre2 = str(blocks2)
  nombre1 = (int(nombre1,16) * int(nombre2,16))%65537
  if nombre1==0x10000:
    nombre1=0

  #nombre1 = format(nombre1, 'b')    

  return str(format(nombre1,'04x'))  

  #nombre1 = format(nombre1, 'b')    
  #return str(format(nombre1,'04x'))  

"""def xor(blocks1,blocks2):
  nombre1 = BitArray(hex=format(int(blocks1,16),'04x'))
  nombre2 = BitArray(hex=format(int(blocks2,16),'04x')) 
  nombre1 =(nombre1^nombre2).hex
  return nombre1"""

def xor(blocks1,blocks2):
  #nombre1 = BitArray(hex=format(int(blocks1,16),'16x'))
  #nombre2 = BitArray(hex=format(int(blocks2,16),'16x')) 
  #print nombre1,nombre2
  nombre1 =(BitArray(hex=blocks1)^BitArray(hex=blocks2)).hex
  return nombre1

def neg(cle):
    nombre = str(cle)
    nombre = 65536 - int(nombre,16)
    return format((nombre),"04x")

def pgcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = pgcd(b % a,a)
    return (g, x - (b // a) * y, y)
def inv(cle):
    if int(cle,16)==0:
      return 0

    m = 65537
    a = int(cle,16)
    g, x, y = pgcd(a, m)
    if g != 1:
        raise Exception('inverse modulaire non existant')
    else:
        j = format((x % m),"04x")
        return j

def creation_sous_cles(cle):
        temp_key = cle
        #print temp_key
        liste_des_cles_de_round = []
        real_keys = [] 
        for i in range(7):
            liste_des_cles_de_round.append(map(''.join,zip(*[iter(temp_key)]*4)))
            for j in range(8):
                   real_keys.append(liste_des_cles_de_round[i][j])

            temp_key = permutation_circulaire(temp_key)

        
        liste_des_cles_de_round = real_keys[0:52]
        return liste_des_cles_de_round

def creation_sous_cles2(cle):
  temp_key = cle
  #print temp_key
  liste_des_cles_de_round = []
  real_keys = [] 
  N = len(cle)/8
  while (len(real_keys) < 52):
      for i in range(N):
        liste_des_cles_de_round.append(map(''.join,zip(*[iter(temp_key)]*(4))))
        for j in range(len(liste_des_cles_de_round[i])):
          real_keys.append(liste_des_cles_de_round[i][j])
          temp_key = permutation_circulaire(temp_key)

  liste_des_cles_de_round = real_keys[0:52]
  #print liste_des_cles_de_round
  return liste_des_cles_de_round

def permutation_circulaire(key):
  cle = hex_to_bin(key)
  cle = cle[25:] + cle[:25]
  
  return bin_to_hex(cle)

def generer_vi():
    random_key = "vectinit"
    result = []
    for c in random_key:
       k = bin(ord(c))[2:]
       k = '00000000'[len(k):] + k
       result.extend([int(b) for b in k])
    key_bin = str(result)
    cle = ""
    for x in range(len(result)):
       y = str(result[x],)
       cle = cle + y
    return cle

def creation_cle_de_dechiffrement(cle):
    cle = creation_sous_cles2(cle)
    dechif_key = []
    i = 1
    dechif_key.append(inv(cle[len(cle)-i-3]))
    dechif_key.append(neg(cle[len(cle)-i-2]))
    dechif_key.append(neg(cle[len(cle)-i-1]))
    dechif_key.append(inv(cle[len(cle)-i]))
    dechif_key.append((cle[len(cle)-i-5]))
    dechif_key.append((cle[len(cle)-i-4]))
    i = i+6
    while(len(dechif_key)<len(cle)-4):
        dechif_key.append(inv(cle[len(cle)-i-3]))
        dechif_key.append(neg(cle[len(cle)-i-1]))
        dechif_key.append(neg(cle[len(cle)-i-2]))
        dechif_key.append(inv(cle[len(cle)-i]))
        dechif_key.append((cle[len(cle)-i-5]))
        dechif_key.append((cle[len(cle)-i-4]))
        i = i+6

    dechif_key.append(inv(cle[0]))
    dechif_key.append(neg(cle[1]))
    dechif_key.append(neg(cle[2]))
    dechif_key.append(inv(cle[3]))
    #print dechif_key
    return dechif_key

def generer_vi():
    # On demande à l'utilisateur d'écrire sa clé composée de 16 caractères ascii
    #random_key = str(raw_input(" veuillez entrer une clé de 16 caractères : "))

    #clé arbitraire à changer: 
    random_key = "jason_M0"
    result = []
    key_hex = binascii.hexlify(random_key)
    #print "Vecteur d'Initialisation = ", key_hex
    return key_hex


def chiffrement_ecb(bloc,cle):
  k = 0
  blocs_chiffres = []

  while (len(blocs_chiffres)!=len(bloc)):
    #print len(bloc) 
    #print len(blocs_chiffres)
    blocs = [bloc[k],bloc[k+1],bloc[k+2],bloc[k+3]]
    cipher = chiffrement(blocs,cle)
    blocs_chiffres.append(cipher[0])
    blocs_chiffres.append(cipher[1])
    blocs_chiffres.append(cipher[2])
    blocs_chiffres.append(cipher[3])
    k = k+4
  return blocs_chiffres  

def chiffrement_CBC(blocks,cle):
    ciph_bloc = []
    #Vecteur d'initialisation 
    VI = generer_vi()
    #VI = bin(int(VI,16))

    #le premier bloc qui sera xor avec le vecteur d'initilisation
    B = "".join(blocks[0:4])
    #B = bin(B)

    #Xor en question
    premier_bloc = xor(B,VI)

    #On xor le bloc present avec le precedent
    pb = hex_to_block(premier_bloc)
    #On applique le chiffrement sur le bloc pb
    dernier_ciph_bloc = chiffrement(pb,cle)
    ciph_bloc.append(dernier_ciph_bloc[0])
    ciph_bloc.append(dernier_ciph_bloc[1])
    ciph_bloc.append(dernier_ciph_bloc[2])
    ciph_bloc.append(dernier_ciph_bloc[3])
    for b in range(4,(len(blocks)),4):

        B = "".join(blocks[b:b+4])


        dernier_ciph_bloc = "".join(ciph_bloc[b-4:b])
        block = hex_to_block(xor(B,(dernier_ciph_bloc)))
        t = chiffrement(block,cle)
        ciph_bloc.append(t[0])
        ciph_bloc.append(t[1])
        ciph_bloc.append(t[2])
        ciph_bloc.append(t[3])


    return ciph_bloc

def chiffrement_PCBC(blocks,cle):
  ciph_bloc = []
  VI = generer_vi()
  B = "".join(blocks[0:4])
  premier_bloc = xor(B,VI)
  pb = hex_to_block(premier_bloc)
  dernier_ciph_bloc = chiffrement(pb,cle)
  ciph_bloc.append(dernier_ciph_bloc[0])
  ciph_bloc.append(dernier_ciph_bloc[1])
  ciph_bloc.append(dernier_ciph_bloc[2])
  ciph_bloc.append(dernier_ciph_bloc[3])  
  for b in range(4,(len(blocks)),4):
    dernier_B = format(int("".join(blocks[b-4:b]),16),'016x')
    B = "".join(blocks[b:b+4])
    dernier_ciph_bloc = format(int("".join(ciph_bloc[b-4:b]),16),'016x')
    dernier_ciph_bloc = xor(dernier_ciph_bloc,dernier_B)
    block = hex_to_block(xor(B,(dernier_ciph_bloc)))
    t = chiffrement(block,cle)
    ciph_bloc.append(t[0])
    ciph_bloc.append(t[1])
    ciph_bloc.append(t[2])
    ciph_bloc.append(t[3])

  return ciph_bloc


def dechiffrement_PCBC(blocks,cle):
  deciph_bloc = []
  #Vecteur d'Initialisation
  VI = generer_vi()
  #premiers 8 blocs blocs_chiffres
  B = blocks[0:4]
  #on dechiffre les premiers blocks
  deciph_bloc_tmp = chiffrement(B,cle)
  deciph_bloc =  hex_to_block(xor("".join(deciph_bloc_tmp),VI))
  for b in range(4,(len(blocks)),4):
    B = blocks[b:b+4]
    precedent_B = blocks[b-4:b]
    #on dechiffre les blocs
    deciph_bloc_tmp = chiffrement(B,cle)
    #bloc chiffre precedent utilise pour xorer le suivant
    xor1 = xor(format(int("".join(precedent_B),16),'016x'),format(int("".join(deciph_bloc[b-4:b]),16),'016x'))
    deciph_bloc.extend(hex_to_block(xor("".join(deciph_bloc_tmp),\
    "".join(xor1))))
  return deciph_bloc   

def dechiffrement_CBC(blocks,cle):

    deciph_bloc = []

    #Vecteur d'initialisation
    VI = generer_vi()
    #premiers 8 blocs chiffres
    B = blocks[0:4]
    #on dechiffre les premiers bloc
    deciph_bloc_tmp = chiffrement(B,cle)
    deciph_bloc =  hex_to_block(xor("".join(deciph_bloc_tmp),VI))
    for b in range(4,(len(blocks)),4):


        B = blocks[b:b+4]

        precedent_B = blocks[b-4:b]

        #on dechiffre les blocs
        deciph_bloc_tmp = chiffrement(B,cle)
        #bloc chiffre precedent utilise pour xorer le suivant
        deciph_bloc.extend(hex_to_block(xor("".join(deciph_bloc_tmp),\
            "".join(precedent_B))))

    return deciph_bloc

def chiffrement(bloc,cle):
  liste_des_cles_de_round = cle
  Bloc_chiffre = []
  k = 0
  while(len(Bloc_chiffre)!=len(bloc)):

    B1 = bloc[k]
    B2 = bloc[k+1]
    B3 = bloc[k+2]
    B4 = bloc[k+3]
    i = 0
    for j in range(8):

      B1 = multiplication_modulo(B1,liste_des_cles_de_round[i])
      B2 = addition_modulo(B2,liste_des_cles_de_round[i+1])
      B3 = addition_modulo(B3,liste_des_cles_de_round[i+2])
      B4 = multiplication_modulo(B4,liste_des_cles_de_round[i+3])
      #print B1,B3
      T1 = xor(B1,B3)
      T2 = xor(B2,B4)
      T1 = multiplication_modulo(T2,liste_des_cles_de_round[i+4])
      T1 = addition_modulo(T1,T2)
      T2 = multiplication_modulo(T2,liste_des_cles_de_round[i+5])
      T1 = addition_modulo(T1,T2)
      B1 = xor(B1,T2)
      B3 = xor(B3,T2)
      B2 = xor(B2,T1)
      B4 = xor(B4,T1)

      B2,B3 = B3,B2
      i=i+6

    B2,B3 = B3,B2
    B1 = multiplication_modulo(B1,liste_des_cles_de_round[48])
    B2 = addition_modulo(B2,liste_des_cles_de_round[49])
    B3 = addition_modulo(B3,liste_des_cles_de_round[50])
    B4 = multiplication_modulo(B4,liste_des_cles_de_round[51])

    Bloc_chiffre.append(B1)
    Bloc_chiffre.append(B2)
    Bloc_chiffre.append(B3)
    Bloc_chiffre.append(B4)

    k=k+4
    #print len(Bloc_chiffre)
    #print Bloc_chiffre
    ciph_string = block_to_strings(Bloc_chiffre)
    #print ciph_string
  return Bloc_chiffre

def mode_de_chiffrement(mode, filename, key):
  bloc = file_to_hex(filename)
  bloc = hex_to_block(bloc)
  k = creation_sous_cles2(binascii.hexlify(key))
  if mode == 1:
    c = chiffrement_ecb(bloc,k)
    blocks_to_file(c,'ciphered_ecb')
    print "Vous trouverez le fichier chiffre dans 'ciphered_ecb'"
  elif mode == 2:
    c = chiffrement_CBC(bloc,k)
    blocks_to_file(c,'ciphered_cbc')
    print "Vous trouverez le fichier chiffre dans 'ciphered_cbc'"
  elif mode == 3:
    c = chiffrement_PCBC(bloc,k)
    blocks_to_file(c,'ciphered_pcbc')
    print "Vous trouverez le fichier chiffre dans 'ciphered_pcbc'"
  else:
    print "euh... ce mode n'existe pas, desole"

def mode_de_dechiffrement(mode, filename, key):
  
  bloc = file_to_hex(filename)
  bloc = hex_to_block(bloc)
  #k = creation_sous_cles2(str(key))
  k = creation_cle_de_dechiffrement((binascii.hexlify(key)))
  if mode == 1:
    d = chiffrement_ecb(bloc,k)
    d1 =  block_to_strings(d)
    print d1
    strings_to_file(d1,"deciphered_ecb")
    print ""
    print ""
    print "Vous trouverez le fichier chiffre dans 'deciphered_ecb'"
    #d2 =  blocks_to_file(d,"deciphered_ecb")
  elif mode == 2:
    d = dechiffrement_CBC(bloc,k)
    d1 =  block_to_strings(d)
    print d1
    #d2 = blocks_to_file(d,"deciphered_cbc")
    strings_to_file(d1,"deciphered_cbc")
    print ""
    print ""
    print "Vous trouverez le fichier chiffre dans 'deciphered_cbc'"
  elif mode == 3:
    d = dechiffrement_PCBC(bloc,k)
    d1 =  block_to_strings(d)
    print d1
    #d2 = blocks_to_file(d1,"deciphered_pcbc")
    strings_to_file(d,"deciphered_pcbc")
    print ""
    print ""
    print "Vous trouverez le fichier chiffre dans 'deciphered_pcbc'"
  else:
    print "euh... ce mode n'existe pas, desole" 
#string = block_to_strings(b)
#c = strings_to_file(string,"deciphered_text")
#l = hex_to_bin(k)
#m = bin_to_hex(l)
#print m
#x = xor('12de','1122')
"""
#print(k)
bloc = file_to_hex("homme.jpeg")
bloc = hex_to_block(bloc)
#print bloc

print"######################################################### Begining ECB ciphering ##################################"
print ""
print ""

k = generer_la_cle2()
k = creation_sous_cles2(k)

c = chiffrement_ecb(bloc,k)
blocks_to_file(c,'ciphered')
#print " ceci est le chiffré de notre fichier:                   " + (block_to_strings(c))

print " ######################################################### finishing ECB ciphering ################################## "
print ""
print ""

print '######################################################### Begining ECB deciphering ##################################"'
print ""
print ""

k1 = creation_cle_de_dechiffrement(generer_la_cle2())

d = chiffrement_ecb(c,k1)
#print d
#d3 = block_to_strings(d)
d3 =  blocks_to_file(d,"d.jpeg") 
#print block_to_strings(d)
#strings_to_file(d3,"d.png",)
print ""
print ""

print"######################################################### Begining CBC ciphering ##################################"
print ""
print ""

c1 = chiffrement_CBC(bloc,k)
print " ceci est le chiffré de notre fichier:                   " + (block_to_strings(c1))
print ""
print ""

print "######################################################### finishing CBCciphering ################################## "
print ""
print ""


print"######################################################### Begining CBC deciphering ##################################"
print  ""

k1 = creation_cle_de_dechiffrement(generer_la_cle2())
d1 = dechiffrement_CBC(c1,k1)
d2 = block_to_strings(d1)
print block_to_strings(d1)
strings_to_file(d2,"d.png",)


print"######################################################### Begining PCBC ciphering ##################################"
print ""
print ""

c4 = chiffrement_PCBC(bloc,k)
print " ceci est le chiffré de notre fichier:                   " + (block_to_strings(c4))
print ""
print ""

print"######################################################### Begining PCBC deciphering ##################################"
print ""
print ""


k5 = creation_cle_de_dechiffrement(generer_la_cle2())
d3 = dechiffrement_PCBC(c4,k5)
d4 = block_to_strings(d3)
print block_to_strings(d3)
strings_to_file(d4,"d.png",)

"""

"""
bloc = file_to_hex("homme.jpeg")
bloc = hex_to_block(bloc)
k = generer_la_cle2()
k = creation_sous_cles2(k)
c = chiffrement_CBC(bloc,k)
blocks_to_file(c,'ciphered')

k1 = creation_cle_de_dechiffrement(generer_la_cle2())
d1 = dechiffrement_CBC(c,k1)
d2 = blocks_to_file(d1,"d3.jpeg")
#print d2
"""