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

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import posts.views
from posts.views import PostsViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Blog API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


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
    PostUpdateAPIView,
    PostDeleteAPIView
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
    path("create", posts.views.create_post, name="create"),
    path("edit/<int:pk>", PostUpdateAPIView.as_view(), name="edit"),
    path("delete/<int:pk>", PostDeleteAPIView.as_view(), name="delete"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
