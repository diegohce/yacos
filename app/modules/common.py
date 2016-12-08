import os
import binascii

 
def random_hash_32(sep='-'):
	code = binascii.hexlify(os.urandom(16)).upper()
	name_l = []
	for i in range(0,31,4):
		name_l.append( code[i:i+4] )
	return sep.join(name_l)

def random_hash_16(sep='-'):
	code = binascii.hexlify(os.urandom(8)).upper()
	name_l = []
	for i in range(0,16,4):
		name_l.append( code[i:i+4] )
	return sep.join(name_l)

def random_hash_8(sep='-'):
	code = binascii.hexlify(os.urandom(4)).upper()
	name_l = []
	for i in range(0,8,4):
		name_l.append( code[i:i+4] )
	return sep.join(name_l)



if __name__ == '__main__':
	print random_hash_32()
	print random_hash_16()
	print random_hash_8()
