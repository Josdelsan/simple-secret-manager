from hashlib import sha256
from misc.crypto import decrypt_aes, decrypt_rsa, encrypt_aes
import json
from api.models import Secret

def create_anonimized_ids(uid, number):
    aids = []
    for i in range(0,number):
        aux_id = uid + str(i)
        aid = sha256(aux_id.encode('utf-8')).hexdigest()
        aids.append(aid)
    return aids


def decrypt_and_serialize(encrypted_secrets_list,sym_key):
    secrets_list = []
    for secret in encrypted_secrets_list:
        name = decrypt_aes(sym_key, secret['name'], secret['name_nonce'])
        value = decrypt_aes(sym_key, secret['value'], secret['value_nonce'])
        secrets_list.append({'name':name,'value':value})
    return secrets_list

def encrypt_and_serialize(secrets_list,sym_key):
    encrypted_secrets_list = []
    secrets_list = json.loads(secrets_list)
    for s in secrets_list:
        encrypted_name, name_nonce = encrypt_aes(sym_key, s['name'])
        encrypted_value, value_nonce = encrypt_aes(sym_key, s['value'])
        secret = Secret(name=encrypted_name,value=encrypted_value,name_nonce=name_nonce,value_nonce=value_nonce)
        encrypted_secrets_list.append(secret)
    return encrypted_secrets_list

