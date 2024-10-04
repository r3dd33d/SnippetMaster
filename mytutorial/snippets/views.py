from rest_framework import renderers, viewsets
from .models import Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response


# UserViewSet: Handles listing and retrieving user instances.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# SnippetViewSet: Handles CRUD operations for snippets and an additional 'highlight' action.
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions. Additionally, we also provide a
    custom `highlight` action to display highlighted code in HTML.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        """
        Custom action to return highlighted HTML version of the snippet.
        """
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        """
        Associate the owner of the snippet with the user who created it.
        """
        serializer.save(owner=self.request.user)
