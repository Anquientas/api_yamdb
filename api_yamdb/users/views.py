from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

# from .models import User
from .serializers import UserAdminSerializer, UserNotAdminSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (IsAuthenticated, ?)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def get_user_data(self, request):
        serializer = UserAdminSerializer(request.user)
        if request.method == 'PATH':
            if request.user.is_admin:
                serializer = UserAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = UserNotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
