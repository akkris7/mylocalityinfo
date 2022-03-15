from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(email = email, **other_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_admin(self, email, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        return self._create_user(email, password, **other_fields)


    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)   

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self._create_user(email, password, **other_fields)  


    def create_staff(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('must have is_staff=True.')

        return self._create_user(email, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email        = models.EmailField(max_length = 100, unique = True)
    mobile       = models.CharField(default = '', max_length = 50, unique = True)
    name         = models.CharField(default = '' , max_length = 100)
    location     = models.OneToOneField('location.Location', on_delete = models.SET_NULL, null = True, blank = True)
    is_active    = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default = False)
    is_staff     = models.BooleanField(default = False)
    is_admin     = models.BooleanField(default = False)
    created_at   = models.DateField(auto_now_add = True)
    updated_at   = models.DateField(auto_now = True)
    profile_pic  = models.ImageField(upload_to = "profile", null = True, blank = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
    	return self.name


@receiver(pre_delete, sender = User)
def delete_profile_pic(sender, instance, **kwargs):
    instance.profile_pic.delete(False)