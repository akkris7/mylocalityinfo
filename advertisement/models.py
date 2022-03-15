from django.db import models


class Advertisement(models.Model):
	location = models.ForeignKey('location.Location', on_delete = models.SET_NULL, null = True, blank = True)
	image = models.ImageField(upload_to = 'ads')
	expiry = models.DateField(null = True, blank = True)