from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import AdViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')

ads_router = NestedSimpleRouter(router, r'ads', lookup='ad')
ads_router.register(r'comments', CommentViewSet, basename='ad-comments')
