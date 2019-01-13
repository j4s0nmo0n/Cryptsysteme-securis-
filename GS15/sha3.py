# -*-coding:Latin-1 -*
import fileinput
import numpy as np
import random
import os
import binascii
import bitarray
import dh
#from bitstring import bitArray
from convert import *


def padding(msg_bin,r): #La fonction de padding pour obtenir un message multipe de r
	if r==8:
		msg_bin.fill() #
	else:
		add=r-msg_bin.length()%r #Calcul du nombre de bits de bourrage à ajouter
		for i in list(range(add)):
			msg_bin.append(False) #Ajout des bits de bourrage
	return msg_bin

def parite(msg_bin): #Fonction qui teste la parite de notre message binaire
	nb_of_1=msg_bin.count()

	if nb_of_1%2==0:
		return 0 #Notre message binaire est paire
	else:
		return 1 #Notre message binaire est impaire 

def bloc_to_matrice(bloc): #On tranforme une matrice qui permettra d'utiliser les différentes routines de la fonction de permutation par blocs de Keccak
	matrice = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]] #On réalise l'initialisation avec un bloc constitue uniquement de 0
	for i in list(range(len(matrice))):
		for j in list(range(len(matrice[i]))):
			matrice[i][j]=bloc[320*i+64*j:320*i+64*(j+1)] #Bloc de 1600 bits constitue de 5x5 sous blocs de 64 bits
	return matrice

def matrice_to_bloc(matrice): #On retransforme la matrice en un bloc
	bloc=bitarray.bitarray() #On crée un tableau de bits vide 
	for i in list(range(len(matrice))):
		for j in list(range(len(matrice[i]))):
			for k in list(range(64)): #Les sous-bloc sont d'une taille de 64 bits
				bloc.append(matrice[i][j][k]) #On remplit le bloc 
	return bloc

def lfsr(iter): #La routine iota defini plus loin doit utiliser une sequence LFSR de degre 8     
	seed='11001001' 
	taps=(8,7,6,1)
	sr, xor= seed, 0
	for i in list(range(iter)):
		xor=0
		for t in taps:
			xor += int(sr[t-1])
		if xor%2 == 0.0:
			xor = 0
		else:
			xor = 1
		sr= str(xor) + sr[:-1]
	return xor

def theta(matrice): #Routine θ de la fonction de permutation par blocs de Keccak 
	matrice_bis=matrice
	for i in list(range(len(matrice))):
		for j in list(range(len(matrice[i]))):
			for k in list(range(len(matrice[i][j]))):
				colonne=bitarray.bitarray(5) #On génére un colonne de bits
				for l in list(range(len(matrice))):
					colonne[l]=matrice[l][j][(k-1)%64] #On incrémente la colonne avec la colonne de la marice
				xor=parite(colonne) #On détermine la partié de la colonne
				matrice_bis[i][j][k]=matrice[i][j][k]^xor 
	return matrice_bis

def rho(matrice): #Routine ρ de la fonction de permutation par blocs de Keccak
	for i in list(range(len(matrice))):
		for j in list(range(len(matrice[i]))):
			t= (i*5)+j+1 #On détermine t qui est la position de chaque sous bloc décalée de 1
			sous_bloc=bitarray.bitarray(64) #on utilise un sous-bloc de 64 bits qui va nous permettre d'effectuer le décalage circulaire 
			for k in list(range(len(sous_bloc))):
				sous_bloc[k]=matrice[i][j][(k+t)%64] #On effectue le décalage circulaire de t positions vers la gauche
			matrice[i][j]=sous_bloc 
			sbloc_inter=0 #On remet le sous-bloc à 0

	return matrice

def pi(matrice): #Routine π de la fonction de permutation par blocs de Keccak
	motif = [ [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0], ] #Création d'un motif fixé qui va permettre la permutation des 25 mots
	for i in list(range(len(matrice))):
		for j in list(range(len(matrice[i]))):
			motif[i][j]=matrice[j][(2*i+3*j)%5] #La permutation est effectuée pour chaque sous-bloc

	matrice=motif #La matrice prend la valaur du motif après permutation
	return matrice

def ksi(matrice): #Routine χ de la fonction de permutation par blocs de Keccak
	matrice_bis=matrice
	for i in list(range(len(matrice))):
		for j in list(range(len(matrice[i]))):
			matrice_bis[i][j]=matrice[i][j]^(matrice[i][(j+1)%5]&matrice[i][(j-1)%5]) #On combine les lignes bit à bit
	matrice=matrice_bis
	return matrice

def iota(matrice):
	#Routine ι de la fonction de permutation par blocs de Keccak
	matrice_bis=matrice
	for i in list(range(5)):
		for j in list(range(7)):
			matrice[i][i][((2**j)-1)%64]=(matrice[i][i][((2**j)-1)%64]^matrice[i][i][(j+7*lfsr(j))%64]) #A chaque iteration, on effectue le XOR de matrice[i][i]*[(2^m)-1) avec le bit j+7i d'une séquence LFSR de degré 8

	matrice=matrice_bis

	return matrice

def permutation(msg_bin):
	N=24 #Nombre d'itération de la permutation
	permutation=bloc_to_matrice(msg_bin) #On transforme le bloc en matrice afin d'effectuer la permutation
	for i in list(range(N)): #On applique les différentes routine de la permutation par blocs de Keccak
		permutation=theta(permutation)
		permutation=rho(permutation)
		permutation=pi(permutation)
		permutation=ksi(permutation)
		permutation=iota(permutation)
	permutation=matrice_to_bloc(permutation) #On retransforme la matrice en bloc
	return permutation

def hashing_sha3(msg, p=256):
	msg = str(msg)
	msg_bin = string2bin(msg)
	bloc_size=1600 #Blocs de 1600 bits
	n_iter=24 #Nombre d'itérations de la fonction de permutation
	c=2*p  #Capacité du hash, et p la taille du hash
	r=bloc_size-c #Le taux 
	bloc=bitarray.bitarray(1600) #On définit un bloc de 1600 bits
	bloc.setall(0) #On initialise le bloc à 0	
	msg_bin=padding(msg_bin,r) #On applique la fonction de padding a notre message binaire
	P=msg_bin.length()//r #Calcul du nombre d'itération de l'absorbation 
	for i in list(range(P)):
		bloc[:r]=bloc[:r]^msg_bin[r*(i%P):r*((i%P)+1)] # On effectue le XOR entre P et r
		bloc=permutation(bloc) #On permute

	hash_bin=bloc[:p]
	hash_hex=str(bin2hex(hash_bin))

	#print ("\n hash:" + str(hash_bin))
	#print("hash en hex:" + hash_hex)

	return hash_hex




def main():
	#msg = raw_input("Veuillez entrer le message que vous souhaitez hacher: ")
	#msg = dh.main()
	#msg_bin = string2bin(msg)
	#msg_bin = string2bin(input("Veuillez entrer le message que vous souhaitez hacher: "))	
	#p=int(input("Entrez la taille du hash (256, 384 ou 512):"))
	hash_test=hashing_sha3(msg,p=256)

"""if __name__=='__main__':

        main()
"""