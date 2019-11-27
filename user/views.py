from rest_framework import viewsets
from django.contrib.auth.models import User
from user.serializers import UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provide 'list'  and 'details' actions over user resources
    """
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
