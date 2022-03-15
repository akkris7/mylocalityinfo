from django.db import models
from .fields import LowerCharField


class Location(models.Model):
	name = LowerCharField(max_length = 100, unique = True)
	image    = models.ImageField(upload_to = 'place', null = True, blank = True)

	def __str__(self):
		return self.name