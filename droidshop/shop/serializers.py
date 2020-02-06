from django.contrib.auth.models import User, Group
from rest_framework import serializers
from droidshop.shop.models import Demand


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = ['id', 'description', 'address', 'info', 'advertiser', 'status']