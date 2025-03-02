from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'api/posts', PostViewSet, basename='post')

app_name = 'core'

urlpatterns = [
    # HTML-шаблоны
    path('', views.home, name='home'),
    path('home/', views.home, name='home1'),
    path('sign_up/', views.RegisterView.as_view(), name='sign_up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('create_post/', views.CreatePostView.as_view(), name='create_post'),
    # path('view_posts/', views.ViewPostListView.as_view(), name='view_post'),

    path('', include(router.urls)),  # API объявлений
    path('', include('apps.auths.urls')),  # API пользователей

    # JWT-токены для API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
