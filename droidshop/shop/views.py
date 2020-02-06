from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from droidshop.shop.serializers import UserSerializer, GroupSerializer, DemandSerializer
from droidshop.shop.models import Demand
from droidshop.shop.permissions import IsOwnerOrAdmin


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
    # Show just objects from the owner or all objects if admin
    def get_queryset(self):
        if self.request.user.groups.filter(name='admin').exists():
            return Demand.objects.all()
        else:
            return Demand.objects.all().filter(advertiser=self.request.user)

    serializer_class = DemandSerializer

    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrAdmin]
