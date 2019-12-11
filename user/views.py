from rest_framework import generics
from django.contrib.auth.models import User
from user.serializers import UserSerializer


class UserList(generics.ListAPIView):
    """
    Provide 'list'  and 'details' actions over user resources
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""
    Sign in view
"""


"""
Log-in View
"""


"""
Logout view
"""



"""
Return user data
"""


"""
Allow user to change his password (and future account related data)
"""


"""
Allow user to delete his account.
"""
