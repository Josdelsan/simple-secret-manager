from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode, b64encode


def decrypt_rsa(key,msg):
    key = b64decode(key)
    key = RSA.importKey(key)
    cipher = PKCS1_OAEP.new(key)
    msg_bytes = cipher.decrypt(b64decode(msg))
    return b64encode(msg_bytes).decode('utf-8')

def encrypt_rsa(key,msg):
    key = b64decode(key)
    key = RSA.importKey(key)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(b64decode(msg))
    return b64encode(ciphertext).decode('utf-8')

def decrypt_aes(key,msg,nonce):
    msg = b64decode(msg)
    nonce = b64decode(nonce)
    cipher = AES.new(bytes(key,'utf-8'), AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(msg)
    return plaintext.decode('utf-8')

def encrypt_aes(key,msg):
    cipher = AES.new(bytes(key,'utf-8'), AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(bytes(msg,'utf-8'))
    ciphertext = (b64encode(ciphertext).decode('utf-8'))
    nonce = (b64encode(nonce).decode('utf-8'))
    return ciphertext,nonce