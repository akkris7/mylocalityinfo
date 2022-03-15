from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from .fields import LowerCharField


class Category(models.Model):
	name = LowerCharField(max_length = 50, unique = True)

	def __str__(self):
		return self.name


class Service(models.Model):
	name 	 = models.CharField(default = '' , max_length = 100)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	contact  = models.CharField(default = '' , max_length = 15)
	address  = models.TextField()
	landmark = models.CharField(default = '' , max_length = 100, null = True, blank = True)
	admin    = models.ForeignKey('account.User', on_delete = models.SET_NULL, null = True, blank = True, related_name="controlledby")
	image    = models.ImageField(upload_to = 'thumb', null = True, blank = True)

	def __str__(self):
		return self.name


@receiver(pre_delete, sender = Service)
def delete_image(sender, instance, **kwargs):
    instance.image.delete(False)