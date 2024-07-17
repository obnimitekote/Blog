from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView, DestroyAPIView

from .models import Post
from .serializers import PostSerializer
from .permissions import OwnPostOrReadOnly


class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'


class MyPostListView(ListView):
    model = Post
    template_name = 'posts/my_posts.html'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user) \
            .all()


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'posts/create.html'
    fields = ['title', 'image', 'content']

    def get_success_url(self) -> str:
        return reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return http.HttpResponseRedirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'posts/edit.html'
    fields = ['title', 'image', 'content']

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'posts/delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class PostsViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OwnPostOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@csrf_exempt
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

