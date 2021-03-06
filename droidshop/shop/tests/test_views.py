import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..models import Demand
from ..serializers import DemandSerializer
from django.contrib.auth.models import User, Group


# initialize the APIClient app
client = APIClient()


class GetAllDemandsTest(APITestCase):
    """ Test module for GET all demands API """

    def setUp(self):
        user = User.objects.create(username='user1')
        client.force_login(user=user)

        Demand.objects.create(
            description='Desc1', address='Addr1', info='Info1', advertiser=user, status=Demand.OPEN)
        Demand.objects.create(
            description='Desc2', address='Addr2', info='Info2', advertiser=user, status=Demand.OPEN)
        Demand.objects.create(
            description='Desc3', address='Addr3', info='Info3', advertiser=user, status=Demand.OPEN)

    def test_get_all_demands(self):
        # get API response
        url = reverse('demand-list')
        response = client.get(url, format='json')
        # get data from db
        demands = Demand.objects.all()
        objects_serializer = DemandSerializer(demands, many=True)
        self.assertEqual(response.data, objects_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleDemandTest(APITestCase):
    """ Test module for GET all demands API """

    def setUp(self):
        self.user = User.objects.create(username='user1')
        client.force_login(user=self.user)

        self.demand1 = Demand.objects.create(
            description='Desc1', address='Addr1', info='Info1', advertiser=self.user, status=Demand.OPEN)
        self.demand2 = Demand.objects.create(
            description='Desc2', address='Addr2', info='Info2', advertiser=self.user, status=Demand.OPEN)
        self.demand3 = Demand.objects.create(
            description='Desc3', address='Addr3', info='Info3', advertiser=self.user, status=Demand.OPEN)

    def test_get_valid_single_demand(self):
        # get API response
        url = reverse('demand-detail', kwargs={'pk': self.demand2.pk})
        response = client.get(url, format='json')
        # get data from db
        demand = Demand.objects.get(pk=self.demand2.pk)
        objects_serializer = DemandSerializer(demand)
        self.assertEqual(response.data, objects_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_demand(self):
        url = reverse('demand-detail', kwargs={'pk': -1})
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateDemandTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        client.force_login(user=self.user)

    def test_create_demand(self):
        """
        Ensure we can create a new demand object.
        """
        url = reverse('demand-list')
        data = {'description': 'descriptionCreated',
                'address': 'addressCreated',
                'info': 'infoCreated'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Demand.objects.count(), 1)
        self.assertEqual(Demand.objects.get().description,
                         'descriptionCreated')
        self.assertEqual(Demand.objects.get().address, 'addressCreated')
        self.assertEqual(Demand.objects.get().info, 'infoCreated')
        self.assertEqual(Demand.objects.get().status, Demand.OPEN)
        self.assertEqual(Demand.objects.get().advertiser, self.user)


class UpdateDemandTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        client.force_login(user=self.user)

        self.demand1 = Demand.objects.create(
            description='Desc1', address='Addr1', info='Info1', advertiser=self.user, status=Demand.OPEN)

    def test_update_demand(self):
        """
        Ensure we can update a demand object.
        """
        url = reverse('demand-detail', kwargs={'pk': self.demand1.pk})
        data = {'description': 'descriptionUpdated',
                'address': 'addressUpdated',
                'info': 'infoUpdated'}
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Demand.objects.get().description,
                         'descriptionUpdated')
        self.assertEqual(Demand.objects.get().address, 'addressUpdated')
        self.assertEqual(Demand.objects.get().info, 'infoUpdated')
        self.assertEqual(Demand.objects.get().status, Demand.OPEN)
        self.assertEqual(Demand.objects.get().advertiser, self.user)


class DeleteDemandTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        client.force_login(user=self.user)

        self.demand1 = Demand.objects.create(
            description='Desc1', address='Addr1', info='Info1', advertiser=self.user, status=Demand.OPEN)

    def test_valid_delete_demand(self):
        """
        Ensure we can delete a demand object.
        """
        url = reverse('demand-detail', kwargs={'pk': self.demand1.pk})
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_demand(self):
        """
        Ensure we cannot delete an invalid demand object.
        """
        url = reverse('demand-detail', kwargs={'pk': -1})
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class FinalizeDemandTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        client.force_login(user=self.user)

        self.demand1 = Demand.objects.create(
            description='Desc1', address='Addr1', info='Info1', advertiser=self.user, status=Demand.OPEN)

    def test_valid_finalize_demand(self):
        """
        Ensure we can finalize a demand object.
        """
        url = reverse('demand-finalize', kwargs={'pk': self.demand1.pk})
        response = client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Demand.objects.get().status, Demand.CLOSED)

    def test_invalid_finalize_demand(self):
        """
        Ensure we can finalize a demand object.
        """
        #close demand first
        self.test_valid_finalize_demand()
        #try to close again
        url = reverse('demand-finalize', kwargs={'pk': self.demand1.pk})
        response = client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'status': 'Demand has been already closed!'})