from django.db import models
import secrets

class Secret(models.Model):
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=512)
    name_nonce = models.CharField(max_length=64)
    value_nonce = models.CharField(max_length=64)
    service_aid = models.CharField(max_length=64)

class Service(models.Model):
    uid = models.CharField(max_length=200)
    sym_key = models.CharField(max_length=512)
    admin_aid = models.CharField(max_length=64)

    def save(self):
        if not self.uid:
            uid = secrets.token_hex(nbytes=32)
            while Service.objects.filter(uid=uid).exists():
                uid = secrets.token_hex(nbytes=32)
            self.uid = uid
        return super().save()

class SecretSalt(models.Model):
    number = models.PositiveIntegerField()
    service_aid = models.CharField(max_length=64)
