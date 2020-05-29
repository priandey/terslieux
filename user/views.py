from rest_framework import generics
from django.contrib.auth.models import User
from user.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    """
    Provide 'list'  and 'details' actions over user resources
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer