#coding:utf8
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Dept(models.Model):
    name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=True)
    def __unicode__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(email,
            username = username,
            password = password,
        )

        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField(max_length=64, null=True)
    sex = models.CharField(max_length=2, null=True, default=2)
    role = models.IntegerField(default=1)
    dept = models.ForeignKey(Dept,null=True, blank=True)
    phone = models.CharField(max_length=255, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class YwLog(models.Model):
	RESULT_CHOICES = (
		('0', '成功'),
		('1', '失败'),
		)
	user = models.CharField(max_length=10)
	logdate = models.DateTimeField(auto_now=True,blank=True, null=True)
	msg = models.CharField(max_length=100)
	result = models.CharField(max_length=10, choices=RESULT_CHOICES)
	ipaddress = models.GenericIPAddressField(null=True)
