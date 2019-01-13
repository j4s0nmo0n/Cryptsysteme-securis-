#/usr/bin/python
#!/usr/bin/python
# -*-coding:Latin-1 -*
import sha3 as sha_3
import rsa_main as rsa_main
import rsa_encrypt as encrypt
import rsa_decrypt as decrypt
import dh
import idea 
import binascii
def choix():
	"""
	Nous affichons les differents choix possibles pour l'Utilisateur
	"""	 
	print "Quelles operations souhaitez vous faire ?"
	print "->1<- Generer une cle publique /privee"
	print "->2<- Authentifier une cle publique / un certificat"
	print "->3<- Partager une cle secrete"
	print "->4<- Utiliser une cle secrete pour chiffrer un message(et le signer)"
	print "->5<- Dechiffrer un message"
	# Not implemented
	print "->6<- THE FULL MONTY"
	return raw_input("Entrez votre choix : ")

def check(choix):

	print ("-----------------------------------")
	print ("PROTOCOLE DE COMMUNICATION SECURISE")
	print ("-----------------------------------")
	
	if choix == 1:
	        print("Generation de cle privee/publique")
	        rsa_main.main()
	        #encrypt.main()
	elif choix == 2:
			print 'Authentifier une cle publique'
			print 'un exemple de cle publique sera une cle de 308 digits en decimal, exemple: 107475751568390812428535047796413052113588419983754760939123105471122541356562487272721769839212907884514324492978399313843381537039135549616910195546680963193472985910684808577442857238355559140566608138405650252141245766868609406460314827361736800182770716168351588061204081405535440675621805754225577763007'
			cle = raw_input("Veuillez entrer votre cle publique : ")
			print'nous allons hasher ce message...'
			cle_hashee = sha_3.hashing_sha3(cle, p=256)
			print "le hashage de la cle nous donne :", cle_hashee

	elif choix == 3:
	        print ("Partage de cle avec Diffie Hellman")
	        dh.main()
	
	elif choix == 4:
		print "Chiffrement et dechiffrement IDEA"
		print ""
		print ""
		print "Utilisation d'une cle secrete pour chiffrer un message"
		print ""
		print ""
		print "exemple de cle de 128 bits => motdepasse123456"
		
		print ""
		print ""
		key = raw_input("\t=>Entrez votre cle de chiffrement : ")
		key = binascii.hexlify(str(key))
		print ""
		print ""
		print "Veuillez choisir le mode de chiffrement"
		print "*** >1< *** ECB"
		print "*** >2< *** CBC"
		print "*** >3< *** PCBC"
		print ""
		print ""
		mode = raw_input("mode ... : ")

		filename = raw_input("Veuillez entrer le fichier a chiffrer : ")
		idea.mode_de_chiffrement(int(mode),filename,key)
	
		#idea.mode_de_dechiffrement(int(mode),filename,key)
	elif choix == 5:
		print ""
		print ""
		print " Dechiffrement un message IDEA et verification de signature :"
		print "Utilisation d'une cle secrete pour chiffrer un message"
		print ""
		print ""
		print "exemple de cle de 128 bits => motdepasse123456"
		print ""
		print ""
		key = raw_input("\t=>Entrez votre cle de chiffrement : ")
		key = binascii.hexlify(str(key))
		print ""
		print ""
		print "Veuillez choisir le mode de chiffrement"
		print "*** >1< *** ECB"
		print "*** >2< *** CBC"
		print "*** >3< *** PCBC"
		print ""
		print ""
		mode = raw_input("votre choix est : ")
		
		print ""
		print ""
		filename = raw_input("Veuillez entrer le fichier a dechiffrer : 'en l'occurence ciphered_[mode]' :")
		idea.mode_de_dechiffrement(int(mode),filename,key)

	elif choix == 6:
			print "THE FULL MONTY"
			print ""
			print ""
			print "Generation de cle secrete"
			key = dh.main()
			print ""
			print ""
			print " hachage de la cle secrete"
			hash_key = sha_3.hashing_sha3(key, p=256)
			print ""
			print ""
			print "Cle de chiffrement : "+ str(hash_key)
			print "Chiffrement a l'aide de IDEA en mode PCBC"
			idea.mode_de_chiffrement(3,"texte",hash_key)
			print ""
			print ""
			print "Generation des cles de l'autorite avec RSA"
			rsa_main.main()
			crypted_key = encrypt.main(hash_key)
			print ""
			print ""
			print "Dechiffrement du message chiffre precedemment"
			print ""
			print ""
			idea.mode_de_dechiffrement(3,"texte",hash_key)
			print ""
			print ""	
			print"verification de la signature par dechiffrement a l'aide de cle publique: "
			decrypt.main()

	else:
	        print ("Votre choix est incorrect")



def main():
	ch = choix()
	check(int(ch))

if __name__ == '__main__':
	main()