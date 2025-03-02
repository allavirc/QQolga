from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями:
    - API: JSON
    - HTML: шаблоны для отображения пользователей
    """
    queryset = CustomUser.objects.all().order_by('-data_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def list(self, request):
        """Возвращает список пользователей (API и HTML)"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if request.accepted_renderer.format == 'html':
            return Response({'users': queryset}, template_name='auths/user_list.html')

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Возвращает конкретного пользователя (API и HTML)"""
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = self.get_serializer(user)

        if request.accepted_renderer.format == 'html':
            return Response({'user': user}, template_name='auths/user_detail.html')

        return Response(serializer.data)
