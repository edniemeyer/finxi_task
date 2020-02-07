from django.contrib.auth.models import User, Group
from rest_framework import serializers
from droidshop.shop.models import Demand


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'demands']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class DemandSerializer(serializers.ModelSerializer):

    # Hide choice of Advertiser field and set the current user
    advertiser = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Demand
        fields = ['id', 'description', 'address',
                  'info', 'advertiser', 'status']
