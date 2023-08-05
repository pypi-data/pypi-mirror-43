from django.db import models, transaction, IntegrityError
from django.contrib.auth.models import User
from uuid import uuid4


class BaseModel (models.Model):
  created_at = models.DateTimeField(
    'created_at',
    'createdAt',
    auto_now_add  = True
  )

  updated_at = models.DateTimeField(
    'updated_at',
    'updatedAt',
    auto_now      = True
  )

class NumberSystem (BaseModel):
  objects = models.Manager()

  name = models.CharField(
    verbose_name  = 'name',
    max_length    = 20,
    primary_key   = True
  )

  population = models.TextField(
    verbose_name  = 'population'
  )

  @property
  def base (self):
    return len(self.population)

  @classmethod
  def decimal_system (cls):
    system = cls.objects.create(
      name        = 'DECIMAL',
      population  = '0123456789'
    )
    return system


class Counter (BaseModel):
  objects = models.Manager()

  key = models.UUIDField(
    verbose_name  = 'key',
    primary_key   = True,
    default       = uuid4,
    editable      = False
  )

  count = models.IntegerField(
    verbose_name  = 'count',
    default       = 0
  )

  @classmethod
  def create_counter (cls):
    counter = cls.objects.create()
    return counter
  
  @classmethod
  def get_counters (cls):
    counters = cls.objects.all()
    return counters
  
  @classmethod
  def get_counter (cls, key):
    try:
      counter = cls.objects.get(key = key)
      return counter
    except:
      return None
  
  @classmethod
  def add (cls, key, val):
    try:
      with transaction.atomic():
        counter = cls.objects.select_for_update().get(key = key)
        counter.count += val
        counter.save()
        return True
    except (IntegrityError, cls.DoesNotExist):
      return False
  
  @classmethod
  def subtract (cls, key, val):
    return cls.add(key, -val)

  @classmethod
  def increament (cls, key):
    return cls.add(key, 1)
  
  @classmethod
  def decreament (cls, key):
    return cls.subtract(key, 1)
