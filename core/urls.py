"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from posts.views import PostsViewSet

router = DefaultRouter()
router.register('posts', PostsViewSet, 'post')

from custom_logout import views as auth_views

from posts.views import (
    PostListView,
    MyPostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

from users.views import RegisterView, email_verification

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path("logout", auth_views.logout_view, name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('email-verification', email_verification, name='email-verification'),
    path('posts/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('my-posts', MyPostListView.as_view(), name='my-posts'),
    path('posts/create', PostCreateView.as_view(), name='post-create'),
    path('posts/update/<int:pk>', PostUpdateView.as_view(), name='edit-post'),
    path('posts/delete/<int:pk>', PostDeleteView.as_view(), name='delete-post'),
    path('api', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
