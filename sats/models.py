# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class School(models.Model):

	name = models.CharField(max_length=128)
	building_no = models.IntegerField()
	street = models.CharField(max_length=128)
	city = models.CharField(max_length=64)
	zone_no = models.IntegerField()
	start_time = models.TimeField()

	def __unicode__(self):
		return self.name

class Admin(models.Model):

	user = models.ForeignKey(User)
	contact_number = models.CharField(max_length=12)
	super_admin = models.BooleanField(default=False)
	school = models.ForeignKey(School, null=True, blank=True)

	def __unicode__(self):
		return ("%s, %s") % (self.user.last_name, self.user.first_name)

class Guardian(models.Model):

	RELATIONSHIP_OPTIONS = (
		("F", "Father"),
		("M", "Mother"),
		("O", "Other")
	)

	user = models.ForeignKey(User)
	relationship = models.CharField(max_length=1, choices=RELATIONSHIP_OPTIONS)
	occupation = models.CharField(max_length=64)

	def __unicode__(self):
		return ("%s %s") % (self.user.first_name, self.user.last_name)


class Tag(models.Model):

	mac_address = models.CharField(max_length=64)


	def __unicode__(self):
		return self.mac_address


class Child(models.Model):

	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	age = models.IntegerField()
	grade = models.IntegerField()
	section = models.CharField(max_length=1)
	tag = models.OneToOneField(Tag)
	school = models.ForeignKey(School)


	def __unicode__(self):
		return ("%s %s") % (self.first_name, self.last_name)


class ChildGuardian(models.Model):

	child = models.ForeignKey(Child)
	guardian = models.ForeignKey(Guardian)

	def __unicode__(self):
		return ("Guardian %s, Child %s") % (self.guardian, self.child)


class Sniffer(models.Model):

	name = models.CharField(max_length=64)
	number = models.IntegerField()
	school = models.ForeignKey(School)

	def __unicode__(self):
		return ("Sniffer #%d, %s, %s") % (self.number, self.school.name, self.name)


class TagUpdate(models.Model):

	tag = models.ForeignKey(Tag)
	sniffer = models.ForeignKey(Sniffer)
	time_stamp = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return str(self.time_stamp)

 		