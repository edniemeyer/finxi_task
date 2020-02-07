from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    # Finalize Demand endpoint, changing status from open to closed
    @action(detail=True, methods=['PUT'], permission_classes=[IsOwnerOrAdmin])
    def finalize(self, request, pk=None):
        demand = self.get_object()
        serializer = DemandSerializer(data=request.data)

        if demand.status == Demand.CLOSED:
            return Response({'status': 'Demand has been already closed!'},
                            status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid:
            demand.status = Demand.CLOSED
            demand.save()
            return Response({'status': 'Demand closed successfully!'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    serializer_class = DemandSerializer

    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrAdmin]
