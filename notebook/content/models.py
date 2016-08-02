from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class RecordNotebook(models.Model):
    class Meta():
        db_table = 'record_notebook'

    owner           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name       = models.CharField(max_length=64)
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{6,15}$', message="format: '+999999'. Up to 15 digits allowed.")
    phone_number    = models.CharField(validators=[phone_regex], blank=False, max_length=15) # validators should be a list
    birthday        = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "Record: %s" % self.full_name
