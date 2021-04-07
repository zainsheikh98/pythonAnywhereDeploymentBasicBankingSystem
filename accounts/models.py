from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, username, balance, password=None):

        if not email:
            raise ValueError("User Must Have A Valid Email Address")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            balance = balance
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, username, balance, password):

        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
            balance = balance
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user


class Account(AbstractBaseUser):
    email               = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined         = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    username            = models.CharField(max_length=25, default="")
    balance             = models.IntegerField(default=0, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "balance"]

    objects = AccountManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Transaction(models.Model):
    sender              = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="AccountSender")
    reciever            = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="AccountReciever")
    transferredAmount   = models.IntegerField(default=0, null=False)
    
    def __str__(self):
        return self.sender.username + " -> " + self.reciever.username