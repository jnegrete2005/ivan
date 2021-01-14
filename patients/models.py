from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from datetime import datetime, date

# Create your models here
class Patient(models.Model):
  """
  Represents a Patient
  """
  names = models.CharField(max_length=70)
  last_names = models.CharField(max_length=70)
  bday = models.DateField()
  cel = models.CharField(max_length=10)
  id_num = models.CharField(max_length=10)
  mail = models.EmailField()
  job = models.CharField(max_length=100)
  company = models.CharField(max_length=200, blank=True, null=True)
  allergies = models.CharField(max_length=300, blank=True, null=True)
  patho_histo = models.CharField(max_length=300, blank=True, null=True)
  fam_histo = models.CharField(max_length=300, blank=True, null=True)

  def __str__(self):
    return self.names + ' ' + self.last_names

  def get_age(self):
    """Will calculate the age according the birthday"""
    today = date.today()
    return today.year - self.bday.year - ((today.month, today.day) < (self.bday.month, self.bday.day))

  def get_all_visits(self):
    """Will return all the visits from the user"""
    return Visit.objects.filter(patient=self).order_by('-date')

  def is_first_visit(self):
    """Will check if it is the patients first visit"""
    return True if not Visit.objects.filter(patient=self) else False


class Visit(models.Model):
  """
  Represents a Visit to the doctor. It is assign to only 1 Patient
  """
  patient = models.ForeignKey(Patient, models.CASCADE, related_name='visits')
  date = models.DateTimeField(auto_now_add=True)
  symptoms = models.TextField()
  treatment = models.TextField()

  def __str__(self):
    return self.symptoms


class User(AbstractUser):
  """
  Represents a User 
  """
  def __str__(self):
    return self.username
