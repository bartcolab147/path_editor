from django.shortcuts import render, get_object_or_404, redirect
from .models import Route, Point, BackgroundImage
from django.contrib.auth.decorators import login_required
from .forms import PointForm


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RouteSerializer, PointSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

@login_required
def route_list(request):
    routes = Route.objects.filter(user=request.user).select_related('background')
    backgrounds = BackgroundImage.objects.all()

    if request.method == 'POST':
        bg_id = request.POST.get('background_id')
        if bg_id:
            background = BackgroundImage.objects.get(id=bg_id)
            # Use background name as default route name
            Route.objects.create(user=request.user, background=background, name=background.name)
            return redirect('gallery:route_list')

    # Pass both routes and backgrounds to the template
    return render(request, 'gallery/route_list.html', {'routes': routes, 'backgrounds': backgrounds})

@login_required
def view_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    points = route.points.all()  # Get all points associated with this route

    # Handle adding a point
    if request.method == 'POST' and 'add_point' in request.POST:
        form = PointForm(request.POST)
        if form.is_valid():
            new_point = form.save(commit=False)
            new_point.route = route  # Associate the point with the route
            new_point.save()
            return redirect('gallery:view_route', route_id=route.id)
    else:
        form = PointForm()

    # Handle deleting a point
    if request.method == 'POST' and 'delete_point' in request.POST:
        point_id = request.POST.get('point_id')
        point = get_object_or_404(Point, id=point_id)  # Use Point instead of RoutePoint
        point.delete()
        return redirect('gallery:view_route', route_id=route.id)

    # Combine consecutive points into pairs for drawing lines between them
    paired_points = zip(points, points[1:])

    return render(request, 'gallery/view_route.html', {
        'route': route,
        'points': points,
        'paired_points': paired_points,
        'form': form,
    })

# API VIEWS

# List and Create Routes
@extend_schema(
    summary="List user's routes or create a new route",
    description="GET: Retrieve all routes belonging to the authenticated user.\nPOST: Create a new route associated with the authenticated user."
)
class RouteListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RouteSerializer

    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve, Update, and Delete a Route
@extend_schema(
    summary="Retrieve, update, or delete a user's route",
    description="GET: Retrieve a specific route.\nPUT: Fully update an existing route.\nDELETE: Delete a route."
)
class RouteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RouteSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'route_id'

    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

    @extend_schema(exclude=True)  # Hides PATCH from Swagger
    def patch(self, request, *args, **kwargs):
        return Response({"detail": "PATCH method is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# List and Create Points for a Route
@extend_schema(
    summary="List points for a route or create a new point",
    description="GET: List all points associated with a given route.\nPOST: Create a new point for the specified route."
)
class PointListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PointSerializer

    def get_queryset(self):
        route_id = self.kwargs['route_id']
        return Point.objects.filter(route__id=route_id, route__user=self.request.user)

    def perform_create(self, serializer):
        route_id = self.kwargs['route_id']
        route = get_object_or_404(Route, id=route_id, user=self.request.user)
        serializer.save(route=route)

# Retrieve, Update, and Delete a Point
@extend_schema(
    summary="Retrieve, update, or delete a point",
    description="GET: Retrieve a specific point.\nPUT: Fully update an existing point.\nDELETE: Delete a point."
)
class PointRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PointSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'point_id'


    def get_queryset(self):
        route_id = self.kwargs['route_id']
        return Point.objects.filter(route__id=route_id, route__user=self.request.user)

    
    @extend_schema(exclude=True)  # Hides PATCH from Swagger
    def patch(self, request, *args, **kwargs):
        return Response({"detail": "PATCH method is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
