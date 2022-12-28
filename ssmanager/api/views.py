from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from misc.crypto import decrypt_aes, decrypt_rsa
from misc.utils import decrypt_and_serialize, create_anonimized_ids
from api.models import Service, SecretSalt, Secret

from hashlib import sha256

@api_view(['POST'])
def secrets_list(request):

    priv_key = request.POST.get('priv_key','')
    service_id = request.POST.get('service_id','')
    if priv_key and service_id:
        try:
            #Decrypt service uid
            service = Service.objects.get(id=service_id)
            service_uid = decrypt_rsa(priv_key, service.uid)
            service_aid = sha256(service_uid.encode('utf-8')).hexdigest()

            #List encrypted secrets
            secrets_salt = SecretSalt.objects.get(service_aid=service_aid)
            secrets_aids = create_anonimized_ids(service_uid, secrets_salt.number)
            encrypted_secrets_list = list(Secret.objects.filter(service_aid__in=secrets_aids).values('name', 'value', 'name_nonce', 'value_nonce'))

            #Decrypt sym key and secrets
            sym_key = decrypt_rsa(priv_key, service.sym_key)
            secrets_list = decrypt_and_serialize(encrypted_secrets_list, sym_key)

            return JsonResponse({'secrets':secrets_list})
        except Exception as e:
            return JsonResponse({'error': e}, status=500)

    return JsonResponse({'error': 'Something is missing'}, status=400)


