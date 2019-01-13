#!/usr/bin/python
# -*-coding:Latin-1 -*
import bitarray
#from bitstring import bitarray
import binascii


#conversion chaine vers bits
def string2bin(chaine):
	chaine_bin = bitarray.bitarray()
	chaine_bin.frombytes(chaine.encode('utf-8'))
	return chaine_bin

#conversion bits vers chaine
def bin2string(binaire):

	return binaire.tobytes().decode('utf-8')

#conversion bitarray vers hex
def bin2hex(binaire):
	return binascii.hexlify(binaire.tobytes())

#conversion binaire vers entier
def bin2int(binaire):
	n=0
	#print(len(binaire))

	for i in list(range(len(binaire))):
		n = n<<1 | binaire[i]

	#print(n, len(binaire))
	return n, len(binaire)

#conversion entier vers binaire
def int2bin(entier,taille):

	n=entier
	array=[]

	#methode classique de conversion decimal vers binaire
	for i in list(range(taille)) :
		reste=n%2
		array.append(reste)
		n//=2

	binaire=bitarray(array)
	binaire.reverse()

	return binaire

#somme binaire sur 2 bitarrays
def bitarray_sum(a,b):
	a, taille_a=bin2int(a)
	b, taille_b=bin2int(b)

	c=a+b
	c=int2bin(c,max(taille_a,taille_b))

	#print(c)
	return(c)

#multiplication binaire
def bitarray_mult(a,b):
	#print ("a = " + str(a) + " et b = " + str(b))
	a, taille_a=bin2int(a)
	b, taille_b=bin2int(b)

	#print ("a = " + str(a) + " et b = " + str(b))
	c=a*b
	#print("C avant = " + str(c))
	c=int2bin(c,max(taille_a,taille_b))

	#print("C = " + str(c))
	return(c)



#test de la conversion si convert_bin.py execute seul
if __name__=='__main__':
	a = raw_input("Veuillez entrer un message:")


	b=string2bin(a)
	print("message en binaire:")
	print(b)


	print("message en hex:"+str(bin2hex(b)))

	c= bin2string(b)

	print ("message reconverti: " + c)

	bin2int(bitarray('0011'))

	int2bin(3, 4)

	bitarray_sum(bitarray('1111'), bitarray('0001'))

	bitarray_mult(bitarray('0011'), bitarray('0110'))


