from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from catalog.models.products.category import Category

class CreateCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')

        if not name:
            return Response(
                {
                    'message': 'A category cannot have null or blank name.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if request.user.has_perm('catalog.add_category'):
                if Category.objects.filter(name=request.data['name']).exists():
                    return Response(
                        {
                            'message': 'Category already exists'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    new_category = Category.objects.create(name=request.data['name'])

                    return Response(
                        {
                            'message': 'Category successfully created',
                            'category': new_category.name
                        },
                        status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    {
                        'error': f"A user with groups {request.user.groups.all()[0]} cannot add a new category"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )