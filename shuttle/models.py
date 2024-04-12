from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail

import uuid

class User(AbstractUser):
    registration_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(('email address'), unique=True)
    rfid_id = models.CharField(max_length=255, blank=True, null=True)  # Allow null RFID ID
    USERNAME_FIELD = 'registration_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.registration_number

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to user model
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Account balance

    def __str__(self):
        return f"Account: {self.user.username} - Balance: {self.balance}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to user model
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Transaction amount
    timestamp = models.DateTimeField(auto_now_add=True)  # Transaction timestamp
    type = models.CharField(max_length=20, choices=(('ADD', 'Add'), ('SUBTRACT', 'Subtract')), default='ADD')  # Transaction type (add or subtract)
    rfid_used = models.BooleanField(default=False)  # Flag indicating if RFID was used
    rfid_id = models.CharField(max_length=255, blank=True, null=True)  # Allow null RFID ID
    reference_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4().hex)  # Unique reference ID for preventing multiple taps

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
