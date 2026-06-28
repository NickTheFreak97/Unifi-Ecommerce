from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Category

class BatchOfCategoriesSerializer(serializers.Serializer):
    categories = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        allow_null=False,
    )


    def validate_categories(self, candidate_categories):
        duplicates = { name for name in candidate_categories if candidate_categories.count(name) > 1 }
        if duplicates:
            raise serializers.ValidationError(
                {
                    'message': f"Input list has duplicated category names",
                    'duplicates': list(duplicates)
                }
            )

        return candidate_categories

class BulkCreateCategories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.has_perm('catalog.add_category'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = BatchOfCategoriesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            categories = serializer.validated_data["categories"]

            if categories is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            skipped_categories = []
            created_categories = []

            for category in categories:
                if not Category.objects.filter(name=category).exists():
                    Category.objects.create(name=category)
                    created_categories.append(category)
                else:
                    skipped_categories.append(category)

            return Response(
                {
                    'created': created_categories,
                    'skipped': skipped_categories
                },
                status=status.HTTP_201_CREATED
            )



