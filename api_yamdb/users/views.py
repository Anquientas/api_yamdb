from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    UserAdminSerializer,
    UserNotAdminSerializer
)
from api.permissions import IsAdmin


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки запросов приложения 'users'"""

    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'head', 'options', 'patch', 'post', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me_data(self, request):
        if request.method == 'GET':
            serializer = UserAdminSerializer(request.user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
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
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_403_FORBIDDEN)
