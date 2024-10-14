from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAdminUser])
def clear_cache(request):
    cache.clear()
    return Response({"message": "Cache cleared successfully."}, status=status.HTTP_200_OK)

