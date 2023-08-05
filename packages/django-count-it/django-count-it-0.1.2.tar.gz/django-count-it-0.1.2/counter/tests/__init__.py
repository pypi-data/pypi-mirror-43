from django.test import TestCase
from django.shortcuts import reverse
from .decorators import test_concurrently


class FooTest (TestCase):

  def test_foo (self):

    @test_concurrently(10)
    def createCounter ():
      self.client.login(username='dsfx3d', password='rootroot')
      self.client.get(reverse('add-counter-view'))

    createCounter()

