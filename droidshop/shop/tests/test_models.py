from django.test import TestCase
from ..models import Demand
from django.contrib.auth.models import User


class DemandTest(TestCase):
    """ Test module for Demand model """

    def setUp(self):
        user = User.objects.create(username='user1')
        Demand.objects.create(
            description='Desc1', address='Addr1', info='Info1', advertiser=user, status=Demand.OPEN)
        Demand.objects.create(
            description='Desc2', address='Addr2', info='Info2', advertiser=user, status=Demand.OPEN)

    def test_insertion(self):
        user = User.objects.get(username='user1')
        demand1 = Demand.objects.get(description='Desc1')
        demand2 = Demand.objects.get(description='Desc2')
        self.assertEqual(
            demand1.advertiser, user)
        self.assertEqual(
            demand2.advertiser, user)
