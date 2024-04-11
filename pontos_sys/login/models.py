from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # We'll use email as the unique identifier
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    points = models.PositiveIntegerField('pontos', default=0)
    cc = models.CharField(max_length=30, default=False)
    is_rh = models.BooleanField(default=False)
    manager_points = models.PositiveIntegerField('manager_points', default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Transaction(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_transactions')#sender
    AMOUNT_CHOICES = [
        (50, '50'),
        (100, '100'),
        (150, '150'),
        (200, '200'),
    ]
    amount = models.IntegerField(choices=AMOUNT_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    reciever = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recieved_transactions')

    
""" def __str__(self):
        return f"Transaction for {self.user.email}: {self.amount}" """

@receiver(post_save, sender=Transaction)
def update_receiver_points(sender, instance, created, **kwargs):
    if created:
        receiver = instance.reciever
        if receiver.points is None:
            receiver.points = instance.amount
        else:
            receiver.points += instance.amount
        receiver.save()
        
        
class Requests(models.Model):
    requester = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_requests')
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    quantidade = models.PositiveIntegerField('quantidade', default=False)