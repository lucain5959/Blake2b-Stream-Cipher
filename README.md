# Blake2b-Stream-Cipher
Use Python's hashlib library to turn Blake2b into a stream cipher

Enter your plaintext and password. The password is turned into the encryption key using PBKDF2-SHA512 with 500,000 iterations. The Encryption key is hashed with Blake2b using HDKF expand to create a keystream. The 256 bit salt used for PBKDF2 is then appended to the ciphertext. 
