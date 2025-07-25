from rest_framework import status, permissions, viewsets, generics, filters
from rest_framework.decorators import action, api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend

from users.permissions import IsAuthorOrAdmin
from .models import Ad, Comment
from .serializers import AdSerializer, CommentSerializer
from .pagination import StandardResultsSetPagination


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

    def get_queryset(self):
        return Comment.objects.filter(ad_id=self.kwargs['ad_pk'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, ad_id=self.kwargs['ad_pk'])


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
