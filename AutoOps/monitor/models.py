from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Mem(models.Model):
	mem_values = models.CharField(max_length=64)
	mem_times = models.CharField(max_length=64)
	def __unicode__(self):
		return self.mem_values


class cpu_load_info(models.Model):
	cpu_type = models.CharField(max_length=64)
	cpu_loads_val = models.CharField(max_length=64)
	info_times = models.CharField(max_length=64)
	def __unicode__(self):
		return self.info_times

