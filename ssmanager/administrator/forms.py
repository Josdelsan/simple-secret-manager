from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from api.models import Service, SecretSalt
from misc.crypto import encrypt_rsa
from misc.utils import encrypt_and_serialize, create_anonimized_ids
import secrets
from hashlib import sha256


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ServiceSecretsForm(forms.Form):
    sym_key = forms.CharField()
    pub_key = forms.CharField()
    secrets_list = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ServiceSecretsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        sym_key = self.cleaned_data['sym_key']
        pub_key = self.cleaned_data['pub_key']
        secrets_list = self.cleaned_data['secrets_list']

        #Generate Service
        uid = secrets.token_hex(nbytes=32)
        while Service.objects.filter(uid=uid).exists():
            uid = secrets.token_hex(nbytes=32)
        encrypted_uid = encrypt_rsa(pub_key, uid)
        encrypted_sym_key = encrypt_rsa(pub_key, sym_key)
        service = Service(uid=encrypted_uid,sym_key=encrypted_sym_key,admin_aid=self.user.id)

        #Serialize and encrypt secrets
        encrypted_secrets_list = encrypt_and_serialize(secrets_list, sym_key)


        #Generate Secrets salt
        number = len(encrypted_secrets_list)
        service_aid = sha256(uid.encode('utf-8')).hexdigest()
        secret_salt = SecretSalt(number=number, service_aid=service_aid)

        #Generate uids, assign to secrets and persist
        anonimized_ids = create_anonimized_ids(uid, number)
        for secret in encrypted_secrets_list:
            aid = anonimized_ids.pop(0)
            secret.service_aid = aid
            secret.save()

        service.save()
        secret_salt.save()

        return service.id

    
            

        