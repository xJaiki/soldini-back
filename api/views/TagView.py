from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models.TagModel import Tag
from api.serializers.TagSerializer import TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
