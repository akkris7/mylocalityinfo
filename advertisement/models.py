from django.db import models


AD_TYPE = (
	('large', 'Large'),
	('small', 'Small')
)

class Advertisement(models.Model):
	location = models.ForeignKey('location.Location', on_delete = models.SET_NULL, null = True, blank = True)
	image = models.ImageField(upload_to = 'ads')
	expiry = models.DateField(null = True, blank = True)
	ad_type = models.CharField(max_length = 10, choices = AD_TYPE, default = 'small', )