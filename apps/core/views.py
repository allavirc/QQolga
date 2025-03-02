from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import (
    redirect, render
)
from django.contrib.auth import (
    authenticate as dj_authenticate,
    login as dj_login,
    logout as dj_logout,
)
from django.views.generic import FormView
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse, Http404
from django.core import serializers
from typing import Any
from apps.core.models import Post
from apps.auths.forms import RegisterForm, LoginForm
from apps.core.mixin import HttpResponseMixin
from apps.auths.models import CustomUser
import random
import json
from .models import Post
from apps.core.forms import PostForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления объявлениями (Post).
    Поддерживает HTML и JSON-ответы.
    """
    queryset = Post.objects.all().order_by('-date_created')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]  # Доступ открыт всем (можно изменить)
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def list(self, request):
        """Обработчик GET-запроса для списка объявлений"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if request.accepted_renderer.format == 'html':
            return Response({'posts': queryset}, template_name='core/view_posts.html')

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Обработчик GET-запроса для одного объявления"""
        post = self.get_object()
        serializer = self.get_serializer(post)

        if request.accepted_renderer.format == 'html':
            return Response({'post': post}, template_name='core/post_detail.html')

        return Response(serializer.data)

    def perform_create(self, serializer):
        """Присваиваем текущего пользователя в качестве владельца"""
        serializer.save(owner=self.request.user)

# class ViewPostListView(ListView):
#     model = Post
#     template_name = "core/view_posts.html"
#     context_object_name = "posts"
#     ordering = ['-date_created']


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "core/create_post.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        """Autintificate user (owner)"""
        form.instance.owner = self.request.user
        return super().form_valid(form)



def generation_account():
    """Account is 20 chars"""
    ALL_ACCOUNTS = Post.objects.all()
    new_account = ""
    for _ in range(20):
        new_account += str(random.randint(0, 9))

    if new_account in ALL_ACCOUNTS:
        generation_account()

    return new_account


class RegisterView(FormView):
    template_name = 'registration/sign_up.html'
    form_class = RegisterForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        password = form.cleaned_data.get('password')
        user = CustomUser.objects.create_user(email, phone, password)
        dj_login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = dj_authenticate(email=email, password=password)
        if user:
            dj_login(self.request, user)
        else:
            form.add_error('__all__', 'Invalid data')
            return super().form_invalid(form)
        return super().form_valid(form)


class LogoutView(View):
    def get(self,  request, *args: Any, **kwargs: Any):
        dj_logout(request)
        return redirect(reverse("core:home"))



class ProfileView(HttpResponseMixin, View):
    """Get and edit user account and show user cards"""
    template_name: str = 'core/profile.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))  # Перенаправление на страницу входа
        return self.get_http_response(
            request,
            template_name=self.template_name,
            context={
                'user': request.user,
                'posts': Post.objects.filter(owner=request.user)
            }
        )



# @login_required(login_url=reverse_lazy("login"))
def home(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, "home.html",
                      {
                          'posts': Post.objects.filter(owner=user)
                      }
                      )
    return render(request, "home.html", {'posts': []})



class GetUsersView(View):
    def get(self, request):
        data = serializers.serialize('json', CustomUser.objects.all())
        return HttpResponse(
            data, content_type='application/json', status=200
        )

    def post(self, request):
        user_data = json.loads(request.body)
        email = user_data.get('email')
        phone = user_data.get('phone')
        password = user_data.get('password')
        try:
            user = CustomUser.objects.create_user(email, phone, password)
        except Exception as e:
            return JsonResponse(
                data={
                    'error': e
                }, status=400)
        data = {
            'user_id': user.id,
            'user_email': user.email,
        }
        return JsonResponse(data, status=201)

    def delete(self, request):
        try:
            user = CustomUser.objects.get(id=501)
        except:
            raise Http404
        CustomUser.objects.delete_model(user)
        return JsonResponse(
            data={'message': "DELETE"},
            status=204,
        )


class GetUserView(View):
    def get(self, request, id):
        data = serializers.serialize(
            'json',
            CustomUser.objects.filter(id=id)
        )
        return HttpResponse(
            data, content_type='application/json', status=200
        )

    def delete(self, request, id):
        try:
            user: CustomUser = CustomUser.objects.get(id=id)
        except:
            raise Http404
        user.objects.delete_model()
        return JsonResponse(
            data={'message': "DELETE"},
            status=204,
        )
