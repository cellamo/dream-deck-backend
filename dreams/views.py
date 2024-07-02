from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


from .serializers import DreamSerializer
from .models import Dream
from .auth_views import SignUpView, LoginView  # noqa: F401


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class DreamViewSet(viewsets.ModelViewSet):
    queryset = Dream.objects.all()
    serializer_class = DreamSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Dream.objects.all()
        return Dream.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_staff or instance.user == self.request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this dream."},
                            status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=["get"])
    def my_dreams(self, request):
        dreams = Dream.objects.filter(user=self.request.user)
        serializer = self.get_serializer(dreams, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def all_dreams(self, request):
        if not request.user.is_premium:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=403,
            )
        dreams = Dream.objects.all()
        serializer = self.get_serializer(dreams, many=True)
        return Response(serializer.data)

