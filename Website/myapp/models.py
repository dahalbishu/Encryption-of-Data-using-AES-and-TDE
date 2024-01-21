# myapp/models.py

from django.db import models
from cryptography.fernet import Fernet

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    encrypted_credit_card = models.TextField()

    @property
    def credit_card(self):
        # Decrypt the credit card number
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        decrypted_credit_card = cipher_suite.decrypt(self.encrypted_credit_card.encode()).decode()
        return decrypted_credit_card

    def __str__(self):
        return self.name
