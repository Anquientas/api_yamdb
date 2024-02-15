from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializers import UserAdminSerializer, UserNotAdminSerializer
from api.permissions import IsAdminOrReadOnly, IsAdmin


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
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
    def get_user_data(self, request):
        if request.method == 'PATH':
            print(request.method)
            if request.user.is_admin:
                serializer = UserAdminSerializer(
                    data=request.data,
                    partial=True
                )
            else:
                serializer = UserNotAdminSerializer(
                    data=request.data,
                    partial=True
                )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserNotAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
