from __future__ import division

import hmac
import hashlib
import sys
import secrets
import base64

if sys.version_info[0] == 3:
	buffer = lambda x: x

#Define expand in HKDF for Blake2b
def hkdf_expand(pseudo_random_key, info=b"", length=32, hash=hashlib.blake2b):
	hash_len = hash().digest_size
	length = int(length)
	if length > 255 * hash_len:
		raise Exception("Cannot expand to more than 255 * %d = %d bytes using the specified hash function" %\
			(hash_len, 255 * hash_len))
	blocks_needed = length // hash_len + (0 if length % hash_len == 0 else 1) # ceil
	okm = b""
	output_block = b""
	for counter in range(blocks_needed):
		output_block = hmac.new(pseudo_random_key, buffer(output_block + info + bytearray((counter + 1,))),\
			hash).digest()
		okm += output_block
	f = bytearray(okm[:length])
	return f
	for i in range(len(f)):
	 f[i]= 0

class BlakeStreamCipher:
    def encrypt(plaintext, key):
        #Encrypt the bytes of the plaintext with the keystream
        stream = bytearray(hkdf_expand(key, info=b"", length=(len(plaintext)), hash=hashlib.blake2b))
        f = bytearray(x^y for x, y in zip(plaintext, stream))
        return f
        for i in range(len(stream)):
            stream[i] = 0
        for i in range(len(f)):
            f[i] = 0

    decrypt = encrypt

print ("Input plaintext:")
plaintext = bytearray(input().encode())
print ("Input password:")
password = bytearray(input().encode())
salt = bytearray(secrets.token_bytes(32))
key = bytearray(hashlib.pbkdf2_hmac('sha512', password, salt, 500000, dklen=64))
ciphertext = bytearray(BlakeStreamCipher.encrypt(plaintext, key))
print ("Ciphertext:", base64.b64encode(ciphertext+salt).decode('utf-8'))

#Clear memory
for i in range(len(plaintext)):
    plaintext[i] = 0
for i in range(len(password)):
    password[i] = 0
for i in range(len(salt)):
    salt[i] = 0
for i in range(len(key)):
    key[i] = 0
for i in range(len(ciphertext)):
    ciphertext[i] = 0
input()

