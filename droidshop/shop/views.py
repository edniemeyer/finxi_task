from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from droidshop.shop.serializers import UserSerializer, GroupSerializer, DemandSerializer
from droidshop.shop.models import Demand


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DemandViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows demands to be viewed or edited.
    """
    queryset = Demand.objects.all()
    serializer_class = DemandSerializer