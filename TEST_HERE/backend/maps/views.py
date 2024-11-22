from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer

@api_view(['GET', 'POST'])
def location_list(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)