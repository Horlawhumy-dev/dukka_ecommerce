import logging
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView



from .serializers import UserAccountSerializer

User = get_user_model()


class APIResponse:
    @staticmethod
    def send(message, status, data=list() or str() or dict(), err=""):
        return Response({"message": message, "status_code": status, "data": data, "error": err})

class RegisterUsersView(APIView):
    """Authorized Specific  Account View"""

    permission_classes = []
    # throttle_scope = 'register-account'

    def post(self, request, *args, **kwargs):
        serializer = UserAccountSerializer(data=self.request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse.send(
                message=f"Account for {request.data['first_name']} is successfully registered. ",
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        return APIResponse.send(
            message=f"Account with {request.data['first_name']} failed to register.",
            status=status.HTTP_400_BAD_REQUEST,
            err=str(serializer.errors)
        )


class AllUserAccountsView(APIView):
    """Authorized Specific Accounts View"""

    permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateOnePerDayThrottle]

    def get(self, request, *args, **kwargs):
        try:
            users = User.objects.all().order_by("id")
        except Exception as err:
            logging.debug(err)
            return APIResponse.send(
                message="Unable to fetch users' accounts.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                err=str(err)
                
            )

        serializer = UserAccountSerializer

        if serializer.is_valid:
            users = serializer(users, many=True).data
            return APIResponse.send(
                message="Successfully fetched users' accounts data.",
                status=status.HTTP_200_OK,
                data=users
            )
        return APIResponse.send(
            message="Some serialization failures occured.",
            status=status.HTTP_400_BAD_REQUEST,
            err=str(serializer.errors)
        )


class UserAccountView(APIView):
    """Authorized Specific Account View"""

    permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs):
        """Specific User Account Fetch"""
        try:
            user = User.objects.get(username=request.user)
        except Exception as err:
            logging.debug(err)
            return APIResponse.send(
                message=f"User account not found.",
                status=status.HTTP_404_NOT_FOUND,
                err=str(err)
            )
        
        serializer = UserAccountSerializer

        if serializer.is_valid:
            user = serializer(user, many=False).data
            return APIResponse.send(
                message=f"User account found successfully.",
                status=status.HTTP_200_OK,
                data=user
            ) 

        return APIResponse.send(
                message="Seriliazers invalid.",
                status=status.HTTP_400_BAD_REQUEST,
                err=str(serializer.errors)
            )