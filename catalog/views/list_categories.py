from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from catalog.models import Category

class ListCategories(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        categories = Category.objects.all().order_by('name')

        return Response(
            {
                'categories': [
                    {
                        "name": category.name
                    }
                    for category in categories
                ],
            },
            status=status.HTTP_200_OK,
        )