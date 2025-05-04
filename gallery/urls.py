from django.urls import path
from . import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RouteListCreateAPIView,
    RouteRetrieveUpdateDestroyAPIView,
    PointListCreateAPIView,
    PointRetrieveUpdateDestroyAPIView
)

'''
router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'points', PointViewSet)
'''

app_name = 'gallery'

urlpatterns = [
    path('', views.route_list, name='route_list'),
    # path('api/', include(router.urls)),
    path('route/<int:route_id>/', views.view_route, name='view_route'),

    path('api/routes/', RouteListCreateAPIView.as_view(), name='route-list-create'),
    path('api/routes/<int:route_id>/', RouteRetrieveUpdateDestroyAPIView.as_view(), name='route-detail'),
    path('api/routes/<int:route_id>/points/', PointListCreateAPIView.as_view(), name='point-list-create'),
    path('api/routes/<int:route_id>/points/<int:point_id>/', PointRetrieveUpdateDestroyAPIView.as_view(), name='point-detail'),

]
